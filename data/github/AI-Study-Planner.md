
# AI-Study-Planner

## Description


## Languages
TypeScript, Python, JavaScript, CSS

## Topics


## Stars
0

## README
  # cap at 3000 chars per repo
# AI Study Planner - Backend

Backend API for the AI-Powered Adaptive Study Planner built with FastAPI, Gemini API, and Pinecone.

## Features

- 🔐 **User Authentication** - JWT-based authentication with secure password hashing
- 📄 **Document Upload** - Upload and process PDF study materials  
- 🤖 **RAG System** - Retrieval-Augmented Generation for intelligent Q&A
- 🔍 **Smart Search** - Semantic search using Gemini embeddings and Pinecone
- 💬 **AI Answers** - Context-aware answers powered by Gemini Pro

## Tech Stack

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL ORM with SQLite
- **Gemini API** - Google's AI for embeddings and text generation
- **Pinecone** - Vector database for semantic search
- **LangChain** - Document processing and chunking
- **JWT** - Secure authentication tokens

## Prerequisites

- Python 3.8+
- Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- Pinecone API key ([Sign up here](https://www.pinecone.io/))

## Setup Instructions

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
DATABASE_URL=sqlite:///./study_planner.db
SECRET_KEY=your-secret-key-here-generate-a-random-string

# Gemini API
GEMINI_API_KEY=your-gemini-api-key-here

# Pinecone
PINECONE_API_KEY=your-pinecone-api-key-here
PINECONE_ENVIRONMENT=your-pinecone-environment
PINECONE_INDEX_NAME=study-planner-docs

# Application Settings
UPLOAD_DIR=./uploads
VECTORSTORE_DIR=./vectorstores
```

**To generate a secure SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 4. Run the Server

```bash
python run.py
```

The API will be available at: `http://localhost:8000`

- API Documentation: `http://localhost:8000/docs`
- Alternative Docs: `http://localhost:8000/redoc`

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user info (requires auth)

### Documents

- `POST /api/documents/upload` - Upload PDF document (requires auth)
- `POST /api/documents/query` - Ask questions about documents (requires auth)
- `GET /api/documents/list` - List all uploaded documents (requires auth)
- `DELETE /api/documents/{id}` - Delete a document (requires auth)

## Usage Examples

### 1. Register a User

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "username": "student1",
    "password": "securepass123"
  }'
```

### 2. Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "password": "securepass123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Upload a PDF

```bash
curl -X POST http://localhost:8000/api/documents/upload \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -F "file=@physics_textbook.pdf"
```

### 4. Ask Questions

```bash
curl -X POST http://localhost:8000/api/documents/query \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is Newton'\''s second law?"
  }'
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection
│   ├── api/                 # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication routes
│   │   └── documents.py     # Document routes
│   ├── models/              # Database models
│   │   ├── __init__.py
│   │   ├── user.py          # User model
│   │   └── document.py      # Document model
│   ├── schemas/             # Pydantic schemas
│   │   ├── auth.py          # Auth schemas
│   │   └── document.py      # Document schemas
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   └── rag_engine.py    # RAG processing
│   └── utils/               # Utilities
│       ├── __init__.py
│       └── security.py      # Auth utilities
├── .env.example             # Environment template
├── .gitignore
├── requirements.txt         # Python dependencies
└── run.py                   # Development server
```

## Development

### Running with Auto-Reload

```bash
python run.py
```

This starts the server with auto-reload enabled for development.

### Accessing API Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

## Troubleshooting

### Issue: ModuleNotFoundError

**Solution:** Make sure you've activated the virtual environment and installed dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Pinecone Index Not Found

**Solution:** Create a Pinecone index manually:
1. Go to [Pinecone Console](https://app.pinecone.io/)
2. Create a new index with dimension `768` and metric `cosine`
3. Update `.env` with the index name

### Issue: "Could not validate credentials"

**Solution:** Make sure you're passing the Bearer token correctly:
```bash
-H "Authorization: Bearer YOUR_ACTUAL_TOKEN"
```

## Next Steps (Week 2)

- [ ] Study planner agent with schedule generation
- [ ] Pomodoro timer endpoints
- [ ] Progress tracking and analytics
- [ ] Exam score prediction

## License

MIT
This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
