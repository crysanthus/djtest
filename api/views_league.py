# create API end points for league routes
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

# import models and serializers
from .models import League
from .serializers import LeagueSerializer

# api/leagues

@api_view(['GET'])
def list_leagues(request):
	"""
	Lists all the leagues.

	Parameters:
	- request: The request object.

	Returns:
	A JsonResponse containing the list of leagues serialized as JSON.
	"""
	leagues = League.objects.values('name', 'description')
	return JsonResponse({'leagues': list(leagues)}, safe=False)


@api_view(['GET'])
def get_league(request, pk):
	"""
	Get a specific league by its primary key.
	
	:param request: The HTTP request object.
	:param pk: The primary key of the league.
	:type pk: int
	:return: A JSON response containing the serialized league data.
	:returns type: JsonResponse
	"""
	try:
		league = League.objects.get(pk=pk)
	except League.DoesNotExist:
		return Response({'message': 'League not found'}, status=status.HTTP_404_NOT_FOUND)

	serializer = LeagueSerializer(league, many=False)
	return Response({'league':serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_league(request):
	"""
	Creates a new league.

	Parameters:
		- request: The HTTP request object containing the league data.

	Returns:
		- Response: The HTTP response object containing the serialized league data.
		- status: The HTTP status code.
	"""
	serializer = LeagueSerializer(data=request.data)
	
	if serializer.is_valid():
		serializer.save()
	return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
def update_league(request, pk):
	"""
	Updates a league.

	Parameters:
		- request: The HTTP request object containing the updated league data.
		- pk: The primary key of the league to update.

	Returns:
		- Response: The HTTP response object containing the serialized league data.
		- status: The HTTP status code.
	"""
	try:
		league = League.objects.get(pk=pk)
		serializer = LeagueSerializer(league, data=request.data)
	
		if serializer.is_valid():
			serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)
	
	except League.DoesNotExist:
		return Response({'message': 'League not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_league(request, pk):
	"""
	Deletes a league.

	Parameters:
		- request: The HTTP request object.
		- pk: The primary key of the league to delete.

	Returns:
		- Response: The HTTP response object containing a success message.
		- status: The HTTP status code.
	"""
	try:
		league = League.objects.get(pk=pk)
		league.delete()
		return Response({'message': 'League deleted successfully'}, status=status.HTTP_200_OK)
	
	except League.DoesNotExist:
		return Response({'message': 'League not found'}, status=status.HTTP_404_NOT_FOUND)
