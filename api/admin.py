from django.contrib import admin

from .models import League, Team, Match, Player

admin.site.register([League, Team, Match, Player])