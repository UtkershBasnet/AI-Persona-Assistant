"""
Embedding model — uses Gemini-hosted embeddings to keep deployment light.
"""
import httpx
import time

from ..config import get_settings


class GeminiEmbeddings:
    """Minimal embedding adapter for Chroma using Gemini's REST API."""

    def __init__(self, model_name: str = "models/gemini-embedding-001"):
        settings = get_settings()
        self.model_name = model_name
        self.api_key = settings.GOOGLE_API_KEY
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY is required for Gemini embeddings.")

    def _post(self, suffix: str, payload: dict) -> dict:
        last_error = None
        for attempt in range(6):
            response = httpx.post(
                f"https://generativelanguage.googleapis.com/v1beta/{self.model_name}:{suffix}",
                params={"key": self.api_key},
                json=payload,
                timeout=60.0,
            )
            if response.status_code != 429:
                response.raise_for_status()
                return response.json()

            last_error = response
            time.sleep(min(2 ** attempt, 20))

        assert last_error is not None
        last_error.raise_for_status()
        return {}

    def _embed(self, text: str, task_type: str) -> list[float]:
        data = self._post(
            "embedContent",
            {
                "model": self.model_name,
                "content": {"parts": [{"text": text}]},
                "taskType": task_type,
            },
        )
        return data["embedding"]["values"]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        embeddings: list[list[float]] = []
        batch_size = 4
        for start in range(0, len(texts), batch_size):
            batch = texts[start : start + batch_size]
            data = self._post(
                "batchEmbedContents",
                {
                    "requests": [
                        {
                            "model": self.model_name,
                            "content": {"parts": [{"text": text}]},
                            "taskType": "RETRIEVAL_DOCUMENT",
                        }
                        for text in batch
                    ]
                },
            )
            embeddings.extend(item["values"] for item in data["embeddings"])
        return embeddings

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text, "RETRIEVAL_QUERY")


def get_embedding_model(model_name: str = "models/gemini-embedding-001") -> GeminiEmbeddings:
    """Get the hosted embedding model for vectorization."""
    return GeminiEmbeddings(model_name=model_name)
