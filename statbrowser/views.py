from django.shortcuts import render
from django.http import HttpResponse
from django_pandas.io import read_frame
from django_tables2 import SingleTableView
from django.views.generic import ListView

from .models import Match
from .tables import MatchTable

# Create your views here.

"""
def index(request):
	matches = read_frame(Match.objects.all())
	#return HttpResponse(str(matches.to_html()))
	return HttpResponse()
"""

"""
class MatchListView(ListView):
	model = Match
	template_name = "statbrowser/index.html"
"""

class MatchListView(SingleTableView):
	model = Match
	table_class = MatchTable
	template_name = "statbrowser/index.html"

