# create API end points for all the routes
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

# import models and serializers
from .models import Player
from .serializers import PlayerSerializer


# api/player view
# create api/player view for the Player model
@api_view(['GET'])
def list_players(request):
	"""
	Retrieves all player objects.

	Parameters:
		- request: The HTTP request object.
	Returns:
		- Response: The HTTP response object containing the serialized player data.
		- status: The HTTP status code.
	"""
	players = Player.objects.values('id', 'name', 'description', 'age', 'height', 'average_score', 'team')
	serializer = PlayerSerializer(players, many=True)
	return Response(serializer.data, status=status.HTTP_200_OK)


# create view for get a player as per model Player
@api_view(['GET'])
def get_player(request, pk):
	"""
	Retrieves a specific player by its primary key.

	Parameters:
		- request: The HTTP request object.
		- pk: The primary key of the player.
	Returns:
		- Response: The HTTP response object containing the serialized player data.
		- status: The HTTP status code.
	"""
	try:
		player = Player.objects.get(pk=pk)
		serializer = PlayerSerializer(player)
		return Response(serializer.data, status=status.HTTP_200_OK)

	except Player.DoesNotExist:
		return Response({'message': 'Player not found'}, status=status.HTTP_404_NOT_FOUND)


# create view to add a player as per model Player
@api_view(['POST'])
def create_player(request):
	"""
	Adds a new player to the database.

	Parameters:
		- request: The HTTP request object containing the player data.
	Returns:
		- Response: The HTTP response object containing the serialized player data.
		- status: The HTTP status code.
	"""
	serializer = PlayerSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# create view for update a player as per model Player
@api_view(['PUT'])
def update_player(request, pk):
	"""
	Updates an existing player in the database.

	Parameters:
		- request: The HTTP request object containing the updated player data.
		- pk: The primary key of the player to be updated.
	Returns:
		- Response: The HTTP response object containing the serialized updated player data.
		- status: The HTTP status code.
	"""
	try:
		player = Player.objects.get(pk=pk)
	except Player.DoesNotExist:
		return Response({'message': 'Player not found'}, status=status.HTTP_404_NOT_FOUND)

	serializer = PlayerSerializer(player, data=request.data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# create view for delete a player as per model Player
@api_view(['DELETE'])
def delete_player(request, pk):
	"""
	Deletes an existing player from the database.

	Parameters:
		- request: The HTTP request object.
		- pk: The primary key of the player to be deleted.
	Returns:
		- Response: The HTTP response object containing a success message.
		- status: The HTTP status code.
	"""
	try:
		player = Player.objects.get(pk=pk)
		player.delete()
		return Response({'message': 'Player deleted successfully'}, status=status.HTTP_200_OK)

	except Player.DoesNotExist:
		return Response({'message': 'Player not found'}, status=status.HTTP_404_NOT_FOUND)


# create view to search player by name
@api_view(['POST'])
def search_player(request):
	"""
	Searches for players by name.

	Parameters:
		- request: The HTTP request object.
	Returns:
		- Response: The HTTP response object containing the serialized player data.
		- status: The HTTP status code.
	"""
	name = request.data.get('name')
	players = Player.objects.filter(name__icontains=name).values('id', 'name', 'description', 'age', 'height', 'average_score', 'team')
	
	if not players:
		return Response({'message': 'No player found with that name'}, status=status.HTTP_404_NOT_FOUND)

	serializer = PlayerSerializer(players, many=True)
	return Response(serializer.data, status=status.HTTP_200_OK)


# create view to search player by team
@api_view(['POST'])
def search_player_by_team(request):
	"""
	Searches for players by team.

	Parameters:
		- request: The HTTP request object.
	Returns:
		- Response: The HTTP response object containing the serialized player data.
		- status: The HTTP status code.
	"""
	team = request.data.get('team')
	players = Player.objects.filter(team__icontains=team).values('id', 'name', 'description', 'age', 'height', 'average_score', 'team')
	
	if not players:
		return Response({'message': 'No player found in that team'}, status=status.HTTP_404_NOT_FOUND)

	serializer = PlayerSerializer(players, many=True)
	return Response(serializer.data, status=status.HTTP_200_OK)


# calculate xth percentiles values to find top players
def calculate_xth_percentile(players, percentile):
	"""
	Calculates the xth percentile of a list of numbers.
	TODO: check percentile value
	"""
	scores = [player.average_score for player in players]
	scores.sort()
	percentile_index = int((percentile / 100.0) * len(scores))
	return scores[percentile_index]


def filter_players_above_xth_percentile(players, percentile=90):
	x_percentile = calculate_xth_percentile(players, percentile)
	filtered_players = [player for player in players if player.average_score >= x_percentile]
	return filtered_players


# create view to search player by average score above or equal to a value
@api_view(['POST'])
def search_player_by_average_score(request):
	"""
	Searches for players by average score above or equal to a given value.

	Parameters:
		- request: The HTTP request object.
	Returns:
		- Response: The HTTP response object containing the serialized player data.
		- status: The HTTP status code.
	"""
	
	# calculate xth percentile of score per player in a team
	team = request.data.get('team')

	# any value between 1 to 100
	# this needed to be restricted using a 1-100 slider in front end
	percentile = request.data.get('percentile')

	# get players by team
	players = Player.objects.filter(team=team).values('id', 'name', 'bio', 'age', 'height', 'average_score', 'team')

	if not players:
		return Response({'message': 'No players found team with that name'}, status=status.HTTP_404_NOT_FOUND)

	# calculate xth percentile
	top_players = filter_players_above_xth_percentile(players, percentile)

	if not top_players:
		return Response({'message': 'No players found with that average score'}, status=status.HTTP_404_NOT_FOUND)

	serializer = PlayerSerializer(top_players, many=True)
	return Response(serializer.data, status=status.HTTP_200_OK)
