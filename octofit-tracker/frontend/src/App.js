import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import './App.css';
import logo from './octofitapp-small.png';

// API Configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Helper function for API calls
const apiCall = async (endpoint, options = {}) => {
  const token = localStorage.getItem('token');
  const headers = {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Token ${token}` }),
    ...options.headers,
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok && response.status === 401) {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login';
  }

  return response;
};

// Navigation Component
function Navigation({ user, onLogout }) {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
      <div className="container">
        <Link className="navbar-brand d-flex align-items-center" to="/">
          <img src={logo} alt="OctoFit" height="40" className="me-2" />
          <span>OctoFit Tracker</span>
        </Link>
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav ms-auto">
            {user ? (
              <>
                <li className="nav-item">
                  <Link className="nav-link" to="/dashboard">Dashboard</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/activities">Activities</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/teams">Teams</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/leaderboard">Leaderboard</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/workouts">Workouts</Link>
                </li>
                <li className="nav-item">
                  <button className="btn btn-outline-light ms-2" onClick={onLogout}>Logout</button>
                </li>
              </>
            ) : (
              <>
                <li className="nav-item">
                  <Link className="nav-link" to="/leaderboard">Leaderboard</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/login">Login</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/register">Register</Link>
                </li>
              </>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
}

// Home Component
function Home() {
  return (
    <div className="container mt-5">
      <div className="jumbotron text-center bg-light p-5 rounded">
        <img src={logo} alt="OctoFit" className="mb-4" style={{ maxWidth: '200px' }} />
        <h1 className="display-4">Welcome to OctoFit Tracker</h1>
        <p className="lead">Your comprehensive gym SaaS for managing customer training progress</p>
        <hr className="my-4" />
        <p>Track your workouts, compete with friends, and achieve your fitness goals!</p>
        <Link className="btn btn-primary btn-lg me-2" to="/register">Get Started</Link>
        <Link className="btn btn-outline-primary btn-lg" to="/leaderboard">View Leaderboard</Link>
      </div>
      
      <div className="row mt-5">
        <div className="col-md-4 mb-4">
          <div className="card h-100">
            <div className="card-body text-center">
              <h3>📊 Track Activities</h3>
              <p>Log your workouts and track your progress over time</p>
            </div>
          </div>
        </div>
        <div className="col-md-4 mb-4">
          <div className="card h-100">
            <div className="card-body text-center">
              <h3>👥 Join Teams</h3>
              <p>Create or join teams and compete together</p>
            </div>
          </div>
        </div>
        <div className="col-md-4 mb-4">
          <div className="card h-100">
            <div className="card-body text-center">
              <h3>🏆 Compete</h3>
              <p>Climb the leaderboard and earn achievements</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// Login Component
function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    try {
      const response = await apiCall('/auth/login/', {
        method: 'POST',
        body: JSON.stringify({ username, password }),
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('token', data.key);
        
        // Get user info
        const userResponse = await apiCall('/auth/user/');
        const userData = await userResponse.json();
        localStorage.setItem('user', JSON.stringify(userData));
        
        onLogin(userData);
      } else {
        setError('Invalid credentials');
      }
    } catch (err) {
      setError('Login failed. Please try again.');
    }
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6">
          <div className="card">
            <div className="card-body">
              <h2 className="card-title text-center mb-4">Login</h2>
              {error && <div className="alert alert-danger">{error}</div>}
              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label className="form-label">Username</label>
                  <input
                    type="text"
                    className="form-control"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                  />
                </div>
                <div className="mb-3">
                  <label className="form-label">Password</label>
                  <input
                    type="password"
                    className="form-control"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                </div>
                <button type="submit" className="btn btn-primary w-100">Login</button>
              </form>
              <div className="text-center mt-3">
                <p>Demo credentials: john_runner / testpass123</p>
                <Link to="/register">Don't have an account? Register</Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// Register Component
function Register({ onLogin }) {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password1: '',
    password2: '',
  });
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const response = await apiCall('/auth/registration/', {
        method: 'POST',
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('token', data.key);
        
        // Get user info
        const userResponse = await apiCall('/auth/user/');
        const userData = await userResponse.json();
        localStorage.setItem('user', JSON.stringify(userData));
        
        onLogin(userData);
      } else {
        const data = await response.json();
        setError(JSON.stringify(data));
      }
    } catch (err) {
      setError('Registration failed. Please try again.');
    }
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6">
          <div className="card">
            <div className="card-body">
              <h2 className="card-title text-center mb-4">Register</h2>
              {error && <div className="alert alert-danger">{error}</div>}
              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label className="form-label">Username</label>
                  <input
                    type="text"
                    className="form-control"
                    value={formData.username}
                    onChange={(e) => setFormData({...formData, username: e.target.value})}
                    required
                  />
                </div>
                <div className="mb-3">
                  <label className="form-label">Email</label>
                  <input
                    type="email"
                    className="form-control"
                    value={formData.email}
                    onChange={(e) => setFormData({...formData, email: e.target.value})}
                    required
                  />
                </div>
                <div className="mb-3">
                  <label className="form-label">Password</label>
                  <input
                    type="password"
                    className="form-control"
                    value={formData.password1}
                    onChange={(e) => setFormData({...formData, password1: e.target.value})}
                    required
                  />
                </div>
                <div className="mb-3">
                  <label className="form-label">Confirm Password</label>
                  <input
                    type="password"
                    className="form-control"
                    value={formData.password2}
                    onChange={(e) => setFormData({...formData, password2: e.target.value})}
                    required
                  />
                </div>
                <button type="submit" className="btn btn-primary w-100">Register</button>
              </form>
              <div className="text-center mt-3">
                <Link to="/login">Already have an account? Login</Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// Dashboard Component
function Dashboard() {
  const [profile, setProfile] = useState(null);
  const [statistics, setStatistics] = useState(null);
  const [recentActivities, setRecentActivities] = useState([]);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [profileRes, statsRes, activitiesRes] = await Promise.all([
        apiCall('/profiles/me/'),
        apiCall('/activities/statistics/'),
        apiCall('/activities/my_activities/'),
      ]);

      if (profileRes.ok) setProfile(await profileRes.json());
      if (statsRes.ok) setStatistics(await statsRes.json());
      if (activitiesRes.ok) {
        const activities = await activitiesRes.json();
        setRecentActivities(activities.slice(0, 5));
      }
    } catch (err) {
      console.error('Error fetching dashboard data:', err);
    }
  };

  if (!profile) return <div className="container mt-5"><div className="spinner-border"></div></div>;

  return (
    <div className="container mt-4">
      <h1>Welcome, {profile.username}!</h1>
      
      <div className="row mt-4">
        <div className="col-md-3 mb-3">
          <div className="card text-center">
            <div className="card-body">
              <h3>{statistics?.total_points || 0}</h3>
              <p className="text-muted">Total Points</p>
            </div>
          </div>
        </div>
        <div className="col-md-3 mb-3">
          <div className="card text-center">
            <div className="card-body">
              <h3>{statistics?.total_activities || 0}</h3>
              <p className="text-muted">Activities</p>
            </div>
          </div>
        </div>
        <div className="col-md-3 mb-3">
          <div className="card text-center">
            <div className="card-body">
              <h3>{statistics?.total_duration || 0}</h3>
              <p className="text-muted">Minutes</p>
            </div>
          </div>
        </div>
        <div className="col-md-3 mb-3">
          <div className="card text-center">
            <div className="card-body">
              <h3>{(statistics?.total_distance || 0).toFixed(1)}</h3>
              <p className="text-muted">KM</p>
            </div>
          </div>
        </div>
      </div>

      <div className="row mt-4">
        <div className="col-md-6">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">Profile Information</h5>
              <p><strong>Fitness Level:</strong> {profile.fitness_level}</p>
              <p><strong>Height:</strong> {profile.height} cm</p>
              <p><strong>Weight:</strong> {profile.weight} kg</p>
              <p><strong>Goals:</strong> {profile.fitness_goals || 'Not set'}</p>
            </div>
          </div>
        </div>
        <div className="col-md-6">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">Recent Activities</h5>
              {recentActivities.length > 0 ? (
                <ul className="list-group list-group-flush">
                  {recentActivities.map(activity => (
                    <li key={activity.id} className="list-group-item">
                      <strong>{activity.activity_type}</strong> - {activity.duration} min
                      <br />
                      <small className="text-muted">{activity.date_performed}</small>
                    </li>
                  ))}
                </ul>
              ) : (
                <p>No activities yet. <Link to="/activities">Log your first workout!</Link></p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// Activities Component
function Activities() {
  const [activities, setActivities] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    activity_type: 'running',
    duration: '',
    distance: '',
    intensity: 'moderate',
    date_performed: new Date().toISOString().split('T')[0],
    notes: '',
  });

  useEffect(() => {
    fetchActivities();
  }, []);

  const fetchActivities = async () => {
    try {
      const response = await apiCall('/activities/my_activities/');
      if (response.ok) {
        setActivities(await response.json());
      }
    } catch (err) {
      console.error('Error fetching activities:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await apiCall('/activities/', {
        method: 'POST',
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        setShowForm(false);
        setFormData({
          activity_type: 'running',
          duration: '',
          distance: '',
          intensity: 'moderate',
          date_performed: new Date().toISOString().split('T')[0],
          notes: '',
        });
        fetchActivities();
      }
    } catch (err) {
      console.error('Error creating activity:', err);
    }
  };

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1>My Activities</h1>
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : 'Log Activity'}
        </button>
      </div>

      {showForm && (
        <div className="card mb-4">
          <div className="card-body">
            <h5 className="card-title">Log New Activity</h5>
            <form onSubmit={handleSubmit}>
              <div className="row">
                <div className="col-md-6 mb-3">
                  <label className="form-label">Activity Type</label>
                  <select
                    className="form-select"
                    value={formData.activity_type}
                    onChange={(e) => setFormData({...formData, activity_type: e.target.value})}
                  >
                    <option value="running">Running</option>
                    <option value="walking">Walking</option>
                    <option value="cycling">Cycling</option>
                    <option value="swimming">Swimming</option>
                    <option value="strength_training">Strength Training</option>
                    <option value="yoga">Yoga</option>
                    <option value="cardio">Cardio</option>
                    <option value="sports">Sports</option>
                    <option value="other">Other</option>
                  </select>
                </div>
                <div className="col-md-6 mb-3">
                  <label className="form-label">Duration (minutes)</label>
                  <input
                    type="number"
                    className="form-control"
                    value={formData.duration}
                    onChange={(e) => setFormData({...formData, duration: e.target.value})}
                    required
                  />
                </div>
              </div>
              <div className="row">
                <div className="col-md-6 mb-3">
                  <label className="form-label">Distance (km) - Optional</label>
                  <input
                    type="number"
                    step="0.1"
                    className="form-control"
                    value={formData.distance}
                    onChange={(e) => setFormData({...formData, distance: e.target.value})}
                  />
                </div>
                <div className="col-md-6 mb-3">
                  <label className="form-label">Intensity</label>
                  <select
                    className="form-select"
                    value={formData.intensity}
                    onChange={(e) => setFormData({...formData, intensity: e.target.value})}
                  >
                    <option value="low">Low</option>
                    <option value="moderate">Moderate</option>
                    <option value="high">High</option>
                    <option value="extreme">Extreme</option>
                  </select>
                </div>
              </div>
              <div className="mb-3">
                <label className="form-label">Date</label>
                <input
                  type="date"
                  className="form-control"
                  value={formData.date_performed}
                  onChange={(e) => setFormData({...formData, date_performed: e.target.value})}
                  required
                />
              </div>
              <div className="mb-3">
                <label className="form-label">Notes</label>
                <textarea
                  className="form-control"
                  rows="3"
                  value={formData.notes}
                  onChange={(e) => setFormData({...formData, notes: e.target.value})}
                />
              </div>
              <button type="submit" className="btn btn-primary">Log Activity</button>
            </form>
          </div>
        </div>
      )}

      <div className="row">
        {activities.map(activity => (
          <div key={activity.id} className="col-md-6 mb-3">
            <div className="card">
              <div className="card-body">
                <h5 className="card-title">{activity.activity_type.replace('_', ' ')}</h5>
                <p className="card-text">
                  <strong>Duration:</strong> {activity.duration} minutes<br />
                  {activity.distance && <><strong>Distance:</strong> {activity.distance} km<br /></>}
                  <strong>Intensity:</strong> {activity.intensity}<br />
                  <strong>Points Earned:</strong> {activity.points_earned}<br />
                  <strong>Date:</strong> {activity.date_performed}
                </p>
                {activity.notes && <p className="text-muted">{activity.notes}</p>}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// Leaderboard Component
function Leaderboard() {
  const [userLeaderboard, setUserLeaderboard] = useState([]);
  const [teamLeaderboard, setTeamLeaderboard] = useState([]);
  const [activeTab, setActiveTab] = useState('users');

  useEffect(() => {
    fetchLeaderboards();
  }, []);

  const fetchLeaderboards = async () => {
    try {
      const [usersRes, teamsRes] = await Promise.all([
        apiCall('/leaderboard/'),
        apiCall('/team-leaderboard/'),
      ]);

      if (usersRes.ok) setUserLeaderboard(await usersRes.json());
      if (teamsRes.ok) setTeamLeaderboard(await teamsRes.json());
    } catch (err) {
      console.error('Error fetching leaderboards:', err);
    }
  };

  return (
    <div className="container mt-4">
      <h1 className="mb-4">🏆 Leaderboard</h1>

      <ul className="nav nav-tabs mb-4">
        <li className="nav-item">
          <button
            className={`nav-link ${activeTab === 'users' ? 'active' : ''}`}
            onClick={() => setActiveTab('users')}
          >
            Users
          </button>
        </li>
        <li className="nav-item">
          <button
            className={`nav-link ${activeTab === 'teams' ? 'active' : ''}`}
            onClick={() => setActiveTab('teams')}
          >
            Teams
          </button>
        </li>
      </ul>

      {activeTab === 'users' ? (
        <div className="table-responsive">
          <table className="table table-hover">
            <thead>
              <tr>
                <th>Rank</th>
                <th>Username</th>
                <th>Points</th>
                <th>Activities</th>
              </tr>
            </thead>
            <tbody>
              {userLeaderboard.map(user => (
                <tr key={user.rank}>
                  <td>
                    {user.rank === 1 && '🥇'}
                    {user.rank === 2 && '🥈'}
                    {user.rank === 3 && '🥉'}
                    {user.rank > 3 && user.rank}
                  </td>
                  <td>{user.username}</td>
                  <td>{user.total_points}</td>
                  <td>{user.activity_count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="table-responsive">
          <table className="table table-hover">
            <thead>
              <tr>
                <th>Rank</th>
                <th>Team Name</th>
                <th>Points</th>
                <th>Members</th>
              </tr>
            </thead>
            <tbody>
              {teamLeaderboard.map(team => (
                <tr key={team.rank}>
                  <td>
                    {team.rank === 1 && '🥇'}
                    {team.rank === 2 && '🥈'}
                    {team.rank === 3 && '🥉'}
                    {team.rank > 3 && team.rank}
                  </td>
                  <td>{team.name}</td>
                  <td>{team.total_points}</td>
                  <td>{team.member_count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

// Teams Component
function Teams() {
  const [teams, setTeams] = useState([]);
  const [myTeams, setMyTeams] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({ name: '', description: '' });

  useEffect(() => {
    fetchTeams();
  }, []);

  const fetchTeams = async () => {
    try {
      const [allTeamsRes, myTeamsRes] = await Promise.all([
        apiCall('/teams/'),
        apiCall('/teams/my_teams/'),
      ]);

      if (allTeamsRes.ok) setTeams(await allTeamsRes.json());
      if (myTeamsRes.ok) setMyTeams(await myTeamsRes.json());
    } catch (err) {
      console.error('Error fetching teams:', err);
    }
  };

  const handleCreateTeam = async (e) => {
    e.preventDefault();
    try {
      const response = await apiCall('/teams/', {
        method: 'POST',
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        setShowForm(false);
        setFormData({ name: '', description: '' });
        fetchTeams();
      }
    } catch (err) {
      console.error('Error creating team:', err);
    }
  };

  const handleJoinTeam = async (teamId) => {
    try {
      const response = await apiCall(`/teams/${teamId}/join/`, { method: 'POST' });
      if (response.ok) fetchTeams();
    } catch (err) {
      console.error('Error joining team:', err);
    }
  };

  const handleLeaveTeam = async (teamId) => {
    try {
      const response = await apiCall(`/teams/${teamId}/leave/`, { method: 'POST' });
      if (response.ok) fetchTeams();
    } catch (err) {
      console.error('Error leaving team:', err);
    }
  };

  const isInTeam = (teamId) => myTeams.some(t => t.id === teamId);

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1>Teams</h1>
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : 'Create Team'}
        </button>
      </div>

      {showForm && (
        <div className="card mb-4">
          <div className="card-body">
            <h5 className="card-title">Create New Team</h5>
            <form onSubmit={handleCreateTeam}>
              <div className="mb-3">
                <label className="form-label">Team Name</label>
                <input
                  type="text"
                  className="form-control"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  required
                />
              </div>
              <div className="mb-3">
                <label className="form-label">Description</label>
                <textarea
                  className="form-control"
                  rows="3"
                  value={formData.description}
                  onChange={(e) => setFormData({...formData, description: e.target.value})}
                />
              </div>
              <button type="submit" className="btn btn-primary">Create Team</button>
            </form>
          </div>
        </div>
      )}

      <h3 className="mb-3">My Teams</h3>
      {myTeams.length > 0 ? (
        <div className="row mb-4">
          {myTeams.map(team => (
            <div key={team.id} className="col-md-6 mb-3">
              <div className="card border-primary">
                <div className="card-body">
                  <h5 className="card-title">{team.name}</h5>
                  <p className="card-text">{team.description}</p>
                  <p>
                    <strong>Points:</strong> {team.total_points}<br />
                    <strong>Members:</strong> {team.member_count}<br />
                    <strong>Creator:</strong> {team.creator_username}
                  </p>
                  <button
                    className="btn btn-outline-danger btn-sm"
                    onClick={() => handleLeaveTeam(team.id)}
                  >
                    Leave Team
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <p className="text-muted mb-4">You haven't joined any teams yet.</p>
      )}

      <h3 className="mb-3">All Teams</h3>
      <div className="row">
        {teams.map(team => (
          <div key={team.id} className="col-md-6 mb-3">
            <div className="card">
              <div className="card-body">
                <h5 className="card-title">{team.name}</h5>
                <p className="card-text">{team.description}</p>
                <p>
                  <strong>Points:</strong> {team.total_points}<br />
                  <strong>Members:</strong> {team.member_count}<br />
                  <strong>Creator:</strong> {team.creator_username}
                </p>
                {!isInTeam(team.id) && (
                  <button
                    className="btn btn-primary btn-sm"
                    onClick={() => handleJoinTeam(team.id)}
                  >
                    Join Team
                  </button>
                )}
                {isInTeam(team.id) && (
                  <span className="badge bg-success">Member</span>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// Workouts Component
function Workouts() {
  const [suggestions, setSuggestions] = useState([]);

  useEffect(() => {
    fetchSuggestions();
  }, []);

  const fetchSuggestions = async () => {
    try {
      const response = await apiCall('/workout-suggestions/');
      if (response.ok) {
        setSuggestions(await response.json());
      }
    } catch (err) {
      console.error('Error fetching suggestions:', err);
    }
  };

  const handleGenerate = async () => {
    try {
      const response = await apiCall('/workout-suggestions/generate/', { method: 'POST' });
      if (response.ok) {
        fetchSuggestions();
      }
    } catch (err) {
      console.error('Error generating suggestions:', err);
    }
  };

  const handleComplete = async (id) => {
    try {
      const response = await apiCall(`/workout-suggestions/${id}/mark_completed/`, { method: 'POST' });
      if (response.ok) {
        fetchSuggestions();
      }
    } catch (err) {
      console.error('Error marking complete:', err);
    }
  };

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1>Workout Suggestions</h1>
        <button className="btn btn-primary" onClick={handleGenerate}>
          Generate Suggestions
        </button>
      </div>

      {suggestions.length > 0 ? (
        <div className="row">
          {suggestions.map(suggestion => (
            <div key={suggestion.id} className="col-md-6 mb-3">
              <div className={`card ${suggestion.completed ? 'border-success' : ''}`}>
                <div className="card-body">
                  <h5 className="card-title">
                    {suggestion.title}
                    {suggestion.completed && <span className="badge bg-success ms-2">Completed</span>}
                  </h5>
                  <p className="card-text">{suggestion.description}</p>
                  <p>
                    <strong>Type:</strong> {suggestion.activity_type.replace('_', ' ')}<br />
                    <strong>Duration:</strong> {suggestion.recommended_duration} min<br />
                    <strong>Intensity:</strong> {suggestion.recommended_intensity}<br />
                    <strong>Level:</strong> {suggestion.fitness_level}
                  </p>
                  {!suggestion.completed && (
                    <button
                      className="btn btn-success btn-sm"
                      onClick={() => handleComplete(suggestion.id)}
                    >
                      Mark as Completed
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="alert alert-info">
          <p>No workout suggestions yet. Click "Generate Suggestions" to get personalized workout recommendations based on your fitness level!</p>
        </div>
      )}
    </div>
  );
}

// Protected Route Component
function ProtectedRoute({ children, user }) {
  return user ? children : <Navigate to="/login" />;
}

// Main App Component
function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
  };

  return (
    <Router>
      <div className="App">
        <Navigation user={user} onLogout={handleLogout} />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login onLogin={handleLogin} />} />
          <Route path="/register" element={<Register onLogin={handleLogin} />} />
          <Route path="/leaderboard" element={<Leaderboard />} />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute user={user}>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/activities"
            element={
              <ProtectedRoute user={user}>
                <Activities />
              </ProtectedRoute>
            }
          />
          <Route
            path="/teams"
            element={
              <ProtectedRoute user={user}>
                <Teams />
              </ProtectedRoute>
            }
          />
          <Route
            path="/workouts"
            element={
              <ProtectedRoute user={user}>
                <Workouts />
              </ProtectedRoute>
            }
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
