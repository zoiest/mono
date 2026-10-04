# Story 006: Context Engineering, Sliding Windows & News Stream Compactor

## User Story
**As a** quantitative research developer,  
**I want to** implement context engineering with sliding windows and headline compaction,  
**So that** the agent can digest hundreds of real-time financial news alerts for a ticker without exceeding LLM context windows or incurring runaway token costs.

---

## 📖 Book Alignment
* **Book:** *Build an AI Agent (From Scratch)* ([Study Notes](../writings/build_an_ai_agent_notes.md#chapter-6-adding-memory-to-your-agent))
  - Chapter 6: *Adding memory to your agent* (6.1 Anatomy of memory, 6.2 Managing context: sliding windows, compaction, summarization)
* **Book:** *Effective Python (3rd Edition)* ([Study Notes](../writings/effective_python_v3_notes.md#chapter-12-data-structures-and-algorithms))
  - **Item 4**: Write Helper Functions Instead of Complex Expressions
  - **Item 22**: Never Modify Containers While Iterating over Them (safe news compaction)
  - **Item 23**: Pass Iterators to `any` and `all` for Short-Circuiting
  - **Item 103**: Prefer `collections.deque` for Producer-Consumer Queues and Bounded Buffers
  - **Item 115**: Use `tracemalloc` to Verify Memory Retention

---

## 🎯 What You Will Learn
1. Using `collections.deque(maxlen=K)` to build bounded short-term news memory buffers.
2. Compacting noisy headline paragraphs into concise market catalyst summaries.
3. Preserving core ticker instructions while evicting stale news observations.
4. Profiling memory stability during continuous streaming runs using `tracemalloc`.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Sliding Window News Memory Buffer
In `src/agent/memory/news_buffer.py`:
```python
from collections import deque
from typing import Any

class TickerNewsBuffer:
    """Maintains bounded recent news context for a ticker using deque (Ch 6.2 & Item 103)."""

    def __init__(self, ticker: str, max_articles: int = 5):
        self.ticker = ticker.upper()
        self.system_prompt: dict[str, str] = {
            "role": "system",
            "content": f"You are evaluating market sentiment for ticker {self.ticker}.",
        }
        # Automatic O(1) eviction of oldest articles
        self.recent_articles: deque[dict[str, Any]] = deque(maxlen=max_articles)

    def push_article(self, headline: str, summary: str, source: str) -> None:
        self.recent_articles.append({
            "role": "user",
            "content": f"[{source}] {headline} -- {summary}",
        })

    def export_prompt_context(self) -> list[dict[str, str]]:
        context = [self.system_prompt]
        context.extend(list(self.recent_articles))
        return context
```

### 2. Financial Catalyst Compactor
In `src/agent/memory/compactor.py`:
```python
class FinancialNewsCompactor:
    """Compacts repetitive earnings and analyst noise into distilled catalyst bullets (Ch 6.2)."""

    def __init__(self, max_length: int = 200):
        self.max_length = max_length

    def compact_news_list(self, articles: list[str]) -> list[str]:
        compacted: list[str] = []
        for art in articles:  # Safe iteration without container mutation (Item 22)
            if len(art) > self.max_length:
                compacted.append(art[:self.max_length] + " [Compacted]")
            else:
                compacted.append(art)
        return compacted
```

---

## ✅ Acceptance Criteria
- [ ] `TickerNewsBuffer` automatically evicts older articles via `collections.deque(maxlen=K)`.
- [ ] System prompt remains pinned at the start of context.
- [ ] Compactor condenses verbose news feeds without modifying original input lists in place.
- [ ] Memory utilization stays constant under 1,000 simulated headline arrivals.
