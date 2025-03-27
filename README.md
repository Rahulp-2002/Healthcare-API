# Healthcare Application API Documentation

<p>This is the API for the Healthcare Application built with Django, Django REST Framework, and PostgreSQL. The API allows users to manage patient and doctor records securely with JWT authentication.</p>

## Authentication APIs

### Register a new user
- **Endpoint**: `POST /api/auth/register/`
- **Description**: Registers a new user.
  {
    "username": "your_username",
    "email": "your_email@example.com",
    "password": "your_password"
  }
