from django.contrib import admin
from .models import AppUser, Competition, CompetitionTeams, CompetitionTeamstudents, Teams, Students, StaticQuestion


class StaticQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'field_name', 'max_score', 'category')


admin.site.register(AppUser)
admin.site.register(Teams)
admin.site.register(Students)
admin.site.register(Competition)
admin.site.register(CompetitionTeams)
admin.site.register(CompetitionTeamstudents)
admin.site.register(StaticQuestion, StaticQuestionAdmin)
