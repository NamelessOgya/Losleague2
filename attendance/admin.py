
from django.contrib import admin
from .models import Team, Player, Match, Registered, Table, Reported, PlayerResult, TeamResult, ClassWinRate, Blog, Season, Tournament, Past, JCGrank,Other_tournament
# Register your models here.
class PlayerAdmin(admin.ModelAdmin):
    list_filter = ["team"]
class ReportedAdmin(admin.ModelAdmin):
    list_filter = ["date", "team"]

class RegisteredAdmin(admin.ModelAdmin):
    list_filter = ["date", "team"]

class TableAdmin(admin.ModelAdmin):
    list_filter = ["date"]

class PlayerResultAdmin(admin.ModelAdmin):
    list_filter = ["date","player", "leader", "wl"]


class PlayerAdmin(admin.ModelAdmin):
    list_filter = ["win","team"]
class Other_tournamentAdmin(admin.ModelAdmin):
    list_filter = ["tournament"]

class JCGrankAdmin(admin.ModelAdmin):
    list_display = ["JCGID", "player_name", "first", "second", "fourth", "total"]
    ordering = ['JCGID']
    search_fields = ["JCGID", "player_name"]


admin.site.register(Team)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Match)
admin.site.register(Registered, RegisteredAdmin)
admin.site.register(Table, TableAdmin)
admin.site.register(Reported, ReportedAdmin)
admin.site.register(PlayerResult, PlayerResultAdmin)
admin.site.register(TeamResult)
admin.site.register(ClassWinRate)
admin.site.register(Blog)
admin.site.register(Season)
admin.site.register(Tournament)
admin.site.register(Past)
admin.site.register(JCGrank,JCGrankAdmin )
admin.site.register(Other_tournament)



