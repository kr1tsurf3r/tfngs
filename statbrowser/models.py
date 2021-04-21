from django.db import models

# Create your models here.

## Describes a single match
class Match(models.Model):
	raise NotImplementedError

## Describes a player within one match
class MatchPlayer(models.Model):
	raise NotImplementedError

## Describes a real human player (across many matches)
class Player(models.Model):
	raise NotImplementedError