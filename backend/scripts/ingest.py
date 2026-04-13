"""
Ingestion script — loads documents, chunks them, embeds, and stores in ChromaDB.
Run this before starting the server:
    python -m backend.scripts.ingest
"""
import sys
import os

# Add project root to path so we can import backend modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.config import get_settings
from backend.rag.loader import load_documents, chunk_documents
from backend.rag.vectorstore import create_vectorstore


def main():
    settings = get_settings()

    print("=" * 60)
    print("  📚 AI Persona — Document Ingestion Pipeline")
    print("=" * 60)

    # Step 1: Load documents
    print("\n📄 Step 1: Loading documents...")
    documents = load_documents(data_dir=settings.DATA_DIR)

    if not documents:
        print("\n❌ No documents found! Make sure the data/ directory has .md files.")
        sys.exit(1)

    # Step 2: Chunk documents
    print("\n✂️  Step 2: Chunking documents...")
    chunks = chunk_documents(documents, chunk_size=1000, chunk_overlap=200)

    # Step 3: Create vector store
    print(f"\n🧮 Step 3: Creating embeddings & vector store...")
    print(f"   Model: {settings.EMBEDDING_MODEL}")
    print(f"   Persist directory: {settings.CHROMA_PERSIST_DIR}")

    vectorstore = create_vectorstore(
        documents=chunks,
        persist_dir=settings.CHROMA_PERSIST_DIR,
        embedding_model_name=settings.EMBEDDING_MODEL,
    )

    # Step 4: Verify
    print("\n🔍 Step 4: Verification...")
    test_queries = [
        "What is Utkersh's experience?",
        "Tell me about the Patient Management System",
        "What programming languages does Utkersh know?",
    ]
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    for query in test_queries:
        results = retriever.invoke(query)
        print(f"\n  Query: '{query}'")
        print(f"  Results: {len(results)} chunks retrieved")
        if results:
            source = results[0].metadata.get("source_name", "Unknown")
            preview = results[0].page_content[:100].replace("\n", " ")
            print(f"  Top result from: {source}")
            print(f"  Preview: {preview}...")

    print("\n" + "=" * 60)
    print("  ✅ Ingestion complete! You can now start the server:")
    print("  uvicorn backend.main:app --reload --port 8000")
    print("=" * 60)


if __name__ == "__main__":
    main()
