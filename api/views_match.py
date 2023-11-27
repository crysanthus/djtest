# create API end points for the match routes
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

# import models and serializers
from .models import Match
from .serializers import  MatchSerializer


# create view for list all the matches
@api_view(['GET'])
def list_matches(request):
	"""
	Lists all the matches.

	Parameters:
	- request: The request object.

	Returns:
	A JsonResponse containing the list of matches serialized as JSON.
	"""
	matches = Game.objects.values('name', 'description', 'league', 'home_team', 'home_score', 'away_team', 'away_score', 'venue', 'date')
	return Response({'matches': list(matches)}, safe=False)


# create view for get a match as per model Match
@api_view(['GET'])
def get_match(request, pk):
	"""
	Get a specific match by its primary key.
	
	:param request: The HTTP request object.
	:param pk: The primary key of the match.
	:type pk: int
	:return: A JSON response containing the serialized match data.
	:returns type: JsonResponse
	"""
	try:
		match = Game.objects.get(pk=pk)
	except Game.DoesNotExist:
		return Response({'message': 'Match not found'}, status=status.HTTP_404_NOT_FOUND)

	serializer = GameSerializer(match, many=False)
	return Response(serializer.data, status=status.HTTP_200_OK)


# create view for add a match as per model Match
@api_view(['POST'])
def create_match(request):
	"""
	Creates a new match.

	Parameters:
		- request: The HTTP request object containing the match data.

	Returns:
		- Response: The HTTP response object containing the serialized match data.
		- status: The HTTP status code.
	"""
	serializer = GameSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()	
	return Response(serializer.data, status=status.HTTP_201_CREATED)


# create view for update a match as per model Match
@api_view(['PUT'])
def update_match(request, pk):
	"""
	Updates a specific match by its primary key.

	Parameters:
		- request: The HTTP request object containing the updated match data.
		- pk: The primary key of the match.
	Returns:
		- Response: The HTTP response object containing the serialized updated match data.
		- status: The HTTP status code.
	"""
	try:
		match = Game.objects.get(pk=pk)
	except Game.DoesNotExist:
		return Response({'message': 'Match not found'}, status=status.HTTP_404_NOT_FOUND)

	serializer = GameSerializer(match, data=request.data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# create view for delete a match as per model Match
@api_view(['DELETE'])
def delete_match(request, pk):
	"""
	Deletes a specific match by its primary key.

	Parameters:
		- request: The HTTP request object.
		- pk: The primary key of the match.
	Returns:
		- Response: The HTTP response object containing a success message.
		- status: The HTTP status code.
	"""
	try:
		match = Match.objects.get(pk=pk)
		match.delete()
		return Response({'message': 'Match deleted successfully'}, status=status.HTTP_200_OK)

	except Match.DoesNotExist:
		return Response({'message': 'Match not found'}, status=status.HTTP_404_NOT_FOUND)
