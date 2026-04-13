"""
FastAPI application — Utkersh Basnet's AI Persona Assistant.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .api.chat import router as chat_router
from .api.calendar import router as calendar_router
from .api.vapi import router as vapi_router
from .rag.runtime import get_runtime_state


app = FastAPI(
    title="AI Persona Assistant",
    description="Utkersh Basnet's AI representative — chat, ask about projects, and book interviews.",
    version="1.0.0",
)

settings = get_settings()
print("\n🚀 Starting AI Persona Assistant...")
print(f"   Model: {settings.CHAT_MODEL}")
print(f"   Data dir: {settings.DATA_DIR}")
print("   Startup mode: lazy lightweight retrieval\n")

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
    state = get_runtime_state()
    return {
        "status": "healthy",
        "rag_initialized": state.persona_chat is not None,
        "initializing": state.initializing,
        "last_error": state.last_error,
        "retrieval_mode": "lightweight",
    }
