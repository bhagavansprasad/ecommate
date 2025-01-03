# Movie Management System

## Overview
This project implements a **Movie Management System** using **FastAPI** for the backend and **Streamlit** for the frontend. It supports features like:

- User authentication and role-based access control (RBAC)
- CRUD operations for movie management
- Multi-client support with easy configuration
- Secure token-based authentication

## Features
- **Authentication**: Secure user authentication with JWT tokens.
- **Role-Based Access Control**:
  - **User**: Access to basic movie management.
  - **Admin**: Ability to manage users and movies.
  - **Root**: Full access to all resources.
- **CRUD Operations**:
  - Create, Read, Update, and Delete movies.
- **Multi-Client Support**: Add new clients by updating a JSON configuration file.

## Project Structure
```
app/
│
├── main.py              # Entry point for FastAPI app
│
├── config/
│   ├── __init__.py      # Init file for config module
│   ├── config.py        # Configuration loader
│   └── clients.json     # Client-specific configurations
│
├── database.py          # Database engine and session setup
│
├── dependencies.py      # Dependency for database session
│
├── models.py            # SQLAlchemy models for User and Movie
│
├── security.py          # Password hashing and JWT token creation
│
├── routers/
│   ├── __init__.py      # Init file for routers module
│   ├── auth.py          # Authentication routes (login)
│   ├── admin.py         # Admin routes (user management)
│   └── movies.py        # Movie management routes (CRUD)
│
└── tests/
    ├── __init__.py      # Init file for tests module
    ├── test_auth.py     # Test cases for authentication endpoints
    ├── test_admin.py    # Test cases for admin endpoints
    └── test_movies.py   # Test cases for movie endpoints
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/movie-management-system.git
   cd movie-management-system
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database:
   - Create a PostgreSQL database.
   - Update the connection details in `app/config/clients.json`.
   - Login to PostgreSQL
   ```sh
      sudo -u postgres psql
      jnjnuh
   ```

   - Create User, password, DB, and add privileges
   ```text
      Generate hashed password
      python app/users.py
   ```
   ```sql
   CREATE USER auranetworks WITH PASSWORD 'aura!234';
   CREATE DATABASE auranetworks_db;
   GRANT ALL PRIVILEGES ON DATABASE auranetworks_db TO auranetworks;
   psql -h 127.0.0.1 -U auranetworks auranetworks_db # 'aura!234'
   INSERT INTO users (username, hashed_password, role, client) VALUES ('bhagavan', '$2b$12$BXT2odlsClGfgNUQvOXUuO3RWn13aGZ0fuSyjH2CWpa.nsf.Cn4Pu', 'admin', 'test_client');
   INSERT INTO users (username, hashed_password, role, client) VALUES ('sudhakar', '$2b$12$BXT2odlsClGfgNUQvOXUuO3RWn13aGZ0fuSyjH2CWpa.nsf.Cn4Pu', 'admin', 'test_client');


   CREATE USER dataworkx WITH PASSWORD 'data!234';
   CREATE DATABASE dataworkx_db;
   GRANT ALL PRIVILEGES ON DATABASE dataworkx_db TO dataworkx;
   psql -h 127.0.0.1 -U auranetworks dataworkx_db # 'data!234'
   ```

4. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   uvicorn app.main:app --reload --log-level debug
   ```

5. Start the Streamlit frontend:
   ```bash
   streamlit run ui/ecommapp.py
   ```

## Usage

### Authentication
- Use the `/token` endpoint to log in and get a JWT token.
- Include the token in the `Authorization` header for all subsequent API requests.

### API Documentation
Access the FastAPI Swagger UI:
```
http://localhost:8000/docs
```

### Frontend
Access the Streamlit UI:
```
http://localhost:8501
```

## Dependencies
- **Backend**:
  - FastAPI
  - Uvicorn
  - SQLAlchemy
  - Psycopg2
  - Passlib (bcrypt)
  - Python-JOSE
- **Frontend**:
  - Streamlit
  - Requests

## License
This project is licensed under the MIT License.

