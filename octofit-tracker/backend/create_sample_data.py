"""
Script to create sample data for OctoFit Tracker
"""
import os
import django
import sys
from datetime import date, timedelta

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'octofit_tracker.settings')
django.setup()

from django.contrib.auth.models import User
from fitness.models import UserProfile, Activity, Team, WorkoutSuggestion, Achievement

# Create users
users_data = [
    {'username': 'john_runner', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe', 'password': 'testpass123'},
    {'username': 'jane_fitness', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith', 'password': 'testpass123'},
    {'username': 'mike_athlete', 'email': 'mike@example.com', 'first_name': 'Mike', 'last_name': 'Johnson', 'password': 'testpass123'},
    {'username': 'sarah_yoga', 'email': 'sarah@example.com', 'first_name': 'Sarah', 'last_name': 'Williams', 'password': 'testpass123'},
]

print("Creating users...")
users = []
for user_data in users_data:
    user, created = User.objects.get_or_create(
        username=user_data['username'],
        defaults={
            'email': user_data['email'],
            'first_name': user_data['first_name'],
            'last_name': user_data['last_name'],
        }
    )
    if created:
        user.set_password(user_data['password'])
        user.save()
        print(f"  Created user: {user.username}")
    users.append(user)

# Update user profiles
profiles_data = [
    {'fitness_level': 'advanced', 'height': 180, 'weight': 75, 'fitness_goals': 'Complete a marathon'},
    {'fitness_level': 'intermediate', 'height': 165, 'weight': 60, 'fitness_goals': 'Improve overall fitness'},
    {'fitness_level': 'expert', 'height': 185, 'weight': 85, 'fitness_goals': 'Train for triathlon'},
    {'fitness_level': 'beginner', 'height': 170, 'weight': 65, 'fitness_goals': 'Start yoga practice'},
]

print("\nUpdating user profiles...")
for user, profile_data in zip(users, profiles_data):
    profile = user.profile
    for key, value in profile_data.items():
        setattr(profile, key, value)
    profile.save()
    print(f"  Updated profile for: {user.username}")

# Create activities
print("\nCreating activities...")
activities_data = [
    {'user': users[0], 'activity_type': 'running', 'duration': 45, 'distance': 8.5, 'intensity': 'high', 'date_performed': date.today() - timedelta(days=1)},
    {'user': users[0], 'activity_type': 'running', 'duration': 60, 'distance': 12, 'intensity': 'moderate', 'date_performed': date.today() - timedelta(days=3)},
    {'user': users[1], 'activity_type': 'strength_training', 'duration': 50, 'intensity': 'moderate', 'date_performed': date.today()},
    {'user': users[1], 'activity_type': 'cycling', 'duration': 40, 'distance': 15, 'intensity': 'moderate', 'date_performed': date.today() - timedelta(days=2)},
    {'user': users[2], 'activity_type': 'swimming', 'duration': 60, 'distance': 2, 'intensity': 'high', 'date_performed': date.today() - timedelta(days=1)},
    {'user': users[2], 'activity_type': 'strength_training', 'duration': 90, 'intensity': 'extreme', 'date_performed': date.today()},
    {'user': users[3], 'activity_type': 'yoga', 'duration': 60, 'intensity': 'low', 'date_performed': date.today()},
    {'user': users[3], 'activity_type': 'walking', 'duration': 30, 'distance': 3, 'intensity': 'low', 'date_performed': date.today() - timedelta(days=1)},
]

for activity_data in activities_data:
    activity, created = Activity.objects.get_or_create(
        user=activity_data['user'],
        activity_type=activity_data['activity_type'],
        date_performed=activity_data['date_performed'],
        defaults=activity_data
    )
    if created:
        print(f"  Created activity: {activity.activity_type} for {activity.user.username}")

# Create teams
print("\nCreating teams...")
teams_data = [
    {'name': 'Morning Runners', 'description': 'Team for early morning running enthusiasts', 'creator': users[0]},
    {'name': 'Strength Squad', 'description': 'Building strength together', 'creator': users[1]},
    {'name': 'Fitness Warriors', 'description': 'Hardcore fitness training group', 'creator': users[2]},
]

teams = []
for team_data in teams_data:
    team, created = Team.objects.get_or_create(
        name=team_data['name'],
        defaults=team_data
    )
    if created:
        # Add creator as member
        team.members.add(team_data['creator'])
        print(f"  Created team: {team.name}")
    teams.append(team)

# Add members to teams
print("\nAdding members to teams...")
teams[0].members.add(users[1], users[3])
teams[1].members.add(users[0], users[2])
teams[2].members.add(users[0], users[1], users[3])

for team in teams:
    team.update_total_points()
    print(f"  Team '{team.name}' has {team.members.count()} members")

# Create workout suggestions
print("\nCreating workout suggestions...")
suggestions_data = [
    {'user': users[0], 'title': '10K Training Run', 'description': 'Build endurance with a 10K run', 
     'activity_type': 'running', 'recommended_duration': 50, 'recommended_intensity': 'moderate', 'fitness_level': 'advanced'},
    {'user': users[1], 'title': 'Full Body Strength', 'description': 'Complete body workout with weights',
     'activity_type': 'strength_training', 'recommended_duration': 45, 'recommended_intensity': 'moderate', 'fitness_level': 'intermediate'},
    {'user': users[2], 'title': 'Triathlon Training', 'description': 'Combined swim, bike, run session',
     'activity_type': 'sports', 'recommended_duration': 120, 'recommended_intensity': 'extreme', 'fitness_level': 'expert'},
    {'user': users[3], 'title': 'Beginner Yoga Flow', 'description': 'Gentle yoga for beginners',
     'activity_type': 'yoga', 'recommended_duration': 30, 'recommended_intensity': 'low', 'fitness_level': 'beginner'},
]

for suggestion_data in suggestions_data:
    suggestion, created = WorkoutSuggestion.objects.get_or_create(
        user=suggestion_data['user'],
        title=suggestion_data['title'],
        defaults=suggestion_data
    )
    if created:
        print(f"  Created suggestion: {suggestion.title} for {suggestion.user.username}")

# Create achievements
print("\nCreating achievements...")
achievements_data = [
    {'user': users[0], 'title': 'First Activity', 'description': 'Completed your first workout', 'badge_type': 'first_activity'},
    {'user': users[0], 'title': '100 Points', 'description': 'Earned 100 fitness points', 'badge_type': 'points_100'},
    {'user': users[1], 'title': 'First Activity', 'description': 'Completed your first workout', 'badge_type': 'first_activity'},
    {'user': users[2], 'title': 'First Activity', 'description': 'Completed your first workout', 'badge_type': 'first_activity'},
    {'user': users[2], 'title': '500 Points', 'description': 'Earned 500 fitness points', 'badge_type': 'points_500'},
]

for achievement_data in achievements_data:
    achievement, created = Achievement.objects.get_or_create(
        user=achievement_data['user'],
        badge_type=achievement_data['badge_type'],
        defaults=achievement_data
    )
    if created:
        print(f"  Created achievement: {achievement.title} for {achievement.user.username}")

# Create superuser
print("\nCreating superuser 'admin'...")
admin_user, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@example.com',
        'is_staff': True,
        'is_superuser': True,
    }
)
if created:
    admin_user.set_password('admin123')
    admin_user.save()
    print("  Superuser created: admin / admin123")
else:
    print("  Superuser already exists")

print("\n✅ Sample data created successfully!")
print("\nTest users:")
for user_data in users_data:
    print(f"  Username: {user_data['username']}, Password: testpass123")
print("\nAdmin user:")
print("  Username: admin, Password: admin123")
