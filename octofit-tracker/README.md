# OctoFit Tracker - Gym SaaS Application

![OctoFit Tracker](docs/octofitapp-small.png)

A comprehensive gym SaaS platform for managing customer training progress, built with Django REST Framework and React.

## 🎯 Features

### User Management
- **User Authentication**: Secure token-based authentication
- **User Profiles**: Track fitness level, goals, physical stats
- **Points System**: Earn points for completed activities

### Activity Tracking
- **Log Workouts**: Record activities with type, duration, distance, intensity
- **Activity Types**: Running, walking, cycling, swimming, strength training, yoga, cardio, sports
- **Automatic Points**: Points calculated based on duration and intensity
- **Activity History**: View all your past workouts

### Team Management
- **Create Teams**: Start your own fitness team
- **Join Teams**: Become a member of existing teams
- **Team Points**: Collective points from all team members
- **Team Competitions**: Compete with other teams on the leaderboard

### Leaderboards
- **User Rankings**: Individual leaderboard with points and activity counts
- **Team Rankings**: Team leaderboard based on collective points
- **Medal System**: Top 3 users/teams get gold, silver, bronze medals

### Workout Suggestions
- **Personalized Recommendations**: Get workout suggestions based on your fitness level
- **Multiple Fitness Levels**: Beginner, Intermediate, Advanced, Expert
- **Track Completion**: Mark suggested workouts as completed

### Achievements
- **Badge System**: Earn badges for milestones
- **Achievement Types**: First activity, point milestones, distance goals, streaks

## 🛠️ Tech Stack

### Backend
- Python 3.12
- Django 4.2.26 (LTS with security patches)
- Django REST Framework 3.14.0
- SQLite (can be switched to PostgreSQL or MySQL)
- dj-rest-auth for authentication
- django-cors-headers for CORS support

### Frontend
- React 18
- Bootstrap 5
- React Router DOM
- Fetch API for backend communication

## 📦 Installation

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd octofit-tracker/backend
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create sample data (optional):
```bash
python create_sample_data.py
```

6. Start the development server:
```bash
python manage.py runserver 0.0.0.0:8000
```

The backend API will be available at `http://localhost:8000/api/`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd octofit-tracker/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## 👤 Demo Credentials

After running `create_sample_data.py`, you can use these credentials:

| Username | Password | Description |
|----------|----------|-------------|
| john_runner | testpass123 | Advanced runner |
| jane_fitness | testpass123 | Intermediate fitness enthusiast |
| mike_athlete | testpass123 | Expert athlete |
| sarah_yoga | testpass123 | Beginner yoga practitioner |
| admin | admin123 | Admin user |

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/registration/` - User registration
- `GET /api/auth/user/` - Get current user

### Profiles
- `GET /api/profiles/` - List all profiles
- `GET /api/profiles/me/` - Get current user's profile
- `GET /api/profiles/{id}/` - Get specific profile
- `PUT /api/profiles/{id}/` - Update profile
- `PATCH /api/profiles/{id}/` - Partial update profile

### Activities
- `GET /api/activities/` - List all activities
- `POST /api/activities/` - Create new activity
- `GET /api/activities/my_activities/` - Get current user's activities
- `GET /api/activities/statistics/` - Get activity statistics
- `GET /api/activities/{id}/` - Get specific activity
- `PUT /api/activities/{id}/` - Update activity
- `DELETE /api/activities/{id}/` - Delete activity

### Teams
- `GET /api/teams/` - List all teams
- `POST /api/teams/` - Create new team
- `GET /api/teams/my_teams/` - Get current user's teams
- `GET /api/teams/{id}/` - Get specific team
- `POST /api/teams/{id}/join/` - Join a team
- `POST /api/teams/{id}/leave/` - Leave a team
- `PUT /api/teams/{id}/` - Update team
- `DELETE /api/teams/{id}/` - Delete team

### Leaderboards
- `GET /api/leaderboard/` - Get user leaderboard (top 50)
- `GET /api/team-leaderboard/` - Get team leaderboard (top 50)

### Workout Suggestions
- `GET /api/workout-suggestions/` - List workout suggestions
- `POST /api/workout-suggestions/generate/` - Generate personalized suggestions
- `POST /api/workout-suggestions/{id}/mark_completed/` - Mark suggestion as completed
- `GET /api/workout-suggestions/{id}/` - Get specific suggestion

### Achievements
- `GET /api/achievements/` - List achievements

## 📱 Application Structure

```
octofit-tracker/
├── backend/
│   ├── octofit_tracker/          # Django project settings
│   │   ├── settings.py            # Project configuration
│   │   ├── urls.py                # Main URL routing
│   │   └── wsgi.py                # WSGI configuration
│   ├── fitness/                   # Main fitness app
│   │   ├── models.py              # Database models
│   │   ├── serializers.py         # DRF serializers
│   │   ├── views.py               # API views
│   │   ├── urls.py                # App URL routing
│   │   └── admin.py               # Admin configuration
│   ├── manage.py                  # Django management script
│   ├── requirements.txt           # Python dependencies
│   └── create_sample_data.py      # Sample data creation script
└── frontend/
    ├── src/
    │   ├── App.js                 # Main React component
    │   ├── App.css                # Application styles
    │   ├── index.js               # React entry point
    │   └── octofitapp-small.png   # Application logo
    ├── public/                    # Static files
    ├── package.json               # Node dependencies
    └── README.md                  # Frontend documentation
