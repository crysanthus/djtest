"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  re_path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  re_path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, re_path
	2. Add a URL to urlpatterns:  re_path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import re_path

# api/urls.py
import api.views

urlpatterns = [
	re_path('admin', admin.site.urls),
	re_path('index', api.views.index),
	re_path('signup', api.views.signup),
	re_path('login', api.views.login),
	re_path('logout', api.views.logout),
	re_path('test_token', api.views.test_token),

	# Leagues
	re_path('list_leagues', api.views.list_leagues),
	re_path('get_league/<int:pk>', api.views.get_league),
	re_path('create_league', api.views.create_league),
	re_path('update_league/<int:pk>', api.views.update_league),
	re_path('delete_league/<int:pk>', api.views.delete_league),

	# Teams
	re_path('list_teams', api.views.list_teams),
	re_path('get_team/<int:pk>', api.views.get_team),
	re_path('create_team', api.views.create_team),
	re_path('update_team/<int:pk>', api.views.update_team),
	re_path('delete_team/<int:pk>', api.views.delete_team),

	# Players
	re_path('list_players', api.views.list_players),
	re_path('get_player/<int:pk>', api.views.get_player),
	re_path('create_player', api.views.create_player),
	re_path('update_player/<int:pk>', api.views.update_player),
	re_path('delete_player/<int:pk>', api.views.delete_player),

	# Game
	re_path('list_games', api.views.list_games),
	re_path('get_game/<int:pk>', api.views.get_game),
	re_path('create_game', api.views.create_game),
	re_path('update_game/<int:pk>', api.views.update_game),
	re_path('delete_game/<int:pk>', api.views.delete_game),

	# Matches
	re_path('list_matches', api.views.list_matches),
	re_path('get_match/<int:pk>', api.views.get_match),
	re_path('create_match', api.views.create_match),
	re_path('update_match/<int:pk>', api.views.update_match),
	re_path('delete_match/<int:pk>', api.views.delete_match),
]

