import datetime
from django.db import models
from enum import Enum

class TeamEnum(Enum):
	RED = "RED"	
	BLU = "BLU"

# Create your models here.

## Describes a single match
class Match(models.Model):
	league = models.CharField(
		max_length = 20,
		default = None
		)
	match_name = models.CharField( # Something like "Week 1A" or "Lower Bracket Semifinals"
		max_length = 200,
		default = None
		)
	blu_team_name = models.CharField(
		max_length = 100,
		default = None
		)
	red_team_name = models.CharField(
		max_length = 100,
		default = None
		)
	blu_score = models.PositiveIntegerField(
		"Blu Score", 
		default = None
		)
	red_score = models.PositiveIntegerField(
		"Red Score", 
		default = None
		)
	match_time = models.PositiveIntegerField(
		"Total Match Time", 
		default = None
		)
	match_logs_id = models.CharField(
		"logs.tf ID(s)",
		max_length = 20,
		default = None
		)

	def __str__(self):
		return (
			f"Match {self.match_logs_id}: "
			f"{self.blu_team_name} {self.blu_score} - "
			f"{self.red_score} {self.red_team_name} "
			f"\nLeague: {self.league} "
			f"\n{self.match_name}"
			f"\nMatch duration: {datetime.timedelta(seconds = self.match_time)}"
			)

## Describes a real human player (across many matches)
class Player(models.Model):
	player_id = models.CharField(
		"Steam Player ID", 
		max_length = 50
		)
	avg_kills_assists = models.PositiveIntegerField(
		"Average Kills and Assists", 
		default = 0
		)
	avg_deaths = models.PositiveIntegerField(
		"Average Deaths", 
		default = 0
		)

	def get_player_from_player_id(self, player_id):
		return self.objects.filter(player_id = player_id).first()

## Describes a player within one match
class MatchPlayer(models.Model):
	player = models.ForeignKey(Player, on_delete = models.PROTECT)
	match = models.ForeignKey(Match, on_delete = models.CASCADE)
	player_disp_name = models.CharField(
		"Player Display Name", # Name used for the match
		max_length = 100,
		default = ""
		)
	team = models.CharField(
		"First team to capture a point",
		max_length = 3,
		choices = [(tag, tag.value) for tag in TeamEnum],
		default = None
		)

	## Scout data
	scout_kills = models.PositiveIntegerField(
		"Kills As Scout",
		default = 0
		)
	scout_assists = models.PositiveIntegerField(
		"Assists as Scout",
		default = 0
		)
	scout_deaths = models.PositiveIntegerField(
		"Deaths as Scout",
		default = 0
		)
	scout_damage = models.PositiveIntegerField(
		"Damage done as Scout",
		default = 0
		)
	scout_time = models.PositiveIntegerField(
		"Time played as Scout",
		default = 0
		)

	## Soldier data
	soldier_kills = models.PositiveIntegerField(
		"Kills as Soldier",
		default = 0
		)
	soldier_assists = models.PositiveIntegerField(
		"Assists as Soldier",
		default = 0
		)
	soldier_deaths = models.PositiveIntegerField(
		"Deaths as Soldier",
		default = 0
		)
	soldier_damage = models.PositiveIntegerField(
		"Damage done as Soldier",
		default = 0
		)
	soldier_time = models.PositiveIntegerField(
		"Time played as Soldier",
		default = 0
		)

	## Pyro
	pyro_kills = models.PositiveIntegerField(
		"Kills as Pyro",
		default = 0
		)
	pyro_assists = models.PositiveIntegerField(
		"Assists as Pyro",
		default = 0
		)
	pyro_deaths = models.PositiveIntegerField(
		"Deaths as Pyro",
		default = 0
		)
	pyro_damage = models.PositiveIntegerField(
		"Damage done as Pyro",
		default = 0
		)
	pyro_time = models.PositiveIntegerField(
		"Time played as Pyro",
		default = 0
		)

	## Demo
	demoman_kills = models.PositiveIntegerField(
		"Kills as Demoman",
		default = 0
		)
	demoman_assists = models.PositiveIntegerField(
		"Assists as Demoman",
		default = 0
		)
	demoman_deaths = models.PositiveIntegerField(
		"Deaths as Demoman",
		default = 0
		)
	demoman_damage = models.PositiveIntegerField(
		"Damage done as Demoman",
		default = 0
		)
	demoman_time = models.PositiveIntegerField(
		"Time played as Demoman",
		default = 0
		)

	## Heavy
	heavy_kills = models.PositiveIntegerField(
		"Kills as Heavy",
		default = 0
		)
	heavy_assists = models.PositiveIntegerField(
		"Assists as Heavy",
		default = 0
		)
	heavy_deaths = models.PositiveIntegerField(
		"Deaths as Heavy",
		default = 0
		)
	heavy_damage = models.PositiveIntegerField(
		"Damage done as Heavy",
		default = 0
		)
	heavy_time = models.PositiveIntegerField(
		"Time played as Heavy",
		default = 0
		)

	## Engineer
	engineer_kills = models.PositiveIntegerField(
		"Kills as Engineer",
		default = 0
		)
	engineer_assists = models.PositiveIntegerField(
		"Assists as Engineer",
		default = 0
		)
	engineer_deaths = models.PositiveIntegerField(
		"Deaths as Engineer",
		default = 0
		)
	engineer_damage = models.PositiveIntegerField(
		"Damage done as Engineer",
		default = 0
		)
	engineer_time = models.PositiveIntegerField(
		"Time played as Engineer",
		default = 0
		)

	## Medic
	medic_kills = models.PositiveIntegerField(
		"Kills as Medic",
		default = 0
		)
	medic_assists = models.PositiveIntegerField(
		"Assists as Medic",
		default = 0
		)
	medic_deaths = models.PositiveIntegerField(
		"Deaths as Medic",
		default = 0
		)
	medic_damage = models.PositiveIntegerField(
		"Damage done as Medic",
		default = 0
		)
	medic_time = models.PositiveIntegerField(
		"Time played as Medic",
		default = 0
		)

	## Sniper
	sniper_kills = models.PositiveIntegerField(
		"Kills as Sniper",
		default = 0
		)
	sniper_assists = models.PositiveIntegerField(
		"Assists as Sniper",
		default = 0
		)
	sniper_deaths = models.PositiveIntegerField(
		"Deaths as Sniper",
		default = 0
		)
	sniper_damage = models.PositiveIntegerField(
		"Damage done as Sniper",
		default = 0
		)
	sniper_time = models.PositiveIntegerField(
		"Time played as Sniper",
		default = 0
		)

	## Spy
	spy_kills = models.PositiveIntegerField(
		"Kills as Spy",
		default = 0
		)
	spy_assists = models.PositiveIntegerField(
		"Assists as Spy",
		default = 0
		)
	spy_deaths = models.PositiveIntegerField(
		"Deaths as Spy",
		default = 0
		)
	spy_damage = models.PositiveIntegerField(
		"Damage done as Spy",
		default = 0
		)
	spy_time = models.PositiveIntegerField(
		"Time played as Spy",
		default = 0
		)

	heals_received = models.PositiveIntegerField(
		"Heals Received",
		default = 0
		)
	medigun_ubers = models.PositiveIntegerField(
		"Ubers with Medigun",
		default = 0
		)
	kritzkrieg_ubers = models.PositiveIntegerField(
		"Ubers with Kritzkrieg",
		default = 0
		)
	hp_from_medkits = models.PositiveIntegerField(
		"Health from medkits",
		default = 0
		)
	uber_drops = models.PositiveIntegerField(
		"Ubers dropped",
		default = 0
		)

