from django.contrib import admin
from .models import UserProfile, Activity, Team, WorkoutSuggestion, Achievement

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'fitness_level', 'total_points', 'created_at']
    list_filter = ['fitness_level', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['total_points', 'created_at', 'updated_at']

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'duration', 'intensity', 'points_earned', 'date_performed']
    list_filter = ['activity_type', 'intensity', 'date_performed']
    search_fields = ['user__username', 'notes']
    readonly_fields = ['points_earned', 'created_at']
    date_hierarchy = 'date_performed'

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'creator', 'total_points', 'member_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description', 'creator__username']
    readonly_fields = ['total_points', 'created_at', 'updated_at']
    filter_horizontal = ['members']
    
    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'Members'

@admin.register(WorkoutSuggestion)
class WorkoutSuggestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'activity_type', 'fitness_level', 'completed', 'created_at']
    list_filter = ['activity_type', 'fitness_level', 'completed', 'recommended_intensity']
    search_fields = ['title', 'description', 'user__username']
    readonly_fields = ['created_at']

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'badge_type', 'earned_at']
    list_filter = ['badge_type', 'earned_at']
    search_fields = ['title', 'user__username']
    readonly_fields = ['earned_at']

