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
# from .models import League, Team, Game, Match, Player
# from .serializers import (
# 	UserSerializer, LeagueSerializer, TeamSerializer, MatchSerializer, PlayerSerializer
# )

# import views CRUD
from .views_league import list_leagues, get_league, create_league, update_league, delete_league
from .views_team import list_teams, get_team, create_team, update_team, delete_team
from .views_game import list_games, get_game, create_game, update_game, delete_game
from .views_match import list_matches, get_match, create_match, update_match, delete_match
from .views_player import list_players, get_player, create_player, update_player, delete_player


# API Info
@api_view(['GET'])
def index(request):
	"""
	A view function for the index page of the API.

	Parameters:
		- request: The HTTP request object.

	Returns:
		- Response: The HTTP response containing a list of API endpoints.
	"""
	return Response({"status": status.HTTP_200_OK, "description": "List of API end points: /api/league, /api/team, /api/match, /api/game, /api/player"})


# create user signup, login and logout endpoints
@api_view(['POST'])
def signup(request):
	"""
	Handle the signup request.

	Parameters:
	- request: The HTTP request object containing the signup data.

	Return:
	- If the signup data is valid, return a response with the user token and data (status code 201).
	- If the signup data is invalid, return a response with the validation errors (status code 400).
	"""
	serializer = UserSerializer(data=request.data)
	
	if serializer.is_valid():
		serializer.save()
		user = User.objects.get(username=request.data['username'])
		user.set_password(request.data['password'])
		user.save()
		token = Token.objects.create(user=user)
		return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)
	
	return Response({'message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
	"""
	Handles the login functionality.

	Parameters:
	- request: The HTTP request object.

	Returns:
	- HttpResponse: The HTTP response containing the token and user details if the login is successful, 
	  otherwise an HTTP response with an error message and status code 401.
	"""
	user = get_object_or_404(User, username=request.data['username'])
	if not user.check_password(request.data['password']):
		return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

	token, _ = Token.objects.get_or_create(user=user)
	serializer = UserSerializer(instance=user)
	return Response({'token': token.key, 'user': serializer.data['email']}, status=status.HTTP_200_OK)


# design logout functionality
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
	"""
	Handles the logout functionality.

	Parameters:
	- request: The HTTP request object.

	Returns:
	- HttpResponse: The HTTP response containing a success message and status code 200.
	"""
	# Perform logout logic here
	request.user.auth_token.delete()
	return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
	"""
	Handles the login request.

	Parameters:
	- request: The HTTP request object.

	Returns:
	- HttpResponse: The response containing the message 'Login successful' with a status code of 200.
	"""
	return Response({'message': f'Login successful for {request.user.email}'}, status=status.HTTP_200_OK)


