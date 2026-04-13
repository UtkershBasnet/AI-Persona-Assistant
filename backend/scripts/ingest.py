"""
Inspection script — loads documents and chunks them to verify retrieval input.
Optional for deployment, useful for checking the knowledge base locally.
"""
import sys
import os

# Add project root to path so we can import backend modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.config import get_settings
from backend.rag.loader import load_documents, chunk_documents


def main():
    settings = get_settings()

    print("=" * 60)
    print("  📚 AI Persona — Knowledge Base Verification")
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

    # Step 3: Verify chunk coverage
    print("\n🔍 Step 3: Verification...")
    by_source = {}
    for chunk in chunks:
        source = chunk.metadata.get("source_name", "Unknown")
        by_source[source] = by_source.get(source, 0) + 1

    print(f"   Total chunks: {len(chunks)}")
    for source, count in sorted(by_source.items()):
        print(f"   - {source}: {count} chunks")

    print("\n" + "=" * 60)
    print("  ✅ Verification complete! You can now start the server:")
    print("  uvicorn backend.main:app --reload --port 8000")
    print("=" * 60)


if __name__ == "__main__":
    main()
