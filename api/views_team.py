# create API end points for team routes
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

# import models and serializers
from .models import Team
from .serializers import TeamSerializer

@api_view(['GET'])
def list_teams(request):
	"""
	Lists all the teams.

	Parameters:
	- request: The request object.

	Returns:
	A JsonResponse containing the list of teams serialized as JSON.
	"""
	teams = Team.objects.values('name', 'description')
	return Response({'teams': list(teams)}, safe=False)


@api_view(['GET'])
def get_team(request, pk):
	"""
	Get a specific team by its primary key.
	
	:param request: The HTTP request object.
	:param pk: The primary key of the team.
	:type pk: int
	:return: A JSON response containing the serialized team data.
	:returns type: JsonResponse
	"""
	try:
		team = Team.objects.get(pk=pk)
	except Team.DoesNotExist:
		return Response({'message': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)

	team = Team.objects.get(pk=pk)
	serializer = TeamSerializer(team, many=False)
	return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_team(request):
	"""
	Creates a new team.

	Parameters:
		- request: The HTTP request object containing the team data.

	Returns:
		- Response: The HTTP response object containing the serialized team data.
		- status: The HTTP status code.
	"""
	serializer = TeamSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
	return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
def update_team(request, pk):
	"""
	Updates a team.

	Parameters:
		- request: The HTTP request object containing the updated team data.
		- pk: The primary key of the team to update.

	Returns:
		- Response: The HTTP response object containing the serialized team data.
		- status: The HTTP status code.
	"""
	try:
		team = Team.objects.get(pk=pk)
		serializer = TeamSerializer(team, data=request.data)
		if serializer.is_valid():
			serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)
	
	except Team.DoesNotExist:
		return Response({'message': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_team(request, pk):
	"""
	Deletes a team.

	Parameters:
		- request: The HTTP request object.
		- pk: The primary key of the team to delete.

	Returns:
		- Response: The HTTP response object containing a success message.
		- status: The HTTP status code.
	"""
	try:
		team = Team.objects.get(pk=pk)
		team.delete()
		return Response({'message': 'Team deleted successfully'}, status=status.HTTP_200_OK)
	
	except Team.DoesNotExist:
		return Response({'message': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)

