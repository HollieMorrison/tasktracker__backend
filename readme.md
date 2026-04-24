cat > readme.md <<'EOF'
# Task Tracker API

**Task Tracker API** is a backend system built with Django and Django REST Framework (DRF).  
It provides a secure and scalable REST API for managing user authentication and task data.

This API powers the **Task Tracker** web application, allowing users to register, log in, and manage their tasks in real time.

---

## 🔗 Live Links

- **Frontend App:** https://tasktrackerfrontend-b0125962c8ee.herokuapp.com  
- **Frontend Repository:** https://github.com/HollieMorrison/tasktracker__frontend  
- **Backend Repository:** https://github.com/HollieMorrison/tasktracker__backend  

---

## 📚 Table of Contents

- [User Experience (UX)](#user-experience-ux)
- [Features](#features)
- [API Endpoints](#api-endpoints)
- [Future Improvements](#future-improvements)
- [Design](#design)
- [Technologies Used](#technologies-used)
- [Tools & Libraries](#tools--libraries)
- [Testing](#testing)
- [Deployment & Local Setup](#deployment--local-setup)
- [Credits](#credits)
- [Acknowledgements](#acknowledgements)

---

## 🧠 User Experience (UX)

The Task Tracker API is designed to be:

- **Secure** — JWT-based authentication ensures protected access  
- **Reliable** — consistent API responses and validation  
- **Flexible** — easily integrates with frontend applications  

### User Goals

As a developer or tester, I want to:

- Register and authenticate users securely  
- Perform CRUD operations on tasks  
- Access only my own data  
- Integrate easily with a frontend application  

---

## ⚙️ Features

### Implemented Features

- **User Authentication (JWT)**
  - Register, login, logout
  - Token refresh support

- **Task Management**
  - Create, read, update, delete tasks
  - Each user can only access their own tasks

- **User Profile Endpoint**
  - Retrieve authenticated user details

- **Environment Configuration**
  - Uses `.env` for secure settings

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/accounts/register/` | Create a new user |
| POST | `/api/accounts/login/` | Login and receive tokens |
| GET | `/api/accounts/me/` | Get current user |
| GET | `/api/tasks/` | Get all tasks |
| POST | `/api/tasks/` | Create a task |
| PATCH | `/api/tasks/{id}/` | Update a task |
| DELETE | `/api/tasks/{id}/` | Delete a task |

---

## 🚀 Future Improvements

- Task categories or tagging  
- Task sharing between users  
- Email reminders or notifications  
- Admin dashboard  

---

## 🏗️ Design

- Built using **Django MVT architecture**
- Uses **Django REST Framework** for API structure
- Clean endpoint design with consistent responses
- SQLite for development and PostgreSQL-ready for production

---

## 💻 Technologies Used

- Python 3  
- Django 5  
- Django REST Framework  
- PostgreSQL-ready production configuration  
- SimpleJWT  

---

## 🛠️ Tools & Libraries

- GitHub — version control  
- Visual Studio Code — development  
- Postman — API testing  
- python-dotenv — environment variables  
- dj-database-url — database configuration  

---

## 🧪 Testing

### Automated Testing

Run tests with:

```bash
python manage.py test

Covers:

Authentication flows
Task CRUD operations
Permissions and security

Manual Testing :
| Feature                | Action                                   | Expected Result     | Actual Result                      | Pass/Fail |
| ---------------------- | ---------------------------------------- | ------------------- | ---------------------------------- | --------- |
| Register               | POST new user details                    | New user is created | User account created successfully  | Pass      |
| Login                  | POST valid credentials                   | JWT tokens returned | Access and refresh tokens returned | Pass      |
| Current User           | GET authenticated user                   | User data returned  | Correct user details returned      | Pass      |
| Create Task            | POST task data                           | Task is created     | Task stored in database            | Pass      |
| List Tasks             | GET task list                            | User tasks returned | Task list returned successfully    | Pass      |
| Update Task            | PATCH task data                          | Task is updated     | Updated task returned              | Pass      |
| Delete Task            | DELETE task                              | Task is removed     | Task removed from database         | Pass      |
| Unauthenticated Access | Request protected endpoint without token | Request is rejected | 401 response returned              | Pass      |


Manual testing also included:

Testing endpoints using Postman
Verifying authentication protection
Checking error handling
Testing frontend integration

🚀 Deployment & Local Setup
Clone Repository
git clone https://github.com/HollieMorrison/tasktracker__backend.git
cd tasktracker__backend/tasktrackerAPI
Virtual Environment
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
Install Dependencies
pip install -r requirements.txt
Environment Variables

Create a .env file:

DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3

For production, set:

DJANGO_DEBUG=False
DATABASE_URL=your_production_database_url
Run Project
python manage.py migrate
python manage.py runserver

Visit:

http://127.0.0.1:8000/
🌐 Deployment

The backend is deployed using Heroku.

Steps
Connect the GitHub repository to Heroku.
Set required environment variables.
Ensure Procfile, requirements.txt, and runtime.txt are present.
Deploy the main branch.
Run migrations on Heroku:
heroku run python manage.py migrate -a YOUR_BACKEND_APP_NAME
Test the deployed API endpoints.

🔐 Security
Sensitive data is stored in environment variables.
.env is included in .gitignore.
db.sqlite3, cache files, and virtual environments are ignored.
JWT authentication protects user-specific data.
Users should only be able to access and manage their own tasks.

📚 Credits
Django & Django REST Framework documentation
SimpleJWT documentation
Stack Overflow and developer resources

🙌 Acknowledgements
Code Institute mentors and support
Open-source community resources
Test users who provided feedback