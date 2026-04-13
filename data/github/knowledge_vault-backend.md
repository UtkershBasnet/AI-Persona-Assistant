
# knowledge_vault-backend

## Description


## Languages
Python

## Topics


## Stars
0

## README
# Knowledge Vault - Backend

An AI-powered backend for a personal knowledge management system. This service provides secure authentication, CRUD operations for knowledge items, and semantic search capabilities using machine learning embeddings.

## Problem Statement
In an era of information overload, individuals often struggle to organize and retrieve specific insights from their various notes and documents. Traditional keyword-based search often fails to find relevant information if the exact terms aren't used. Knowledge Vault solves this by using AI embeddings to enable semantic search, allowing users to find information based on meaning rather than just keywords.

## Tech Stack Used
- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **Database:** [MongoDB](https://www.mongodb.com/) (NoSQL)
- **AI/ML:** [Sentence-Transformers](https://www.sbert.net/) (for text embeddings)
- **Authentication:** JWT (JSON Web Tokens) with `python-jose` and `passlib`
- **Other:** `python-dotenv`, `pymongo`, `uvicorn`

## Features Implemented
- **User Authentication:** Secure registration and login using hashed passwords and JWT.
- **Knowledge Management:** Full CRUD (Create, Read, Update, Delete) for knowledge items.
- **AI Embeddings:** Automatic generation of vector embeddings for all stored knowledge.
- **Semantic Search:** Meaning-based retrieval using vector similarity.
- **CORS Middleware:** Enabled for cross-origin communication with the mobile frontend.

## How to Run Locally

### Prerequisites
- Python 3.8+
- MongoDB instance (Local or Atlas)

### Steps
1. **Navigate to backend directory:**
   ```bash
   cd knowledge_vault-backend
   ```
2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure environment variables:**
   Create a `.env` file in the `backend/` directory with:
   ```env
   MONGODB_URL=your_mongodb_connection_string
   SECRET_KEY=your_secret_key_for_jwt
   ```
5. **Run the server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   The API will be available at `http://localhost:8000`.

## API Documentation (Basic)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/auth/register` | Register a new user | No |
| `POST` | `/auth/login` | Login and receive a JWT token | No |
| `GET`  | `/knowledge/` | Fetch all knowledge items for the user | Yes |
| `POST` | `/knowledge/` | Create a new knowledge item (triggers embedding) | Yes |
| `PUT`  | `/knowledge/{id}` | Update an existing knowledge item | Yes |
| `DELETE` | `/knowledge/{id}` | Delete a knowledge item | Yes |
| `POST` | `/search` | Perform a semantic search query | Yes |

*Detailed Swagger documentation is available at `http://localhost:8000/docs` when the server is running.*
  # cap at 3000 chars per repo
