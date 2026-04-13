"""
Document loader — reads resume.md and all GitHub repo markdown files,
then chunks them for embedding.
"""
import os
from typing import List
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


def load_documents(data_dir: str = "./data") -> List[Document]:
    """Load all markdown documents from the data directory."""
    documents: List[Document] = []

    # 1. Load resume
    resume_path = os.path.join(data_dir, "resume.md")
    if os.path.exists(resume_path):
        loader = TextLoader(resume_path, encoding="utf-8")
        docs = loader.load()
        for doc in docs:
            doc.metadata["source_type"] = "resume"
            doc.metadata["source_name"] = "Utkersh Basnet Resume"
        documents.extend(docs)
        print(f"  ✓ Loaded resume: {resume_path}")

    # 2. Load combined GitHub context
    github_context_path = os.path.join(data_dir, "github_context.md")
    if os.path.exists(github_context_path):
        loader = TextLoader(github_context_path, encoding="utf-8")
        docs = loader.load()
        for doc in docs:
            doc.metadata["source_type"] = "github_combined"
            doc.metadata["source_name"] = "GitHub Repositories Overview"
        documents.extend(docs)
        print(f"  ✓ Loaded GitHub context: {github_context_path}")

    # 3. Load individual GitHub repo files
    github_dir = os.path.join(data_dir, "github")
    if os.path.exists(github_dir):
        for filename in sorted(os.listdir(github_dir)):
            if filename.endswith(".md"):
                filepath = os.path.join(github_dir, filename)
                repo_name = filename.replace(".md", "")
                try:
                    loader = TextLoader(filepath, encoding="utf-8")
                    docs = loader.load()
                    for doc in docs:
                        doc.metadata["source_type"] = "github_repo"
                        doc.metadata["source_name"] = repo_name
                    documents.extend(docs)
                    print(f"  ✓ Loaded repo: {repo_name}")
                except Exception as e:
                    print(f"  ✗ Failed to load {filepath}: {e}")

    print(f"\n  Total documents loaded: {len(documents)}")
    return documents


def chunk_documents(
    documents: List[Document],
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> List[Document]:
    """Split documents into chunks for embedding."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n## ", "\n### ", "\n---", "\n\n", "\n", ". ", " "],
        length_function=len,
    )
    chunks = splitter.split_documents(documents)
    print(f"  Split into {len(chunks)} chunks (size={chunk_size}, overlap={chunk_overlap})")
    return chunks
