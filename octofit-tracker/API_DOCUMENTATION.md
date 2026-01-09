# OctoFit Tracker API Documentation

## Base URL
- Development: `http://localhost:8000/api/`
- Production: Update based on deployment

## Authentication

All authenticated endpoints require a token in the Authorization header:
```
Authorization: Token <your-token-here>
```

## API Root

### Get API Information
```
GET /api/
```

Returns information about available endpoints.

**Response:**
```json
{
  "message": "Welcome to OctoFit Tracker API",
  "endpoints": {
    "profiles": "/api/profiles/",
    "activities": "/api/activities/",
    "teams": "/api/teams/",
    "leaderboard": "/api/leaderboard/",
    "auth": { ... }
  }
}
```

## Authentication Endpoints

### Register
```
POST /api/auth/registration/
Content-Type: application/json

{
  "username": "newuser",
  "email": "user@example.com",
  "password1": "securepass123",
  "password2": "securepass123"
}
```

**Response:**
```json
{
  "key": "token-string-here"
}
```

### Login
```
POST /api/auth/login/
Content-Type: application/json

{
  "username": "john_runner",
  "password": "testpass123"
}
```

**Response:**
```json
{
  "key": "token-string-here"
}
```

### Logout
```
POST /api/auth/logout/
Authorization: Token <your-token>
```

### Get Current User
```
GET /api/auth/user/
Authorization: Token <your-token>
```

**Response:**
```json
{
  "pk": 1,
  "username": "john_runner",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

## Profile Endpoints

### Get My Profile
```
GET /api/profiles/me/
Authorization: Token <your-token>
```

**Response:**
```json
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "john_runner",
    "email": "john@example.com"
  },
  "username": "john_runner",
  "bio": "",
  "height": 180.0,
  "weight": 75.0,
  "fitness_level": "advanced",
  "fitness_goals": "Complete a marathon",
  "total_points": 180,
  "created_at": "2026-01-09T07:59:00Z",
  "updated_at": "2026-01-09T08:00:00Z"
}
```

### Update Profile
```
PATCH /api/profiles/{id}/
Authorization: Token <your-token>
Content-Type: application/json

{
  "height": 182,
  "weight": 76,
  "fitness_level": "advanced",
  "fitness_goals": "Run a sub-4-hour marathon"
}
```

## Activity Endpoints

### List My Activities
```
GET /api/activities/my_activities/
Authorization: Token <your-token>
```

**Response:**
```json
[
  {
    "id": 1,
    "user": 1,
    "username": "john_runner",
    "activity_type": "running",
    "duration": 45,
    "distance": 8.5,
    "calories_burned": null,
    "intensity": "high",
    "notes": "",
    "points_earned": 90,
    "date_performed": "2026-01-08",
    "created_at": "2026-01-09T08:00:00Z"
  }
]
```

### Create Activity
```
POST /api/activities/
Authorization: Token <your-token>
Content-Type: application/json

{
  "activity_type": "running",
  "duration": 60,
  "distance": 10,
  "intensity": "moderate",
  "date_performed": "2026-01-09",
  "notes": "Great morning run"
}
```

**Response:**
```json
{
  "id": 3,
  "user": 1,
  "username": "john_runner",
  "activity_type": "running",
  "duration": 60,
  "distance": 10.0,
  "intensity": "moderate",
  "notes": "Great morning run",
  "points_earned": 90,
  "date_performed": "2026-01-09",
  "created_at": "2026-01-09T08:30:00Z"
}
```

### Get Activity Statistics
```
GET /api/activities/statistics/
Authorization: Token <your-token>
```

**Response:**
```json
{
  "total_activities": 2,
  "total_duration": 105,
  "total_distance": 20.5,
  "total_points": 180,
  "activity_breakdown": {
    "running": 2
  }
}
```

## Team Endpoints

### List All Teams
```
GET /api/teams/
Authorization: Token <your-token>
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Morning Runners",
    "description": "Team for early morning running enthusiasts",
    "creator": 1,
    "creator_username": "john_runner",
    "members": [
      {
        "id": 1,
        "username": "john_runner",
        "total_points": 180
      }
    ],
    "member_count": 3,
    "total_points": 405,
    "created_at": "2026-01-09T08:00:00Z"
  }
]
```

### Create Team
```
POST /api/teams/
Authorization: Token <your-token>
Content-Type: application/json

