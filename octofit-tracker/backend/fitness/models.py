from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# User Profile Model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    height = models.FloatField(null=True, blank=True, help_text='Height in cm')
    weight = models.FloatField(null=True, blank=True, help_text='Weight in kg')
    fitness_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
            ('expert', 'Expert'),
        ],
        default='beginner'
    )
    fitness_goals = models.TextField(blank=True, null=True)
    total_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        ordering = ['-total_points']

# Auto-create profile when user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# Activity Model
class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(
        max_length=50,
        choices=[
            ('running', 'Running'),
            ('walking', 'Walking'),
            ('cycling', 'Cycling'),
            ('swimming', 'Swimming'),
            ('strength_training', 'Strength Training'),
            ('yoga', 'Yoga'),
            ('cardio', 'Cardio'),
            ('sports', 'Sports'),
            ('other', 'Other'),
        ]
    )
    duration = models.IntegerField(help_text='Duration in minutes')
    distance = models.FloatField(null=True, blank=True, help_text='Distance in km')
    calories_burned = models.IntegerField(null=True, blank=True)
    intensity = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('moderate', 'Moderate'),
            ('high', 'High'),
            ('extreme', 'Extreme'),
        ],
        default='moderate'
    )
    notes = models.TextField(blank=True, null=True)
    points_earned = models.IntegerField(default=0)
    date_performed = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calculate points based on duration and intensity
        intensity_multipliers = {
            'low': 1,
            'moderate': 1.5,
            'high': 2,
            'extreme': 2.5,
        }
        self.points_earned = int(self.duration * intensity_multipliers.get(self.intensity, 1))
        
        # Update user's total points
        if self.pk is None:  # Only on creation
            self.user.profile.total_points += self.points_earned
            self.user.profile.save()
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} on {self.date_performed}"

    class Meta:
        ordering = ['-date_performed', '-created_at']
        verbose_name_plural = 'Activities'

# Team Model
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_teams')
    members = models.ManyToManyField(User, related_name='teams', blank=True)
    total_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_total_points(self):
        """Calculate total points from all team members"""
        total = sum(member.profile.total_points for member in self.members.all())
        self.total_points = total
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-total_points']

# Workout Suggestion Model
class WorkoutSuggestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workout_suggestions')
    title = models.CharField(max_length=200)
    description = models.TextField()
    activity_type = models.CharField(
        max_length=50,
        choices=[
            ('running', 'Running'),
            ('walking', 'Walking'),
            ('cycling', 'Cycling'),
            ('swimming', 'Swimming'),
            ('strength_training', 'Strength Training'),
            ('yoga', 'Yoga'),
            ('cardio', 'Cardio'),
            ('sports', 'Sports'),
            ('other', 'Other'),
        ]
    )
    recommended_duration = models.IntegerField(help_text='Duration in minutes')
    recommended_intensity = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('moderate', 'Moderate'),
            ('high', 'High'),
            ('extreme', 'Extreme'),
        ]
    )
    fitness_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
            ('expert', 'Expert'),
        ]
    )
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} for {self.user.username}"

    class Meta:
        ordering = ['-created_at']

# Achievement/Badge Model
class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=100)
    description = models.TextField()
    badge_type = models.CharField(
        max_length=50,
        choices=[
            ('first_activity', 'First Activity'),
            ('streak_7', '7 Day Streak'),
            ('streak_30', '30 Day Streak'),
            ('points_100', '100 Points'),
            ('points_500', '500 Points'),
            ('points_1000', '1000 Points'),
            ('distance_10k', '10km Distance'),
            ('distance_50k', '50km Distance'),
            ('team_member', 'Team Member'),
            ('team_leader', 'Team Leader'),
        ]
    )
    earned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    class Meta:
        ordering = ['-earned_at']
