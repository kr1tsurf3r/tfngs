import django_tables2 as tables 
from .models import Match, Player, MatchPlayer

class MatchTable(tables.Table):
	class Meta:
		model = Match
		#template_name = "django_tables2/bootstrap.html"
		fields = (
			"blu_score", "blu_team_name", "league", "match_id", "match_name",
			"match_time", "red_score", "red_team_name"
			)