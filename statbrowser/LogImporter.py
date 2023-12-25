"""
This script handles database population of the
database with info from a game log
"""

import json
import requests

from .models import (
	Match, Player, MatchPlayer, MatchRound, MatchEvent, 
	TeamEnum, RoundPlayer, MatchEventTypeEnum
	)

CLASSES = [
	"scout", "soldier", "pyro", "demoman", "heavy",
	"engineer", "medic", "sniper", "spy"
]

CLASS_STATS = [
	("kills", "kills"),
	("assists", "assists"),
	("deaths", "deaths"),
	("damage", "dmg"),
	("time", "total_time")
]

class LogImporter:
	def __init__(self, 
		tf_logs_id, 
		league, 
		match_name,
		blu_team_name,
		red_team_name,
		overwrite = True
		):
		## Check if already in database and confirm overwrite
		obj = Match.objects.filter(
			match_logs_id = tf_logs_id
			).first()

		if obj and not overwrite:
			raise RuntimeError(
				f"Log {tf_logs_id} already in database"
				)

		## Retrieve JSON
		self.log_json = requests.get(
			f"https://logs.tf/api/v1/log/{tf_logs_id}"
			).json()

		## Initialize new match
		match = Match(
			league = league,
			match_name = match_name,
			blu_team_name = blu_team_name,
			red_team_name = red_team_name,
			red_score = self.get_team_score("Red"),
			blu_score = self.get_team_score("Blue"),
			match_time = self.get_match_time(),
			match_logs_id = tf_logs_id
			)
		match.save()

		## Populate match players
		for player_id in self.get_player_ids():
			## Check if Player already exists, create if not
			player = Player.get_player_from_player_id(Player, player_id)
			if not player:
				player = Player(
					player_id = player_id
					)
				player.save()

			match_player = MatchPlayer(
				player = player,
				match = match,
				player_disp_name = self.get_player_display_name(player_id),
				team = self.get_player_teamname(player_id, match)
				)

			## Populate class stats
			for class_name in CLASSES:
				for class_stat_pair in CLASS_STATS:
					match_player.__dict__[
					class_name+"_"+class_stat_pair[0] 
					] = self.get_class_stat(
						player_id, class_name, class_stat_pair[1]
						)

			## Populate heals received
			match_player.heals_received = self.get_heals_received(player_id)

			## Populate uber used stats
			match_player.medigun_ubers = self.get_ubers(player_id, "medigun")
			match_player.kritzkrieg_ubers = self.get_ubers(player_id, "kritzkrieg")

			## Populate hp from medkits
			match_player.hp_from_medkits = self.get_hp_from_medkits(player_id)

			## Populate ubers dropped
			match_player.uber_drops = self.get_ubers_dropped(player_id)

			match_player.save()

		## Populate MatchRounds
		for i in range(self.get_n_rounds()):
			match_round = MatchRound(
				match = match,
				start_time = self.get_match_start_time(i),
				winner = self.get_round_winner(i),

				red_score = self.get_round_team_stat(i, TeamEnum.RED, "score"),
				red_team_kills = self.get_round_team_stat(i, TeamEnum.RED, "kills"),
				red_team_damage = self.get_round_team_stat(i, TeamEnum.RED, "dmg"),
				red_team_ubers = self.get_round_team_stat(i, TeamEnum.RED, "ubers"),

				blu_score = self.get_round_team_stat(i, TeamEnum.BLU, "score"),
				blu_team_kills = self.get_round_team_stat(i, TeamEnum.BLU, "kills"),
				blu_team_damage = self.get_round_team_stat(i, TeamEnum.BLU, "dmg"),
				blu_team_ubers = self.get_round_team_stat(i, TeamEnum.BLU, "ubers"),

				first_cap = self.get_round_first_cap(i),
				round_duration = self.get_round_duration(i)
				)
			match_round.save()

			## Populate match players
			for player_id in self.get_player_ids():
				round_player = RoundPlayer

			## Populate round Events
			for j in range(self.get_n_events(i)):
				event_type = self.get_event_type(i, j)

				match_event = MatchEvent(
					match = match,
					match_round = match_round,
					event_type = event_type,
					event_time = self.get_match_event_time(i, j),
					event_team = self.get_match_event_team(i, j)
					)
		
				if event_type == MatchEventTypeEnum.POINT_CAP:
					match_event.point = self.get_match_event_point(i, j)

				elif event_type == MatchEventTypeEnum.UBER_CHARGE:
					match_event.event_medigun = self.get_event_medigun(i, j)
					match_event.match_player_id = self.get_event_player(i, j)

				elif event_type == MatchEventTypeEnum.MEDIC_DEATH:
					match_event.match_player_id = self.get_event_player(i, j)
					match_event.killer_player_id = self.get_event_killer(i, j)

				elif event_type == MatchEventTypeEnum.UBER_DROP:
					match_event.matc_player_id = self.get_event_player(i, j)

				elif event_type == MatchEventTypeEnum.ROUND_WIN:
					continue

				else:
					raise ValueError(f"Received invalid event type '{event_type}'")
					
				match_event.save()


			## Populate round players
			for player_id in self.get_round_player_ids(i):
				match_player = self.get_match_player_from_id(match, player_id)

				round_player = RoundPlayer(
					match = match,
					match_round = match_round,
					match_player = match_player,
					round_kills = self.get_round_player_stat(i, player_id, "kills"),
					round_damage = self.get_round_player_stat(i, player_id, "dmg")
					)
				
				round_player.save()


	def get_team_score(self, team):
		return self.log_json["teams"][team]["score"]

	def get_match_time(self):
		return self.log_json["length"]

	def get_player_ids(self):
		return list(self.log_json["players"].keys())

	def get_player_display_name(self, player_id):
		return self.log_json["names"][player_id]

	def get_player_teamname(self, player_id, match):
		player_team_color = self.log_json["players"][player_id]["team"]
		if player_team_color == "Blue":
			return match.blu_team_name
		else:
			return match.red_team_name

	def get_class_stat(self, player_id, class_name, stat_name):
		class_stats = self.log_json["players"][player_id]["class_stats"]
		for class_stat in class_stats:
			if class_stat["type"] == class_name:
				return class_stat[stat_name]
		return 0

	def get_heals_received(self, player_id):
		return self.log_json["players"][player_id]["hr"]

	def get_ubers(self, player_id, gun_name):
		try:
			return self.log_json["players"][player_id]["ubertypes"][gun_name]
		except KeyError:
			return 0

	def get_hp_from_medkits(self, player_id):
		return self.log_json["players"][player_id]["medkits_hp"]

	def get_ubers_dropped(self, player_id):
		try:
			return self.log_json["players"][player_id]["drops"]
		except KeyError:
			return 0

	def get_n_rounds(self):
		return len(self.log_json["rounds"])

	def get_match_start_time(self, round_num):
		return self.log_json["rounds"][round_num]["start_time"]

	def get_round_winner(self, round_num):
		winner = self.log_json["rounds"][round_num]["winner"]
		if winner == "Blue":
			return TeamEnum.BLU.value
		elif winner == "Red":
			return TeamEnum.RED.value
		else:
			return "Neither"

	def get_round_team_stat(self, round_num, team, stat_name):
		if team == TeamEnum.RED:
			team = "Red"
		else: 
			team = "Blue"
		return self.log_json["rounds"][round_num]["team"][team][stat_name]

	def get_round_first_cap(self, round_num):
		first_cap_team = self.log_json["rounds"][round_num]["firstcap"]
		if first_cap_team == "Blue":
			return TeamEnum.BLU.value
		elif first_cap_team == "Red":
			return TeamEnum.RED.value
		else:
			return "Neither"

	def get_round_duration(self, round_num):
		return self.log_json["rounds"][round_num]["length"]

	def get_n_events(self, round_num):
		return len(self.log_json["rounds"][round_num]["events"])

	def get_event_type(self, round_num, event_num):
		return self.log_json["rounds"][round_num]["events"][event_num]["type"]

	def get_match_event_time(self, round_num, event_num):
		event_time = self.log_json["rounds"][round_num]["events"][event_num]["time"]
		#if event_time < 0:
		#	raise ValueError(f"Negative time delta in match event {(round_num, event_num)}")
		return event_time

	def get_match_event_team(self, round_num, event_num):
		event_team = self.log_json["rounds"][round_num]["events"][event_num]["team"]
		if event_team == "Blue":
			return TeamEnum.BLU.value
		elif event_team == "Red":
			return TeamEnum.RED.value
		else:
			return "Neither"

	def get_match_event_point(self, round_num, event_num):
		return self.log_json["rounds"][round_num]["events"][event_num]["point"]

	def get_event_medigun(self, round_num, event_num):
		return self.log_json["rounds"][round_num]["events"][event_num]["medigun"]

	def get_event_player(self, round_num, event_num):
		return self.log_json["rounds"][round_num]["events"][event_num]["steamid"]

	def get_event_killer(self, round_num, event_num):
		return self.log_json["rounds"][round_num]["events"][event_num]["killer"]

	def get_round_player_ids(self, round_num):
		return list(self.log_json["rounds"][round_num]["players"].keys())

	def get_match_player_from_id(self, match, player_id):
		return MatchPlayer.objects.filter(
			match = match,
			player__player_id = player_id
			).first()

	def get_round_player_stat(self, round_num, player_id, stat_name):
		return self.log_json["rounds"][round_num]["players"][player_id][stat_name]
		







