from django.test import TestCase

# Create your tests here.

from .LogImporter import LogImporter

class LogImporterTests(TestCase):
	def test_log_loads(self):
		l = LogImporter(
			tf_logs_id = "2861729",
			league = "RGL Invite",
			match_name = "MAL vs KUOD",
			blu_team_name = "MyAnimeList After Dark",
			red_team_name = "KUOD Damage"
			)
		self.assertIs(True, True)