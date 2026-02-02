# Secure Web Application – Admin & User Authentication

## Project Overview
This project is a secure web application developed using Python Flask.
It implements authentication, authorization, and role-based access control
with a protected admin dashboard.

---

## Objectives
- Secure user login and registration
- Password hashing using bcrypt
- Role-based access (Admin / User)
- Session-based authentication
- Admin dashboard protection

---

## Tech Stack
- Backend: Python (Flask)
- Frontend: HTML
- Database: SQLite
- Security: Flask-Bcrypt
- Session Management: Flask Session

---

## Features
- User Registration & Login
- Secure password hashing
- Default admin account creation
- Admin dashboard
- User dashboard
- Logout functionality
- Session protection

---

## Default Admin Credentials
For initial testing and demonstration, a default admin account is created during the first run of the application.

Email: admin@secureapp.com
Password: admin123

---

## How to Run the Project
1. Activate virtual environment:
`venv\Script\activate
`
   
3. Run the application:
`python app.py
`

5. Open browser and visit:
`http://127.0.0.1:5000
`

---

## Project Structure
secure-web-app
│── app.py
│── database.db
│── README.md
│── .gitignore
│
├── venv/
│
└── templates/
    ├── login.html
    ├── register.html
    ├── dashboard.html
    └── admin.html
