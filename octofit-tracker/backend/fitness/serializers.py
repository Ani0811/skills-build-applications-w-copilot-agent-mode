from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Activity, Team, WorkoutSuggestion, Achievement

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'username', 'bio', 'height', 'weight',
            'fitness_level', 'fitness_goals', 'total_points',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'total_points', 'created_at', 'updated_at']

class ActivitySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Activity
        fields = [
            'id', 'user', 'username', 'activity_type', 'duration',
            'distance', 'calories_burned', 'intensity', 'notes',
            'points_earned', 'date_performed', 'created_at'
        ]
        read_only_fields = ['id', 'points_earned', 'created_at']
    
    def create(self, validated_data):
        # Set the user from the request context
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class TeamMemberSerializer(serializers.ModelSerializer):
    total_points = serializers.IntegerField(source='profile.total_points', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'total_points']

class TeamSerializer(serializers.ModelSerializer):
    creator_username = serializers.CharField(source='creator.username', read_only=True)
    members = TeamMemberSerializer(many=True, read_only=True)
    member_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = [
            'id', 'name', 'description', 'creator', 'creator_username',
            'members', 'member_count', 'total_points', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'total_points', 'created_at', 'updated_at']
    
    def get_member_count(self, obj):
        return obj.members.count()
    
    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        team = super().create(validated_data)
        # Auto-add creator as member
        team.members.add(self.context['request'].user)
        team.update_total_points()
        return team

class WorkoutSuggestionSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = WorkoutSuggestion
        fields = [
            'id', 'user', 'username', 'title', 'description',
            'activity_type', 'recommended_duration', 'recommended_intensity',
            'fitness_level', 'completed', 'completed_at', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

class AchievementSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Achievement
        fields = [
            'id', 'user', 'username', 'title', 'description',
            'badge_type', 'earned_at'
        ]
        read_only_fields = ['id', 'earned_at']

class LeaderboardSerializer(serializers.Serializer):
    """Serializer for leaderboard rankings"""
    rank = serializers.IntegerField()
    username = serializers.CharField()
    total_points = serializers.IntegerField()
    activity_count = serializers.IntegerField()
    
class TeamLeaderboardSerializer(serializers.Serializer):
    """Serializer for team leaderboard rankings"""
    rank = serializers.IntegerField()
    name = serializers.CharField()
    total_points = serializers.IntegerField()
    member_count = serializers.IntegerField()
