# Story 004: RAG Knowledge Base, Vector Search & Text Chunking Pipeline

## User Story
**As an** AI Agent developer,  
**I want to** build a Retrieval-Augmented Generation (RAG) subsystem with text chunking, embedding generation, and vector similarity search,  
**So that** the agent can ground its reasoning and tool answers on external documents, knowledge bases, and fetched web content without hallucinating.

---

## 📖 Book Alignment
* **Book:** *Build an AI Agent (From Scratch)* ([Study Notes](../bin/build_an_ai_agent_notes.md#chapter-5-building-knowledge-bases-with-rag--filesystem-tools))
  - Chapter 5: *Building knowledge bases with RAG* (5.1 Problem of internal data, 5.2 Search methods, 5.3 Practicing vector search)
* **Book:** *Effective Python (3rd Edition)* ([Study Notes](../bin/effective_python_v3_notes.md#chapter-6-comprehensions-and-generators))
  - **Item 40 & 43**: Use Comprehensions; Consider Generators Instead of Returning Lists
  - **Item 99**: Consider `memoryview` and `bytearray` for Zero-Copy Interactions
  - **Item 100 & 101**: Sort by Complex Criteria Using `key`; Know the Difference Between `sort` and `sorted`
  - **Item 104**: Know How to Use `heapq` for Priority Queues / Top-K Selection

---

## 🎯 What You Will Learn
1. Using Python generators (`yield`) to chunk large text streams lazily without high memory usage.
2. Generating dense vector embeddings for text chunks.
3. Implementing an in-memory vector store using cosine similarity math.
4. Using `heapq.nlargest` to retrieve top-K relevant chunks in O(N log K) time.
5. Exposing vector search to the agent as a tool.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Implement Memory-Efficient Text Chunker
In `src/agent/rag/chunker.py`:
```python
from typing import Iterator

def chunk_text_sliding_window(
    text: str,
    *,
    chunk_size: int = 500,
    overlap: int = 50
) -> Iterator[str]:
    """Generates text chunks using a sliding window with overlap (Effective Python Item 43)."""
    start = 0
    text_len = len(text)
    stride = chunk_size - overlap

    while start < text_len:
        end = min(start + chunk_size, text_len)
        chunk = text[start:end].strip()
        if chunk:
            yield chunk
        if end == text_len:
            break
        start += stride
```

### 2. Implement In-Memory Vector Store with `heapq`
In `src/agent/rag/vector_store.py`:
```python
import math
import heapq
from dataclasses import dataclass
from typing import Callable

@dataclass
class SearchResult:
    text: str
    score: float

def cosine_similarity(v1: list[float], v2: list[float]) -> float:
    dot = sum(a * b for a, b in zip(v1, v2))
    norm_a = math.sqrt(sum(a * a for a in v1))
    norm_b = math.sqrt(sum(b * b for b in v2))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)

class SimpleVectorStore:
    """In-memory vector store with top-K retrieval via heapq (Ch 5.3 & Item 104)."""

    def __init__(self, embed_fn: Callable[[str], list[float]]):
        self._embed = embed_fn
        self._docs: list[str] = []
        self._vectors: list[list[float]] = []

    def add_texts(self, texts: list[str]) -> None:
        for t in texts:
            self._docs.append(t)
            self._vectors.append(self._embed(t))

    def search(self, query: str, top_k: int = 3) -> list[SearchResult]:
        query_vec = self._embed(query)
        scored = (
            (cosine_similarity(query_vec, doc_vec), doc)
            for doc, doc_vec in zip(self._docs, self._vectors)
        )
        # Use heapq.nlargest for O(N log K) top-K selection (Item 104)
        top_items = heapq.nlargest(top_k, scored, key=lambda pair: pair[0])
        return [SearchResult(text=doc, score=score) for score, doc in top_items]
```

### 3. Expose RAG Tool to Agent
In `src/agent/tools/rag_tool.py`:
```python
from agent.tools.base import tool
from agent.rag.vector_store import SimpleVectorStore

def make_knowledge_tool(vector_store: SimpleVectorStore):
    @tool(name="knowledge_base_search", description="Search internal documentation for relevant facts.")
    def search_kb(query: str) -> str:
        results = vector_store.search(query, top_k=2)
        if not results:
            return "No matching internal documents found."
        formatted = [f"[{i+1}] (Score: {r.score:.2f}) {r.text}" for i, r in enumerate(results)]
        return "
".join(formatted)
    return search_kb
```

---

## ✅ Acceptance Criteria
- [ ] Text chunker yields chunks without allocating entire chunk lists in memory.
- [ ] Cosine similarity correctly ranks identical texts with score 1.0.
- [ ] `SimpleVectorStore.search` leverages `heapq.nlargest` for top-K extraction.
- [ ] Knowledge base tool integrates into `ToolRegistry` and provides factual grounding.