{
  "name": "Evening Warriors",
  "description": "Training hard after work"
}
```

### Join Team
```
POST /api/teams/{id}/join/
Authorization: Token <your-token>
```

**Response:**
```json
{
  "detail": "Successfully joined the team."
}
```

### Leave Team
```
POST /api/teams/{id}/leave/
Authorization: Token <your-token>
```

**Response:**
```json
{
  "detail": "Successfully left the team."
}
```

### Get My Teams
```
GET /api/teams/my_teams/
Authorization: Token <your-token>
```

## Leaderboard Endpoints

### User Leaderboard
```
GET /api/leaderboard/
```

**Response:**
```json
[
  {
    "rank": 1,
    "username": "mike_athlete",
    "total_points": 345,
    "activity_count": 2
  },
  {
    "rank": 2,
    "username": "john_runner",
    "total_points": 180,
    "activity_count": 2
  }
]
```

### Team Leaderboard
```
GET /api/team-leaderboard/
```

**Response:**
```json
[
  {
    "rank": 1,
    "name": "Fitness Warriors",
    "total_points": 750,
    "member_count": 4
  }
]
```

## Workout Suggestion Endpoints

### List My Suggestions
```
GET /api/workout-suggestions/
Authorization: Token <your-token>
```

**Response:**
```json
[
  {
    "id": 1,
    "user": 1,
    "username": "john_runner",
    "title": "10K Training Run",
    "description": "Build endurance with a 10K run",
    "activity_type": "running",
    "recommended_duration": 50,
    "recommended_intensity": "moderate",
    "fitness_level": "advanced",
    "completed": false,
    "completed_at": null,
    "created_at": "2026-01-09T08:00:00Z"
  }
]
```

### Generate Suggestions
```
POST /api/workout-suggestions/generate/
Authorization: Token <your-token>
```

Generates personalized workout suggestions based on the user's fitness level.

### Mark Suggestion as Completed
```
POST /api/workout-suggestions/{id}/mark_completed/
Authorization: Token <your-token>
```

**Response:**
```json
{
  "detail": "Workout marked as completed."
}
```

## Achievement Endpoints

### List My Achievements
```
GET /api/achievements/
Authorization: Token <your-token>
```

**Response:**
```json
[
  {
    "id": 1,
    "user": 1,
    "username": "john_runner",
    "title": "First Activity",
    "description": "Completed your first workout",
    "badge_type": "first_activity",
    "earned_at": "2026-01-09T08:00:00Z"
  }
]
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Error message explaining what went wrong"
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

## Activity Types
- `running`
- `walking`
- `cycling`
- `swimming`
- `strength_training`
- `yoga`
- `cardio`
- `sports`
- `other`

## Intensity Levels
- `low` (multiplier: 1x)
- `moderate` (multiplier: 1.5x)
- `high` (multiplier: 2x)
- `extreme` (multiplier: 2.5x)

## Fitness Levels
- `beginner`
- `intermediate`
- `advanced`
- `expert`

## Points Calculation

Points are automatically calculated when creating an activity:
```
points = duration (minutes) × intensity_multiplier
```

Example:
- 60 minutes of moderate intensity = 60 × 1.5 = 90 points
- 45 minutes of high intensity = 45 × 2 = 90 points

## Rate Limiting

Currently, there are no rate limits on the API. For production deployment, consider implementing rate limiting using Django REST Framework throttling.

## Pagination

List endpoints support pagination:
- Default page size: 30 items (varies by endpoint)
- Maximum page size: 100 items

## CORS

The API supports CORS for the following origins:
- `http://localhost:3000` (development)
- `http://127.0.0.1:3000` (development)
- GitHub Codespaces URLs (automatically configured)

## Testing the API

### Using cURL

**Login:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john_runner", "password": "testpass123"}'
```

**Get Leaderboard:**
```bash
curl http://localhost:8000/api/leaderboard/
```

**Create Activity (authenticated):**
```bash
curl -X POST http://localhost:8000/api/activities/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -d '{
    "activity_type": "running",
    "duration": 30,
    "distance": 5,
    "intensity": "moderate",
    "date_performed": "2026-01-09"
  }'
```

### Using Postman

1. Import the API endpoints
2. Set up an environment variable for the token
3. Add the Authorization header to authenticated requests

### Using the Admin Interface

Access the Django admin at `http://localhost:8000/admin/` using the admin credentials:
- Username: `admin`
- Password: `admin123`

The admin interface provides a web UI to manage all data models.
