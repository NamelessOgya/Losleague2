
from django.contrib import admin
from .models import Team, Player, Match, Registered, Table, Reported, PlayerResult, TeamResult, ClassWinRate, Blog, Season
# Register your models here.
class PlayerAdmin(admin.ModelAdmin):
    list_filter = ["team", "season"]
class ReportedAdmin(admin.ModelAdmin):
    list_filter = ["date", "team"]



admin.site.register(Team)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Match)
admin.site.register(Registered)
admin.site.register(Table)
admin.site.register(Reported, ReportedAdmin)
admin.site.register(PlayerResult)
admin.site.register(TeamResult)
admin.site.register(ClassWinRate)
admin.site.register(Blog)
admin.site.register(Season)



