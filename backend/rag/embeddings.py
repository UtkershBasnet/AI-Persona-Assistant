"""
Embedding model — uses sentence-transformers for local, free embeddings.
"""
from langchain_huggingface import HuggingFaceEmbeddings


def get_embedding_model(model_name: str = "all-MiniLM-L6-v2") -> HuggingFaceEmbeddings:
    """Get the HuggingFace embedding model for vectorization."""
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
