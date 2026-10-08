# Job Application Tracker API

A REST API built with FastAPI to track job applications. 
Built as part of my journey toward AI Engineering roles in New York.

## Tech Stack
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT Authentication
- Python

## Features
- User registration and login with JWT authentication
- Full CRUD operations for job applications
- Protected routes
- Request logging with middleware
- Async routes
- Global exception handling

## Endpoints

### Auth
- POST /register → Register new user
- POST /login → Login and get JWT token

### Job Applications
- POST /company → Create application (protected)
- GET /company → Get all applications (protected)
- GET /company/{name} → Get one application (protected)
- PUT /company/{name} → Update application (protected)
- DELETE /company/{name} → Delete application (protected)

## Setup

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate`
4. Install packages: `pip install -r requirements.txt`
5. Create `.env` file with your DATABASE_URL
6. Run: `uvicorn main:app --reload`