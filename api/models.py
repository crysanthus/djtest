from django.db import models
from django.contrib.auth.models import User


# define a db model named league with following
# fields: name, description
class League(models.Model):
	name = models.CharField(max_length=3)
	description = models.TextField(max_length=100)

	def __str__(self):
		return self.name


# define a db model named team with following
# fields: name, description
class Team(models.Model):
	name = models.CharField(max_length=50)
	description = models.TextField(max_length=100)
	coach = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.name
	
	
# define a db model named player with following
# fields: name, description, age, height, average_score, team
class Player(models.Model):
	name = models.CharField(max_length=50)
	bio = models.TextField(max_length=100)
	age = models.IntegerField()
	height = models.IntegerField()
	average_score = models.DecimalField(max_digits=5, decimal_places=2)
	team = models.ForeignKey(Team, on_delete=models.CASCADE)

	def __str__(self):
		return self.name


# define a db model named game with following
# fields: name, description, home_team, away_team, venue, date
# a game is a collection of matches
class Game(models.Model):
	name = models.CharField(max_length=50)
	description = models.TextField(max_length=100)
	home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
	home_score = models.IntegerField()
	away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
	away_score = models.IntegerField()
	venue = models.CharField(max_length=50)
	date = models.DateField()

	def __str__(self):
		return self.name

# define a db model named match with following
# fields: game, player, score
# a match is a collection of players and their scores in a game
class Match(models.Model):
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	player = models.ForeignKey(Player, on_delete=models.CASCADE)
	score = models.IntegerField()

	def __str__(self):
		return self.game.name