# Describes one round within a Match
class MatchRound(models.Model):
	match = models.ForeignKey(Match, on_delete = models.CASCADE)

	start_time = models.PositiveIntegerField(
		"Timestamp for start of round",
		default = None
		)

	winner = models.CharField(
		max_length = 3,
		choices = [(tag, tag.value) for tag in TeamEnum]
		)

	## RED team data
	red_score = models.PositiveIntegerField(
		"RED team score",
		default = None
		)
	red_team_kills = models.PositiveIntegerField(
		"Kills by RED team",
		default = 0
		)
	red_team_damage = models.PositiveIntegerField(
		"Damage done by RED team",
		default = 0
		)
	red_team_ubers = models.PositiveIntegerField(
		"Ubers by RED team",
		default = 0
		)

	## BLU team data
	blu_score = models.PositiveIntegerField(
		"BLU team score",
		default = None
		)
	blu_team_kills = models.PositiveIntegerField(
		"Kills by BLU team",
		default = 0
		)
	blu_team_damage = models.PositiveIntegerField(
		"Damage done by BLU team",
		default = 0
		)
	blu_team_ubers = models.PositiveIntegerField(
		"Ubers by BLU team",
		default = 0
		)

	first_cap = models.CharField(
		"First team to capture a point",
		max_length = 3,
		choices = [(tag, tag.value) for tag in TeamEnum]
		)

	round_duration = models.PositiveIntegerField(
		"Duration of the round",
		default = None
		)

class RoundPlayer(models.Model):
	match = models.ForeignKey(Match, on_delete = models.CASCADE)
	match_round = models.ForeignKey(MatchRound, on_delete = models.CASCADE)
	match_player = models.ForeignKey(MatchPlayer, on_delete = models.CASCADE)

	round_kills = models.PositiveIntegerField(
		"Round kills by player",
		default = 0
		)
	round_damage = models.PositiveIntegerField(
		"Round damage by player",
		default = 0
		)

class MatchEventTypeEnum(str, Enum):
	POINT_CAP = "pointcap"
	UBER_CHARGE = "charge"
	MEDIC_DEATH = "medic_death"
	UBER_DROP = "drop"
	ROUND_WIN = "round_win"

class MedigunEnum(Enum):
	MEDIGUN = "Medigun"
	KRITZKRIEG = "Kritzkrieg"

class MatchEvent(models.Model):
	match = models.ForeignKey(Match, on_delete = models.CASCADE)
	match_round = models.ForeignKey(MatchRound, on_delete = models.CASCADE)
	#match_player = models.ForeignKey(MatchPlayer, on_delete = models.CASCADE)
	match_player_id = models.CharField(
		"Steam Player ID for player", 
		max_length = 50
		)
	#killer = models.ForeignKey(MatchPlayer, on_delete = models.CASCADE, 
	#	related_name = "player_killer")
	killer_player_id = models.CharField(
		"Steam Player ID for killer",
		max_length = 50,
		null = True,
		default = None
		)

	event_type = models.CharField(
		"Type of the round event",
		max_length = 15,
		choices = [(tag, tag.value) for tag in MatchEventTypeEnum]
		)
	event_time = models.PositiveIntegerField(
		"Time that event occurred",
		default = None 
		)
	event_team = models.CharField(
		"Team for the event",
		max_length = 3,
		choices = [(tag, tag.value) for tag in TeamEnum]
		)
	event_medigun = models.CharField(
		"Medigun used in event",
		max_length = 10,
		null = True,
		default = None,
		choices = [(tag, tag.value) for tag in MedigunEnum]
		)
	point = models.PositiveIntegerField(
		"Point captured in event",
		null = True,
		default = None
		)


