```

## 🎨 Key Components

### Backend Models

1. **UserProfile**: Extended user information with fitness data
2. **Activity**: Workout logging with automatic point calculation
3. **Team**: Team management with collective points
4. **WorkoutSuggestion**: Personalized workout recommendations
5. **Achievement**: Badge system for milestones

### Frontend Components

1. **Home**: Landing page with feature highlights
2. **Login/Register**: Authentication pages
3. **Dashboard**: User stats and recent activities
4. **Activities**: Activity logging and history
5. **Teams**: Team creation and management
6. **Leaderboard**: Rankings for users and teams
7. **Workouts**: Personalized workout suggestions

## 🔒 Security Features

- Token-based authentication
- CORS configuration for secure frontend-backend communication
- Password validation
- Protected routes in frontend
- User-specific data access controls

## 🌐 Environment Configuration

### Codespaces Support
The application automatically detects GitHub Codespaces environment and configures ALLOWED_HOSTS and CORS_ALLOWED_ORIGINS accordingly.

### Environment Variables
- `CODESPACE_NAME`: Automatically set in GitHub Codespaces

## 📊 Database Schema

### UserProfile
- One-to-One relationship with Django User
- Fitness level (beginner/intermediate/advanced/expert)
- Physical stats (height, weight)
- Fitness goals
- Total points

### Activity
- Foreign key to User
- Activity type, duration, distance, intensity
- Points earned (calculated automatically)
- Date performed

### Team
- Creator (Foreign key to User)
- Members (Many-to-Many with User)
- Total points (sum of all members' points)

### WorkoutSuggestion
- Foreign key to User
- Workout details (type, duration, intensity)
- Fitness level recommendation
- Completion status

### Achievement
- Foreign key to User
- Badge type and details
- Earned timestamp

## 🚀 Deployment

### Backend Deployment
1. Update `SECRET_KEY` in settings.py
2. Set `DEBUG = False`
3. Configure production database
4. Set up proper ALLOWED_HOSTS
5. Collect static files: `python manage.py collectstatic`
6. Use a production WSGI server (gunicorn, uwsgi)

### Frontend Deployment
1. Update API URL in App.js
2. Build production version: `npm run build`
3. Deploy build folder to hosting service

## 🤝 Contributing

This is a learning project built as part of the GitHub Copilot skills course. Feel free to fork and extend it!

## 📝 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- Built as part of GitHub Skills course: "Build applications with GitHub Copilot agent mode"
- Logo and design inspired by fitness tracking applications
- Sample data created for demonstration purposes

## 📧 Support

For issues and questions, please open an issue on the GitHub repository.

---

**Happy Fitness Tracking! 🏋️‍♂️💪🏃‍♀️**
