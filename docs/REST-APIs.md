# REST API Design Document

## 1. Overview

1. **API Name**: Movie Management API  
2. **Business Purpose**:  
   - This API allows users to create and retrieve movie records, supporting a simplified movie management system.  

## 2. High-Level Architecture and Constraints

1. **Technology Stack**:  
   - **Backend**: Python-based FastAPI  
   - **Database**: PostgreSQL  
   - **Hosting**: Local Linux System  

2. **Constraints**:  
   - **Security**: Must use HTTPS/TLS for data in transit; all POST requests require a valid Bearer token.

## 3. Resources and Endpoints

### 3.1 Resource Name
**Resource**: `Movie`  
**Base URL**: `/movies`

### 3.2 Endpoint: Create Movie (POST `/movies`)
- **Description**: Creates a new movie record in the system.

#### 3.2.1 Operations
- **HTTP Method**: `POST`  
- **Purpose**: Add a new movie to the database.  

#### 3.2.2 Request Structure
- **Headers**:  
  - `Content-Type: application/json`  
  - `Authorization: Bearer <token>` (required for authenticated access)  
- **Path Parameters**: None  
- **Query Parameters**: None  
- **Request Body (JSON)**:  
  ```json
  {
    "title": "string - required",
    "description": "string - optional",
    "releaseYear": "number - required",
    "genre": "string - optional"
  }
  ```
  - **title**: The name of the movie. (Required)  
  - **description**: A short description or synopsis. (Optional)  
  - **releaseYear**: Year of release, e.g., `2022`. (Required)  
  - **genre**: The genre of the movie (e.g., `Action`, `Drama`). (Optional)

#### 3.2.3 Response Structure
- **Success (201 Created)**:  
  - **Headers**: `Location: /movies/{newMovieId}`  
  - **Body** (JSON):
    ```json
    {
      "id": 101,
      "title": "The Matrix",
      "description": "A computer hacker learns about the true nature of reality.",
      "releaseYear": 1999,
      "genre": "Sci-Fi",
      "createdAt": "2025-01-02T10:15:30Z"
    }
    ```
- **Error (400 Bad Request)**:  
  ```json
  {
    "error": "Validation Error",
    "message": "Title is required."
  }
  ```
- **Error (401 Unauthorized)** (if missing or invalid token):
  ```json
  {
    "error": "Unauthorized",
    "message": "Invalid or missing token."
  }
  ```

#### 3.2.4 Example Requests/Responses

- **Example Request** (cURL):
  ```bash
  curl -X POST \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer eyJhbGciOi..." \
       -d '{
             "title": "The Matrix",
             "releaseYear": 1999,
             "description": "A computer hacker learns about the true nature of reality.",
             "genre": "Sci-Fi"
           }' \
       https://api.example.com/movies
  ```

- **Example Success Response**:
  ```json
  {
    "id": 101,
    "title": "The Matrix",
    "description": "A computer hacker learns about the true nature of reality.",
    "releaseYear": 1999,
    "genre": "Sci-Fi",
    "createdAt": "2025-01-02T10:15:30Z"
  }
  ```

### 3.3 Endpoint: Get All Movies (GET `/movies`)

- **Description**: Retrieves a list of all movie records in the system.

#### 3.3.1 Operations
- **HTTP Method**: `GET`  
- **Purpose**: Fetch all available movies with optional filtering.

#### 3.3.2 Request Structure
- **Headers**:  
  - `Accept: application/json` (optional)  
- **Path Parameters**: None  
- **Query Parameters** (Optional):
  - `page`: Page number for pagination, e.g., `?page=2`  
  - `limit`: Number of results per page, e.g., `?limit=10`  
  - Example full URL: `/movies?page=2&limit=10`
- **Request Body**: None

#### 3.3.3 Response Structure
- **Success (200 OK)**:
  ```json
  {
    "page": 1,
    "limit": 10,
    "total": 2,
    "data": [
      {
        "id": 1,
        "title": "The Matrix",
        "description": "A computer hacker learns about the true nature of reality.",
        "releaseYear": 1999,
        "genre": "Sci-Fi"
      },
      {
        "id": 2,
        "title": "Inception",
        "description": "A thief steals corporate secrets through dream-sharing technology.",
        "releaseYear": 2010,
        "genre": "Sci-Fi"
      }
    ]
  }
  ```
- **Error (500 Internal Server Error)**:
  ```json
  {
    "error": "ServerError",
    "message": "An unexpected error occurred."
  }
  ```

#### 3.3.4 Example Requests/Responses

- **Example Request** (cURL):
  ```bash
  curl -X GET "https://api.example.com/movies?page=1&limit=10"
  ```

- **Example Success Response**:
  ```json
  {
    "page": 1,
    "limit": 10,
    "total": 2,
    "data": [
      {
        "id": 1,
        "title": "The Matrix",
        "description": "A computer hacker learns about the true nature of reality.",
        "releaseYear": 1999,
        "genre": "Sci-Fi"
      },
      {
        "id": 2,
        "title": "Inception",
        "description": "A thief steals corporate secrets through dream-sharing technology.",
        "releaseYear": 2010,
        "genre": "Sci-Fi"
      }
    ]
  }
  ```

## 4. Data Models

**Entity: `Movie`**  
- **Fields**:
  - `id` (integer, auto-generated, unique primary key)  
  - `title` (string, required, max length 255)  
  - `description` (string, optional, max length 1000)  
  - `releaseYear` (integer, required)  
  - `genre` (string, optional, max length 100)  
  - `createdAt` (timestamp, auto-generated)  

**Relationships**:  
- Currently, no direct relationship to other entities in this simplified example.

## 5. Authentication & Authorization

1. **Auth Method**:  
   - A separate Auth Service issues JWT tokens.  
   - The `POST /movies` endpoint requires a valid Bearer token in the `Authorization` header.  

2. **Roles / Permissions**:  
   - **Admin**: Can create movies (future endpoints will include update/delete).  
   - **User**: Can view (GET) movies.  

3. **Token Details**:  
   - **Format**: JWT with `sub` (subject) and `exp` (expiration).  
   - **Expiration**: 24 hours by default, refresh token available via Auth Service.

## 6. Error Handling & Status Codes

- **POST /movies**:  
  - `201 Created`: Movie created successfully.  
  - `400 Bad Request`: Missing or invalid data in the request body.  
  - `401 Unauthorized`: Invalid or missing token.  
  - `500 Internal Server Error`: Unexpected server-side error.  

- **GET /movies**:  
  - `200 OK`: Movies retrieved successfully.  
  - `500 Internal Server Error`: Unexpected server-side error.  

**Error Response Format** (JSON):
```json
{
  "error": "ErrorType",
  "message": "Human-readable message describing the error."
}
```

## 7. Testing Strategy

1. **Types of Tests**:  
   - **Unit**: Validate controller logic.  
   - **Integration**: Ensure DB operations succeed when creating and fetching movies.  
   - **Performance**: Load tests with JMeter or Artillery.  

*(Additional testing details can be added as needed—e.g., test environments, CI/CD setup, etc.)*

**End of Document**