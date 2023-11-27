# create API end points for all the routes
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import logout

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

# import models and serializers
from .models import Game
from .serializers import GameSerializer


# create api/game view for the Game model
@api_view(['GET'])
def list_games(request):
	"""
	Retrieves all game objects.

	Parameters:
		- request: The HTTP request object.
	Returns:
		- Response: The HTTP response object containing the serialized game data.
		- status: The HTTP status code.
	"""
	games = Game.objects.all()
	serializer = GameSerializer(games, many=True)
	return Response(serializer.data, status=status.HTTP_200_OK)


# create view for get a game as per model Game
@api_view(['GET'])
def get_game(request, pk):
	"""
	Retrieves a specific game by its primary key.

	Parameters:
		- request: The HTTP request object.
		- pk: The primary key of the game.
	Returns:
		- Response: The HTTP response object containing the serialized game data.
		- status: The HTTP status code.
	"""
	try:
		game = Game.objects.get(pk=pk)
		serializer = GameSerializer(game)
		return Response(serializer.data, status=status.HTTP_200_OK)

	except Game.DoesNotExist:
		return Response({'message': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)


# create view for add a game as per model Game
@api_view(['POST'])
def create_game(request):
	"""
	Creates a new game.

	Parameters:
		- request: The HTTP request object containing the game data.

	Returns:
		- Response: The HTTP response object containing the serialized game data.
		- status: The HTTP status code.
	"""
	serializer = GameSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# create view for update a game as per model Game
@api_view(['PUT'])
def update_game(request, pk):
	"""
	Updates a specific game by its primary key.

	Parameters:
		- request: The HTTP request object containing the updated game data.
		- pk: The primary key of the game.
	Returns:
		- Response: The HTTP response object containing the serialized updated game data.
		- status: The HTTP status code.
	"""
	try:
		game = Game.objects.get(pk=pk)
		serializer = GameSerializer(game, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	except Game.DoesNotExist:
		return Response({'message': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)


# create view for delete a game as per model Game
@api_view(['DELETE'])
def delete_game(request, pk):
	"""
	Deletes a specific game by its primary key.

	Parameters:
		- request: The HTTP request object.
		- pk: The primary key of the game.
	Returns:
		- Response: The HTTP response object containing a success message.
		- status: The HTTP status code.
	"""
	try:
		game = Game.objects.get(pk=pk)
		game.delete()
		return Response({'message': 'Game deleted successfully'}, status=status.HTTP_200_OK)

	except Game.DoesNotExist:
		return Response({'message': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)
