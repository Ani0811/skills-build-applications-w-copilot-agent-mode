from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'profiles', views.UserProfileViewSet)
router.register(r'activities', views.ActivityViewSet)
router.register(r'teams', views.TeamViewSet)
router.register(r'workout-suggestions', views.WorkoutSuggestionViewSet)
router.register(r'achievements', views.AchievementViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('team-leaderboard/', views.team_leaderboard, name='team-leaderboard'),
]
