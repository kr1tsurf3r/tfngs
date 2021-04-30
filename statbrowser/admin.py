from django.contrib import admin

# Register your models here.

from .models import Player, MatchPlayer, Match 

admin.site.register(Match)