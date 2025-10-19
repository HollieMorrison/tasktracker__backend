# Task Tracker API

**Task Tracker API** is a backend system built with Django and Django REST Framework (DRF).  
It provides a secure and reliable foundation for managing user authentication, task data, and API interactions.  
The backend powers the *Task Tracker* web app — helping users stay productive and organised by keeping their daily tasks in sync across devices.

![API Screenshot](./assets/readme/api-preview.png)  
[View Task Tracker API on GitHub](https://github.com/HollieMorrison/tasktracker__backend)

---

## Table of Contents

### [User Experience (UX)](#user-experience-ux-1)
* [User Goals](#user-goals)
### [Features](#features)
* [Implemented Features](#implemented-features)
### [Future Improvements](#future-improvements)
### [Design](#design-1)
### [Technologies Used](#technologies-used-1)
### [Frameworks, Libraries & Tools](#frameworks-libraries--tools-1)
### [Testing](#testing-1)
* [Automated Testing](#automated-testing)
* [Manual Testing](#manual-testing)
### [Deployment and Local Setup](#deployment-and-local-setup-1)
* [Environment Configuration](#environment-configuration)
* [Running Locally](#running-locally)
* [Deployment Steps](#deployment-steps)
### [Credits](#credits-1)
### [Acknowledgements](#acknowledgements-1)

---

## User Experience (UX)

The Task Tracker API is designed to be developer-friendly and dependable.  
It allows easy integration with front-end clients such as React or mobile apps and follows REST principles for clarity and consistency.  

Its focus is on:
- **Security:** Using JWT for token-based authentication.  
- **Clarity:** Clean endpoint naming and structured JSON responses.  
- **Scalability:** Built to grow with new features such as task categories or admin dashboards.

### User Goals

*As a developer or tester using the API, I want to:*
- Register and log in users securely.  
- Manage tasks through clear CRUD endpoints.  
- View, edit, and delete tasks based on authentication tokens.  
- Integrate the backend smoothly with a frontend interface.  

---

## Features

### Implemented Features

- **User Authentication & Authorization:**  
  Register, log in, log out, and verify users using JSON Web Tokens (JWT).  

- **Task Management System:**  
  Create, view, edit, and delete personal tasks.  

- **User Profile Endpoint:**  
  Retrieve information about the authenticated user.  

- **Token Refresh Mechanism:**  
  Obtain new access tokens without logging in again.  

- **Environment Configuration:**  
  Uses `.env` for managing sensitive settings securely.  

Example API overview:

| Method | Endpoint | Description |
|--------|-----------|-------------|
| `POST` | `/api/accounts/register/` | Create a new user account |
| `POST` | `/api/accounts/login/` | Obtain JWT tokens |
| `GET` | `/api/accounts/me/` | Get details of the current user |
| `GET` | `/api/tasks/` | Retrieve all tasks for a user |
| `POST` | `/api/tasks/` | Add a new task |
| `PATCH` | `/api/tasks/{id}/` | Update an existing task |
| `DELETE` | `/api/tasks/{id}/` | Delete a task |

---

### Future Improvements

- Add task categories and due dates.  
- Implement task sharing between users.  
- Include reminders or email notifications.  
- Build an admin dashboard for managing users and data.  

---

## Design

- Built with **Django’s MVT architecture** for clean separation of concerns.  
- **REST Framework viewsets and serializers** simplify endpoint creation.  
- Consistent naming and logical URL patterns improve usability.  
- Database flexibility allows use of SQLite in development and PostgreSQL in production.  

---

## Technologies Used

- [Python 3](https://www.python.org/)  
- [Django 5](https://www.djangoproject.com/)  
- [Django REST Framework](https://www.django-rest-framework.org/)  
- [PostgreSQL](https://www.postgresql.org/)  
- [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)  

---

## Frameworks, Libraries & Tools

- [GitHub](https://github.com/) — version control and repository hosting.  
- [Visual Studio Code](https://code.visualstudio.com/) — IDE for development.  
- [Postman](https://www.postman.com/) — API endpoint testing.  
- [python-dotenv](https://pypi.org/project/python-dotenv/) — manages environment variables.  
- [dj-database-url](https://pypi.org/project/dj-database-url/) — handles dynamic database configuration.  

---

## Testing

### Automated Testing

Unit and integration tests are written with Django’s built-in test framework and DRF’s `APITestCase`.  

Typical tests include:
- Registering and logging in users.  
- Token authentication and refresh flow.  
- CRUD operations for task management.  

Run tests using:
```bash
python manage.py test

Manual Testing

Manual testing included:

Verifying endpoints in Postman using real-world scenarios.

Checking authenticated and unauthenticated access behaviour.

Confirming error handling for invalid input.

Frontend integration testing with live API responses.

Deployment and Local Setup
Environment Configuration

Clone the repository:

git clone https://github.com/HollieMorrison/tasktracker__backend.git


Move into the project folder:

cd tasktracker__backend


Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate      # macOS/Linux  
venv\Scripts\activate         # Windows


Install project dependencies:

pip install -r requirements.txt


Add a .env file with:

DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3

Running Locally

Run database migrations:

python manage.py migrate


Start the development server:

python manage.py runserver


Visit http://127.0.0.1:8000/
 to explore endpoints.

Deployment Steps

This backend can be deployed to services like Render, Railway, or Heroku:

Configure environment variables securely on the platform.

Use dj-database-url for production database connections.

Set DEBUG=False and define ALLOWED_HOSTS for production security.

Credits
Code References

Django and DRF official documentation for structure and testing guidance.

SimpleJWT docs for token-based authentication setup.

Environment setup patterns inspired by modern Django deployment practices.

Content

API documentation and descriptions written by the project developer, Hollie Morrison.

Acknowledgements

Mentors and reviewers who offered feedback on project structure and readability.

Django and open-source community forums for continuous learning resources.

Developer peers who tested endpoints and suggested improvements.
