"""
This script handles database population of the
database with info from a game log
"""

import json
import requests

from .models import Match, Player, MatchPlayer, MatchRound, MatchEvent

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

			for class_name in CLASSES:
				for class_stat_pair in CLASS_STATS:
					match_player.__dict__[
					class_name+"_"+class_stat_pair[0] 
					] = self.get_class_stat(
						player_id, class_name, class_stat_pair[1]
						)


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



