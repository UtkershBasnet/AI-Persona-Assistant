"""
ChromaDB vector store — create, persist, and load the vector database.
"""
import os
from typing import List
from langchain.schema import Document
from langchain_chroma import Chroma
from .embeddings import get_embedding_model


def create_vectorstore(
    documents: List[Document],
    persist_dir: str = "./chroma_db",
    embedding_model_name: str = "all-MiniLM-L6-v2",
) -> Chroma:
    """Create a new ChromaDB vector store from documents and persist it."""
    # Clean out old data if it exists
    if os.path.exists(persist_dir):
        import shutil
        shutil.rmtree(persist_dir)
        print(f"  Cleared old vector store at {persist_dir}")

    embeddings = get_embedding_model(embedding_model_name)

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_dir,
        collection_name="persona_knowledge",
    )

    print(f"  ✓ Vector store created with {len(documents)} documents at {persist_dir}")
    return vectorstore


def load_vectorstore(
    persist_dir: str = "./chroma_db",
    embedding_model_name: str = "all-MiniLM-L6-v2",
) -> Chroma:
    """Load an existing ChromaDB vector store."""
    if not os.path.exists(persist_dir):
        raise FileNotFoundError(
            f"Vector store not found at {persist_dir}. "
            "Run the ingestion script first: python -m backend.scripts.ingest"
        )

    embeddings = get_embedding_model(embedding_model_name)

    vectorstore = Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings,
        collection_name="persona_knowledge",
    )

    count = vectorstore._collection.count()
    print(f"  ✓ Loaded vector store from {persist_dir} ({count} documents)")
    return vectorstore
