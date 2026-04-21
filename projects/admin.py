from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'project_lead', 'created_at')
    list_filter = ('status',)
    search_fields = ('title', 'description')
    filter_horizontal = ('team_members',)
