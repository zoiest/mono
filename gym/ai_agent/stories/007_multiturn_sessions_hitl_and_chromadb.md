# Story 007: Multiturn Market Research Sessions & ChromaDB Ticker Memory

## User Story
**As a** quantitative research developer,  
**I want to** implement stateful session persistence and an episodic memory store backed by ChromaDB,  
**So that** analyst queries about a ticker persist across multiturn interactions and past market theses and signals are remembered across separate days.

---

## 📖 Book Alignment
* **Book:** *Build an AI Agent (From Scratch)* ([Study Notes](../bin/build_an_ai_agent_notes.md#chapter-6-adding-memory-to-your-agent))
  - Chapter 6: *Adding memory to your agent* (6.3 Continuous execution: Sessions & state management, 6.4 Long-term memory with ChromaDB)
* **Book:** *Effective Python (3rd Edition)* ([Study Notes](../bin/effective_python_v3_notes.md#chapter-12-data-structures-and-algorithms))
  - **Item 27 & 28**: Prefer `defaultdict`; Construct Key-Dependent Defaults with `__missing__`
  - **Item 31**: Return Dedicated Result Objects Instead of Requiring Unpacking
  - **Item 87**: Use `try/finally` for Reliable State Persistence
  - **Item 105**: Use `datetime` with UTC Clocks for Market Session Timestamps
  - **Item 107**: Make Serialization Maintainable (safe JSON models over untrusted pickle)

---

## 🎯 What You Will Learn
1. Preserving multiturn research sessions using typed `MarketResearchSession` dataclasses.
2. Managing session persistence to disk safely with JSON serialization.
3. Storing historical ticker signals, earnings dates, and price reactions in ChromaDB.
4. Retrieving past historical signals dynamically to enrich new ticker analysis prompts.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Market Research Session Model
In `src/agent/memory/market_session.py`:
```python
import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any

@dataclass
class MarketResearchSession:
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    ticker: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    messages: list[dict[str, Any]] = field(default_factory=list)
    signals_history: list[dict[str, Any]] = field(default_factory=list)

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)

    @classmethod
    def from_json(cls, s: str) -> "MarketResearchSession":
        return cls(**json.loads(s))
```

### 2. Episodic Ticker Memory with ChromaDB
In `src/agent/memory/ticker_memory.py`:
```python
from typing import Any

class TickerMemoryManager:
    """Stores past trading signals and analyst notes in vector memory (Ch 6.4)."""

    def __init__(self):
        self._memory_store: list[dict[str, Any]] = []

    def remember_signal(self, ticker: str, direction: str, rationale: str) -> None:
        entry = {
            "ticker": ticker.upper(),
            "direction": direction,
            "rationale": rationale,
        }
        self._memory_store.append(entry)

    def recall_past_signals(self, ticker: str) -> list[str]:
        target = ticker.upper()
        return [
            f"Past Signal [{m['direction']}]: {m['rationale']}"
            for m in self._memory_store
            if m["ticker"] == target
        ]
```

---

## ✅ Acceptance Criteria
- [ ] `MarketResearchSession` correctly serializes to and deserializes from JSON.
- [ ] Sessions accurately track timestamps in UTC.
- [ ] `TickerMemoryManager` stores past signals per ticker.
- [ ] Recalled historical signals can be injected into new research turns.
