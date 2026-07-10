# Personal Blog Backend API

A lightweight, RESTful backend API for a personal blog. It features a public guest section for reading articles and a secure admin section for content management and analytics.

## Tech Stack
- **Framework:** FastAPI (Python)
- **Database:** SQLite
- **Validation:** Pydantic

## Database Schema
The application uses a single SQLite database (`blog.db`) with the following schema:
```sql
CREATE TABLE articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    published_date TEXT NOT NULL,
    visits INTEGER DEFAULT 0
);
```

## Setup & Installation

1. **Create project directory and virtual environment:**
   ```bash
   mkdir my_blog_backend && cd my_blog_backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn
   ```

## Running the Application

Start the local development server:
```bash
uvicorn main:app --reload
```
* Access the API: `http://127.0.0.1:8000`
* Access Interactive Docs (Swagger UI): `http://127.0.0.1:8000/docs`

## API Endpoints

### Guest Section (Public)
No authentication required.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/articles` | Fetch a list of all published articles. |
| `GET` | `/articles/{id}` | Fetch a single article by ID. *(Automatically increments the visit counter).* |

### Admin Section (Protected)
Requires the `X-Admin-Token` header for authentication.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/login` | Authenticate admin credentials and retrieve the access token. |
| `GET` | `/admin/dashboard` | View all articles with their visit analytics. |
| `POST` | `/articles` | Create and publish a new article. |
| `PATCH` | `/articles/{id}` | Update an existing article's title or content. |
| `DELETE` | `/articles/{id}` | Permanently delete an article. |

## Authentication Guide

1. **Obtain Token:** Send a `POST` request to `/login` with your admin credentials. The response will contain your access token.
2. **Authorize in Swagger UI:** 
   - Go to `http://127.0.0.1:8000/docs`.
   - Click the **Authorize** button (top right).
   - Enter your token and click authorize.
3. **Test Protected Routes:** All Admin endpoints will now automatically include the `X-Admin-Token` header in their requests.
