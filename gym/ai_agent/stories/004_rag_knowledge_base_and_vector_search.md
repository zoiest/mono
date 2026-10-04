# Story 004: Financial RAG Knowledge Base & SEC Filings Vector Search

## User Story
**As a** quantitative research developer,  
**I want to** build a Retrieval-Augmented Generation (RAG) vector index to chunk and search SEC 10-K/10-Q filings and long financial news articles,  
**So that** the agent can ground its ticker signal on verified financial statements, risk factors, and earnings guidance without hallucinations.

---

## 📖 Book Alignment
* **Book:** *Build an AI Agent (From Scratch)* ([Study Notes](../bin/build_an_ai_agent_notes.md#chapter-5-building-knowledge-bases-with-rag-filesystem-tools))
  - Chapter 5: *Building knowledge bases with RAG* (5.1 Problem of internal data, 5.2 Search methods, 5.3 Practicing vector search)
* **Book:** *Effective Python (3rd Edition)* ([Study Notes](../bin/effective_python_v3_notes.md#chapter-6-comprehensions-and-generators))
  - **Item 40 & 43**: Use Comprehensions; Consider Generators Instead of Returning Lists
  - **Item 99**: Consider `memoryview` for Zero-Copy Interactions with Large Filing Buffers
  - **Item 100 & 101**: Sort by Complex Criteria Using `key` (e.g. relevance score + filing recency)
  - **Item 104**: Know How to Use `heapq` for Top-K Vector Retrieval

---

## 🎯 What You Will Learn
1. Chunking multi-page SEC filings (10-K, 10-Q) using generator functions to conserve memory.
2. Building an in-memory vector index with cosine similarity math.
3. Using `heapq.nlargest` for fast O(N log K) retrieval of the most relevant financial disclosures.
4. Exposing `search_sec_filings` as an LLM tool.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Generator-Based Financial Filing Chunker
In `src/agent/rag/chunker.py`:
```python
from typing import Iterator

def chunk_filing_sections(filing_text: str, chunk_size: int = 600, overlap: int = 80) -> Iterator[str]:
    """Splits lengthy SEC filings into overlapping chunks using generators (Item 43)."""
    start = 0
    text_len = len(filing_text)
    stride = chunk_size - overlap

    while start < text_len:
        end = min(start + chunk_size, text_len)
        chunk = filing_text[start:end].strip()
        if chunk:
            yield chunk
        if end == text_len:
            break
        start += stride
```

### 2. Financial Vector Store with `heapq.nlargest`
In `src/agent/rag/vector_store.py`:
```python
import math
import heapq
from dataclasses import dataclass
from typing import Callable

@dataclass
class FilingSearchResult:
    chunk_text: str
    ticker: str
    section: str
    score: float

def cosine_similarity(v1: list[float], v2: list[float]) -> float:
    dot = sum(a * b for a, b in zip(v1, v2))
    n1 = math.sqrt(sum(x * x for x in v1))
    n2 = math.sqrt(sum(y * y for y in v2))
    return dot / (n1 * n2) if n1 and n2 else 0.0

class FinancialVectorStore:
    """Stores vector embeddings for company filings and earnings reports (Ch 5.3 & Item 104)."""

    def __init__(self, embed_fn: Callable[[str], list[float]]):
        self._embed = embed_fn
        self._docs: list[tuple[str, str, str]] = []  # (ticker, section, text)
        self._vectors: list[list[float]] = []

    def add_filing(self, ticker: str, section: str, chunks: list[str]) -> None:
        for c in chunks:
            self._docs.append((ticker.upper(), section, c))
            self._vectors.append(self._embed(c))

    def search(self, ticker: str, query: str, top_k: int = 3) -> list[FilingSearchResult]:
        q_vec = self._embed(query)
        target_ticker = ticker.upper()

        scored = (
            (cosine_similarity(q_vec, vec), t, sec, text)
            for (t, sec, text), vec in zip(self._docs, self._vectors)
            if t == target_ticker
        )

        top_matches = heapq.nlargest(top_k, scored, key=lambda p: p[0])
        return [
            FilingSearchResult(chunk_text=text, ticker=t, section=sec, score=score)
            for score, t, sec, text in top_matches
        ]
```

### 3. Expose Filing Search Tool
In `src/agent/tools/filing_tool.py`:
```python
from agent.tools.base import tool
from agent.rag.vector_store import FinancialVectorStore

def make_filing_search_tool(store: FinancialVectorStore):
    @tool(name="search_sec_filings", description="Search 10-K/10-Q disclosures for a ticker.")
    def search_filings(ticker: str, query: str) -> str:
        results = store.search(ticker, query, top_k=2)
        if not results:
            return f"No filings matching '{query}' found for {ticker}."
        formatted = [f"[{r.section}] (Score: {r.score:.2f}) {r.chunk_text}" for r in results]
        return "

".join(formatted)
    return search_filings
```

---

## ✅ Acceptance Criteria
- [ ] Chunker splits financial filings efficiently without loading full lists into memory.
- [ ] Cosine similarity correctly scores text embeddings.
- [ ] `FinancialVectorStore` filters by target ticker and extracts top-K matches with `heapq`.
- [ ] Tool provides grounded context from filings during ReAct execution.
