# Social Media API

A FastAPI-based REST API for a social media platform with user management and post functionality. Built with PostgreSQL, SQLAlchemy ORM, and Pydantic for data validation.

## Table of Contents

- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Running the Server](#running-the-server)
- [API Endpoints](#api-endpoints)
- [Testing with Postman](#testing-with-postman)
- [Technologies Used](#technologies-used)
- [Project Evolution](#project-evolution)

---

## Project Structure

```
apis/
├── app/
│   ├── __init__.py
│   ├── api.py              # Main FastAPI application with all endpoints
│   ├── database.py         # SQLAlchemy database configuration
│   ├── models.py           # SQLAlchemy ORM models (Post, User)
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore file
├── db_init.py             # Database initialization script (optional)
└── README.md              # This file
```

---

## Prerequisites

Before getting started, ensure you have the following installed:

- **Python 3.11+** - [Download here](https://www.python.org/downloads/)
- **PostgreSQL 12+** - [Download here](https://www.postgresql.org/download/)
- **Git** - [Download here](https://git-scm.com/)
- **Postman** (optional, for API testing) - [Download here](https://www.postman.com/downloads/)

---

## Installation

### 1. Clone the Repository

```bash
cd /Users/nitinkishore/PycharmProjects/apis
```

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
```

### 3. Activate the Virtual Environment

**On macOS/Linux:**
```bash
source .venv/bin/activate
```

**On Windows:**
```bash
.venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Verify Installation

```bash
pip list
```

You should see:
- fastapi==0.104.1
- uvicorn==0.24.0
- pydantic==2.5.0
- python-multipart==0.0.6
- sqlalchemy==2.0.23
- psycopg2-binary==2.9.9

---

## Database Setup

### 1. Create PostgreSQL Database

Open PostgreSQL terminal (psql) and run:

```sql
-- Create database
CREATE DATABASE fastapi;

-- Connect to the database
\c fastapi

-- Tables will be created automatically by SQLAlchemy when the app starts
```

### 2. Database Credentials

The app uses these default PostgreSQL credentials:

- **Host:** localhost
- **Port:** 5432
- **Database:** fastapi
- **User:** postgres
- **Password:** postgres

**To change credentials:** Edit `/Users/nitinkishore/PycharmProjects/apis/app/database.py`

```python
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/fastapi"
```

### 3. Automatic Table Creation

The application automatically creates tables on startup via this line in `api.py`:

```python
models.Base.metadata.create_all(bind=engine)
```

When the server starts:
- ✅ Connects to PostgreSQL
- ✅ Reads model definitions from `models.py`
- ✅ Creates `posts` and `users` tables if they don't exist

---

## Running the Server

### Start the FastAPI Server with Auto-Reload

```bash
cd /Users/nitinkishore/PycharmProjects/apis
uvicorn app.api:app --host 127.0.0.1 --port 8000 --reload
```

### Expected Output

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Access the API

- **API Base URL:** `http://127.0.0.1:8000`
- **Interactive Docs (Swagger UI):** `http://127.0.0.1:8000/docs`
- **Alternative Docs (ReDoc):** `http://127.0.0.1:8000/redoc`

---

## API Endpoints

### Health Check

| Method | Endpoint | Description | Response |
|--------|----------|-------------|----------|
| GET | `/` | Root endpoint | `{"message": "Hello World"}` |

### Test SQLAlchemy

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/sqlalchemy` | Test SQLAlchemy connection and retrieve all posts |

---

## Posts Endpoints

### Get All Posts

```
GET /posts
```

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "title": "First Post",
      "content": "Hello World",
      "published": true,
      "rating": 5,
      "created_at": "2026-04-26T10:30:00"
    }
  ]
}
```

### Create a Post

```
POST /createposts
Content-Type: application/json

{
  "title": "My Post Title",
  "content": "This is the content of my post",
  "published": true,
  "rating": 4
}
```

**Response:** `201 Created`
```json
{
  "data": {
    "id": 2,
    "title": "My Post Title",
    "content": "This is the content of my post",
    "published": true,
    "rating": 4,
    "created_at": "2026-04-26T11:00:00"
  }
}
```

### Get Single Post

```
GET /posts/{id}
```

Example: `GET /posts/1`

**Response:** `200 OK`
```json
{
  "post_detail": {
    "id": 1,
    "title": "First Post",
    "content": "Hello World",
    "published": true,
    "rating": 5,
    "created_at": "2026-04-26T10:30:00"
  }
}
```

**Error Response:** `404 Not Found`
```json
{
  "detail": "post with id: 999 was not found"
}
```

### Update a Post

```
PUT /posts/{id}
Content-Type: application/json

{
  "title": "Updated Title",
  "content": "Updated content",
  "published": true,
  "rating": 5
}
```

**Response:** `200 OK`
```json
{
  "data": {
    "id": 1,
    "title": "Updated Title",
    "content": "Updated content",
    "published": true,
    "rating": 5,
    "created_at": "2026-04-26T10:30:00"
  }
}
```

### Delete a Post

```
DELETE /posts/{id}
```

Example: `DELETE /posts/1`

**Response:** `204 No Content` (empty response)

---

## Users Endpoints

### Get All Users

```
GET /users
```

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "is_active": true,
      "created_at": "2026-04-26T10:30:00"
    }
  ]
}
```

### Create a User

```
POST /users
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password_123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response:** `201 Created`
```json
{
  "data": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure_password_123",
    "first_name": "John",
    "last_name": "Doe",
    "is_active": true,
    "created_at": "2026-04-26T10:30:00"
  }
}
```

### Get Single User

```
GET /users/{id}
```

Example: `GET /users/1`

**Response:** `200 OK`
```json
{
  "user_detail": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_active": true,
    "created_at": "2026-04-26T10:30:00"
  }
}
```

### Update a User

```
PUT /users/{id}
Content-Type: application/json

{
  "username": "john_doe_updated",
  "email": "john_updated@example.com",
  "password": "new_password_456",
  "first_name": "Jonathan",
  "last_name": "Doe"
}
```

**Response:** `200 OK`
```json
{
  "data": {
    "id": 1,
    "username": "john_doe_updated",
    "email": "john_updated@example.com",
    "password": "new_password_456",
    "first_name": "Jonathan",
    "last_name": "Doe",
    "is_active": true,
    "created_at": "2026-04-26T10:30:00"
  }
}
```

### Delete a User

```
DELETE /users/{id}
```

Example: `DELETE /users/1`

**Response:** `204 No Content` (empty response)

---

## Testing with Postman

### 1. Import Collection

- Open Postman
- Click **Import** → **Paste Raw Text**
- Paste the endpoints listed above

### 2. Create a Post Request

**Method:** POST  
**URL:** `http://127.0.0.1:8000/createposts`  
**Headers:**
- Key: `Content-Type`
- Value: `application/json`

**Body (raw JSON):**
```json
{
  "title": "My First Post",
  "content": "This is awesome!",
  "published": true,
  "rating": 5
}
```

### 3. Create a User Request

**Method:** POST  
**URL:** `http://127.0.0.1:8000/users`  
**Headers:**
- Key: `Content-Type`
- Value: `application/json`

**Body (raw JSON):**
```json
{
  "username": "jane_smith",
  "email": "jane@example.com",
  "password": "my_password",
  "first_name": "Jane",
  "last_name": "Smith"
}
```

### 4. Test Other Endpoints

- **GET all posts:** `GET http://127.0.0.1:8000/posts`
- **GET all users:** `GET http://127.0.0.1:8000/users`
- **GET specific post:** `GET http://127.0.0.1:8000/posts/1`
- **GET specific user:** `GET http://127.0.0.1:8000/users/1`

---

## Technologies Used

| Technology | Version | Purpose |
|------------|---------|---------|
| **FastAPI** | 0.104.1 | Web framework for building APIs |
| **Uvicorn** | 0.24.0 | ASGI server to run FastAPI |
| **SQLAlchemy** | 2.0.23 | ORM for database operations |
| **Pydantic** | 2.5.0 | Data validation and serialization |
| **PostgreSQL** | 12+ | Relational database |
| **psycopg2-binary** | 2.9.9 | PostgreSQL adapter for Python |
| **Python** | 3.11+ | Programming language |

---

## Project Evolution

### Phase 1: Initial Setup
- ✅ Created FastAPI application
- ✅ Set up Uvicorn server
- ✅ Created requirements.txt with dependencies
- ✅ Set up localhost binding (127.0.0.1:8000) for security

### Phase 2: Basic Endpoints
- ✅ Created simple GET endpoints
- ✅ Added POST endpoint for creating posts
- ✅ Implemented proper HTTP status codes (201 for creation, 404 for not found)
- ✅ Added HTTPException for proper error handling

### Phase 3: Database Integration
- ✅ Started with in-memory list storage
- ✅ Attempted PostgreSQL with psycopg2 raw queries
- ✅ Encountered compatibility issues on macOS
- ✅ Migrated to SQLAlchemy ORM for cleaner code

### Phase 4: SQLAlchemy Implementation
- ✅ Set up SQLAlchemy database configuration
- ✅ Created Post model with SQLAlchemy
- ✅ Implemented dependency injection with `Depends(get_db)`
- ✅ Converted all endpoints to use SQLAlchemy ORM
- ✅ Commented out old PostgreSQL raw query code for reference

### Phase 5: User Management
- ✅ Created User model with SQLAlchemy
- ✅ Added user CRUD endpoints
- ✅ Implemented Pydantic models for request/response validation
- ✅ Added proper error handling and status codes

### Key Design Decisions
1. **SQLAlchemy ORM** over raw SQL queries for better maintainability
2. **Dependency Injection** using FastAPI's `Depends()` for session management
3. **Pydantic Models** for strict request/response validation
4. **Automatic Table Creation** via `Base.metadata.create_all()`
5. **Auto-reload** enabled during development for faster iteration
6. **Commented Code** preserved for reference and learning

---

## Common Issues & Solutions

### Issue: "password authentication failed for user"

**Solution:** Check credentials in `database.py`:
```python
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/fastapi"
```

Ensure PostgreSQL user/password matches.

### Issue: "Table already exists" error

**Solution:** The error occurs when SQLAlchemy tries to create a table that already exists. This is handled automatically - no action needed.

### Issue: Table gets deleted after restart

**Solution:** This happens because `models.Base.metadata.create_all()` recreates tables. The tables persist in PostgreSQL database, not in memory.

### Issue: Port 8000 already in use

**Solution:** Kill the existing process or use a different port:
```bash
uvicorn app.api:app --host 127.0.0.1 --port 8001 --reload
```

---

## Environment Variables (Optional)

To make the app more secure, you can use environment variables:

Create a `.env` file:
```
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=fastapi
```

Then update `database.py` to read from environment variables.

---

## Next Steps

- ✅ Add authentication (JWT tokens)
- ✅ Add relationships (User has many Posts)
- ✅ Add pagination to endpoints
- ✅ Add search and filtering
- ✅ Add request validation improvements
- ✅ Implement proper error handling middleware
- ✅ Add logging
- ✅ Deploy to cloud (Heroku, AWS, etc.)

---

## Support

For issues or questions:
1. Check the error message in the terminal
2. Verify PostgreSQL is running
3. Ensure all dependencies are installed
4. Check the API documentation at `http://127.0.0.1:8000/docs`

---

## License

This project is open source and available under the MIT License.

---

**Happy coding! 🚀**
