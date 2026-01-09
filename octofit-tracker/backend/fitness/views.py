from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from datetime import datetime, timedelta
from .models import UserProfile, Activity, Team, WorkoutSuggestion, Achievement
from .serializers import (
    UserSerializer, UserProfileSerializer, ActivitySerializer,
    TeamSerializer, WorkoutSuggestionSerializer, AchievementSerializer,
    LeaderboardSerializer, TeamLeaderboardSerializer
)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Users can only see their own profile unless they're staff
        if self.request.user.is_staff:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's profile"""
        serializer = self.get_serializer(request.user.profile)
        return Response(serializer.data)

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Users can only see their own activities unless they're staff
        if self.request.user.is_staff:
            return Activity.objects.all()
        return Activity.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_activities(self, request):
        """Get current user's activities"""
        activities = Activity.objects.filter(user=request.user)
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get activity statistics for current user"""
        activities = Activity.objects.filter(user=request.user)
        
        stats = {
            'total_activities': activities.count(),
            'total_duration': activities.aggregate(Sum('duration'))['duration__sum'] or 0,
            'total_distance': activities.aggregate(Sum('distance'))['distance__sum'] or 0,
            'total_points': request.user.profile.total_points,
            'activity_breakdown': dict(activities.values('activity_type').annotate(count=Count('id')).values_list('activity_type', 'count')),
        }
        return Response(stats)

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        """Join a team"""
        team = self.get_object()
        if request.user in team.members.all():
            return Response(
                {'detail': 'You are already a member of this team.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        team.members.add(request.user)
        team.update_total_points()
        return Response({'detail': 'Successfully joined the team.'})
    
    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        """Leave a team"""
        team = self.get_object()
        if request.user not in team.members.all():
            return Response(
                {'detail': 'You are not a member of this team.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if team.creator == request.user:
            return Response(
                {'detail': 'Team creator cannot leave the team. Delete the team instead.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        team.members.remove(request.user)
        team.update_total_points()
        return Response({'detail': 'Successfully left the team.'})
    
    @action(detail=False, methods=['get'])
    def my_teams(self, request):
        """Get teams current user is a member of"""
        teams = Team.objects.filter(members=request.user)
        serializer = self.get_serializer(teams, many=True)
        return Response(serializer.data)

class WorkoutSuggestionViewSet(viewsets.ModelViewSet):
    queryset = WorkoutSuggestion.objects.all()
    serializer_class = WorkoutSuggestionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Users can only see their own suggestions unless they're staff
        if self.request.user.is_staff:
            return WorkoutSuggestion.objects.all()
        return WorkoutSuggestion.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        """Mark a workout suggestion as completed"""
        suggestion = self.get_object()
        suggestion.completed = True
        suggestion.completed_at = datetime.now()
        suggestion.save()
        return Response({'detail': 'Workout marked as completed.'})
    
    @action(detail=False, methods=['post'])
    def generate(self, request):
        """Generate personalized workout suggestions based on user's fitness level"""
        user = request.user
        profile = user.profile
        
        suggestions_data = {
            'beginner': [
                {'title': 'Morning Walk', 'description': 'Start your day with a light 20-minute walk', 
                 'activity_type': 'walking', 'recommended_duration': 20, 'recommended_intensity': 'low'},
                {'title': 'Basic Stretching', 'description': 'Gentle stretching routine for flexibility',
                 'activity_type': 'yoga', 'recommended_duration': 15, 'recommended_intensity': 'low'},
            ],
            'intermediate': [
                {'title': 'Interval Running', 'description': '30 minutes of alternating running and jogging',
                 'activity_type': 'running', 'recommended_duration': 30, 'recommended_intensity': 'moderate'},
                {'title': 'Strength Circuit', 'description': 'Full body strength training circuit',
                 'activity_type': 'strength_training', 'recommended_duration': 45, 'recommended_intensity': 'moderate'},
            ],
            'advanced': [
                {'title': 'High Intensity Run', 'description': 'Challenging 45-minute run with hills',
                 'activity_type': 'running', 'recommended_duration': 45, 'recommended_intensity': 'high'},
                {'title': 'Advanced Strength', 'description': 'Advanced strength training with heavy weights',
                 'activity_type': 'strength_training', 'recommended_duration': 60, 'recommended_intensity': 'high'},
            ],
            'expert': [
                {'title': 'Elite Training', 'description': 'Extreme endurance and strength workout',
                 'activity_type': 'cardio', 'recommended_duration': 90, 'recommended_intensity': 'extreme'},
                {'title': 'Competition Prep', 'description': 'High-intensity training for competition',
                 'activity_type': 'sports', 'recommended_duration': 120, 'recommended_intensity': 'extreme'},
            ],
        }
        
        suggestions = suggestions_data.get(profile.fitness_level, suggestions_data['beginner'])
        created_suggestions = []
        
        for suggestion_data in suggestions:
            suggestion = WorkoutSuggestion.objects.create(
                user=user,
                fitness_level=profile.fitness_level,
                **suggestion_data
            )
            created_suggestions.append(suggestion)
        
        serializer = self.get_serializer(created_suggestions, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class AchievementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Users can only see their own achievements unless they're staff
        if self.request.user.is_staff:
            return Achievement.objects.all()
        return Achievement.objects.filter(user=self.request.user)

@api_view(['GET'])
@permission_classes([AllowAny])
def leaderboard(request):
    """Get user leaderboard"""
    profiles = UserProfile.objects.select_related('user').order_by('-total_points')[:50]
    
    leaderboard_data = []
    for rank, profile in enumerate(profiles, start=1):
        activity_count = Activity.objects.filter(user=profile.user).count()
        leaderboard_data.append({
            'rank': rank,
            'username': profile.user.username,
            'total_points': profile.total_points,
            'activity_count': activity_count,
        })
    
    serializer = LeaderboardSerializer(leaderboard_data, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def team_leaderboard(request):
    """Get team leaderboard"""
    teams = Team.objects.all().order_by('-total_points')[:50]
    
    leaderboard_data = []
    for rank, team in enumerate(teams, start=1):
        leaderboard_data.append({
            'rank': rank,
            'name': team.name,
            'total_points': team.total_points,
            'member_count': team.members.count(),
        })
    
    serializer = TeamLeaderboardSerializer(leaderboard_data, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """API root endpoint with available endpoints"""
    return Response({
        'message': 'Welcome to OctoFit Tracker API',
        'endpoints': {
            'profiles': '/api/profiles/',
            'profile_me': '/api/profiles/me/',
            'activities': '/api/activities/',
            'my_activities': '/api/activities/my_activities/',
            'activity_statistics': '/api/activities/statistics/',
            'teams': '/api/teams/',
            'my_teams': '/api/teams/my_teams/',
            'workout_suggestions': '/api/workout-suggestions/',
            'generate_suggestions': '/api/workout-suggestions/generate/',
            'achievements': '/api/achievements/',
            'leaderboard': '/api/leaderboard/',
            'team_leaderboard': '/api/team-leaderboard/',
            'auth': {
                'login': '/api/auth/login/',
                'logout': '/api/auth/logout/',
                'register': '/api/auth/registration/',
                'user': '/api/auth/user/',
            }
        }
    })

