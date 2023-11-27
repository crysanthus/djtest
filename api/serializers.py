"""
	All model serializers for the API
"""
from rest_framework import serializers
from django.contrib.auth.models import User

from .models import (
	League, Team, Game, Player, Match
)


# create a serializer for each model
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'password', 'email')
		extra_kwargs = {'password': {'write_only': True, 'required': True}}

class LeagueSerializer(serializers.ModelSerializer):
	class Meta:
		model = League
		fields = '__all__'

class PlayerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Player
		fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
	class Meta:
		model = Team
		fields = '__all__'

class GameSerializer(serializers.ModelSerializer):
	class Meta:
		model = Game
		fields = '__all__'

class MatchSerializer(serializers.ModelSerializer):
	class Meta:
		model = Match
		fields = '__all__'

