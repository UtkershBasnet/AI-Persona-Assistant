"""
FastAPI application — Utkersh Basnet's AI Persona Assistant.
"""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .api.chat import router as chat_router, set_persona_chat
from .api.calendar import router as calendar_router
from .api.vapi import router as vapi_router, set_vectorstore as set_vapi_vectorstore
from .rag.vectorstore import load_vectorstore
from .rag.chain import PersonaChat


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize the RAG pipeline on startup."""
    settings = get_settings()
    print("\n🚀 Starting AI Persona Assistant...")
    print(f"   Model: {settings.CHAT_MODEL}")
    print(f"   Vector DB: {settings.CHROMA_PERSIST_DIR}")

    try:
        vectorstore = load_vectorstore(
            persist_dir=settings.CHROMA_PERSIST_DIR,
            embedding_model_name=settings.EMBEDDING_MODEL,
        )
        persona = PersonaChat(
            vectorstore=vectorstore,
            model=settings.CHAT_MODEL,
            cal_link=settings.CAL_COM_LINK,
        )
        set_persona_chat(persona)
        set_vapi_vectorstore(vectorstore)
        print("✅ AI Persona ready!")
        print(f"   Vapi endpoint: /api/vapi/chat/completions\n")
    except FileNotFoundError as e:
        print(f"\n⚠️  {e}")
        print("   The chat endpoint will return 503 until you run:")
        print("   python -m backend.scripts.ingest\n")

    yield
    print("\n👋 Shutting down AI Persona Assistant...")


app = FastAPI(
    title="AI Persona Assistant",
    description="Utkersh Basnet's AI representative — chat, ask about projects, and book interviews.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow the Next.js frontend + Vapi
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Vapi needs to reach the endpoint
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(chat_router)
app.include_router(calendar_router)
app.include_router(vapi_router)


@app.get("/", tags=["health"])
async def root():
    return {
        "status": "online",
        "service": "AI Persona Assistant",
        "persona": "Utkersh Basnet",
        "docs": "/docs",
    }


@app.get("/health", tags=["health"])
async def health_check():
    from .api.chat import persona_chat
    return {
        "status": "healthy",
        "rag_initialized": persona_chat is not None,
    }
