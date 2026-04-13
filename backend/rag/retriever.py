"""
Lightweight keyword-based retriever for free hosting environments.
"""
import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import List

from langchain.schema import Document

from .loader import load_documents, chunk_documents

TOKEN_PATTERN = re.compile(r"[a-z0-9_+#.-]+")


def _tokenize(text: str) -> list[str]:
    return TOKEN_PATTERN.findall(text.lower())


@dataclass
class IndexedChunk:
    document: Document
    term_counts: Counter
    length: int
    text_lower: str


class LightweightRetriever:
    """Simple TF-IDF-style retriever with phrase boosting."""

    def __init__(self, chunks: List[Document]):
        self.chunks = chunks
        self.index: list[IndexedChunk] = []
        self.doc_freqs: Counter = Counter()
        self.avg_length = 0.0

        total_length = 0
        for chunk in chunks:
            tokens = _tokenize(chunk.page_content)
            counts = Counter(tokens)
            total_length += max(len(tokens), 1)
            self.index.append(
                IndexedChunk(
                    document=chunk,
                    term_counts=counts,
                    length=max(len(tokens), 1),
                    text_lower=chunk.page_content.lower(),
                )
            )
            for term in counts:
                self.doc_freqs[term] += 1

        self.avg_length = total_length / max(len(self.index), 1)

    @classmethod
    def from_data_dir(
        cls,
        data_dir: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ) -> "LightweightRetriever":
        documents = load_documents(data_dir=data_dir)
        if not documents:
            raise FileNotFoundError(
                f"No documents found in {data_dir}. Populate the data directory first."
            )
        chunks = chunk_documents(
            documents,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        return cls(chunks)

    def invoke(self, query: str, k: int = 6) -> List[Document]:
        query_tokens = _tokenize(query)
        if not query_tokens:
            return []

        query_terms = Counter(query_tokens)
        total_docs = len(self.index)
        scored: list[tuple[float, Document]] = []

        for chunk in self.index:
            score = 0.0
            for term, qtf in query_terms.items():
                tf = chunk.term_counts.get(term, 0)
                if not tf:
                    continue
                df = self.doc_freqs.get(term, 1)
                idf = math.log((total_docs + 1) / df)
                norm = 0.75 + 0.25 * (chunk.length / max(self.avg_length, 1))
                score += (tf / norm) * idf * qtf

            if query.lower() in chunk.text_lower:
                score += 3.0

            if score > 0:
                scored.append((score, chunk.document))

        scored.sort(key=lambda item: item[0], reverse=True)
        return [doc for _, doc in scored[:k]]
