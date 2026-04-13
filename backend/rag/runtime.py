"""
Shared runtime state for lazily initializing RAG resources.
"""
import asyncio
from dataclasses import dataclass
from typing import Optional

from .chain import PersonaChat
from .retriever import LightweightRetriever
from ..config import get_settings


@dataclass
class RuntimeState:
    persona_chat: Optional[PersonaChat] = None
    retriever: Optional[LightweightRetriever] = None
    initializing: bool = False
    last_error: Optional[str] = None


_state = RuntimeState()
_init_lock = asyncio.Lock()


def get_runtime_state() -> RuntimeState:
    """Return the shared runtime state."""
    return _state


async def ensure_runtime_ready() -> RuntimeState:
    """Load the vector store and chat chain on first use."""
    if _state.persona_chat is not None and _state.retriever is not None:
        return _state

    async with _init_lock:
        if _state.persona_chat is not None and _state.retriever is not None:
            return _state

        _state.initializing = True
        _state.last_error = None
        settings = get_settings()

        try:
            retriever = await asyncio.to_thread(
                LightweightRetriever.from_data_dir,
                data_dir=settings.DATA_DIR,
            )
            persona = PersonaChat(
                retriever=retriever,
                model=settings.CHAT_MODEL,
                cal_link=settings.CAL_COM_LINK,
            )
            _state.retriever = retriever
            _state.persona_chat = persona
            print("✅ AI Persona ready!")
            print("   Retrieval: lightweight in-memory index")
            print("   Vapi endpoint: /api/vapi/chat/completions\n")
        except Exception as exc:
            _state.last_error = str(exc)
            raise
        finally:
            _state.initializing = False

    return _state
