from django.test import TestCase

# Create your tests here.

from .LogImporter import LogImporter

class LogImporterTests(TestCase):
	def test_log_loads(self):
		l = LogImporter(
			#tf_logs_id = "2861729",
			tf_logs_id = "2818748",
			league = "RGL Invite",
			match_name = "FROYO vs HRTeam",
			blu_team_name = "HRTeam",
			red_team_name = "froyotech"
			)
		self.assertIs(True, True)