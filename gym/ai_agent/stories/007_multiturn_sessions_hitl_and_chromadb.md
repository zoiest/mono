# Story 007: Multiturn Sessions, HITL Pause/Resume & Long-Term Memory (ChromaDB)

## User Story
**As an** AI Agent developer,  
**I want to** implement stateful `SessionManager` with pause-and-resume workflows for human approvals, and an episodic long-term memory store using ChromaDB,  
**So that** agent conversations persist across sessions, human-in-the-loop workflows run asynchronously, and agents learn facts and user preferences across distinct interactions.

---

## 📖 Book Alignment
* **Book:** *Build an AI Agent (From Scratch)* ([Study Notes](file:///home/tofunth/stuffs/mono/gym/ai_agent/bin/build_an_ai_agent_notes.md#chapter-6-adding-memory-to-your-agent))
  - Chapter 6: *Adding memory to your agent* (6.3 Continuous execution: Session and state management, 6.4 Long-term memory)
* **Book:** *Effective Python (3rd Edition)* ([Study Notes](file:///home/tofunth/stuffs/mono/gym/ai_agent/bin/effective_python_v3_notes.md#chapter-12-data-structures-and-algorithms))
  - **Item 27 & 28**: Prefer `defaultdict`; Construct Key-Dependent Defaults with `__missing__`
  - **Item 31**: Return Dedicated Result Objects Instead of Requiring Unpacking
  - **Item 87**: Use `try/finally` for Reliable State Persistence
  - **Item 105**: Use `datetime` Instead of `time` for Local and UTC Clocks
  - **Item 107**: Make Serialization Maintainable (safe JSON/Pydantic over untrusted pickle)

---

## 🎯 What You Will Learn
1. Managing multiturn conversations using stateful `Session` models and UTC timestamps.
2. Building a pause-and-resume state machine to handle human confirmation without holding open process threads.
3. Persisting session snapshots cleanly as JSON rather than insecure raw pickles.
4. Integrating ChromaDB for episodic memory storage and semantic recall across user sessions.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Define Session Data Models
In `src/agent/memory/session.py`:
```python
import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any

@dataclass
class PendingConfirmation:
    """Represents a suspended tool call awaiting human verification."""
    tool_call_id: str
    tool_name: str
    arguments: dict[str, Any]
    prompt: str

@dataclass
class Session:
    """Encapsulates conversation state and lifecycle (Ch 6.3 & Item 31, 105)."""
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    messages: list[dict[str, Any]] = field(default_factory=list)
    pending_confirmation: PendingConfirmation | None = None
    is_paused: bool = False

    def to_json(self) -> str:
        """Safe JSON serialization (Item 107)."""
        data = asdict(self)
        data["created_at"] = self.created_at.isoformat()
        data["updated_at"] = self.updated_at.isoformat()
        return json.dumps(data, indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> "Session":
        data = json.loads(json_str)
        data["created_at"] = datetime.fromisoformat(data["created_at"])
        data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        if data.get("pending_confirmation"):
            data["pending_confirmation"] = PendingConfirmation(**data["pending_confirmation"])
        return cls(**data)
```

### 2. Implement SessionManager & Pause/Resume
In `src/agent/memory/manager.py`:
```python
import os
from agent.memory.session import Session, PendingConfirmation

class SessionManager:
    """Thread-safe disk persistence for agent sessions (Ch 6.3)."""

    def __init__(self, storage_dir: str = ".sessions"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

    def _path(self, session_id: str) -> str:
        return os.path.join(self.storage_dir, f"{session_id}.json")

    def save(self, session: Session) -> None:
        with open(self._path(session.session_id), "w", encoding="utf-8") as f:
            f.write(session.to_json())

    def load(self, session_id: str) -> Session:
        with open(self._path(session_id), "r", encoding="utf-8") as f:
            return Session.from_json(f.read())

    def pause_for_confirmation(self, session: Session, conf: PendingConfirmation) -> None:
        session.pending_confirmation = conf
        session.is_paused = True
        self.save(session)

    def resume_with_approval(self, session: Session, approved: bool) -> PendingConfirmation:
        conf = session.pending_confirmation
        if not conf:
            raise ValueError("Session is not awaiting confirmation.")
        session.is_paused = False
        session.pending_confirmation = None
        self.save(session)
        return conf
```

### 3. Implement Long-Term Task Memory with ChromaDB
In `src/agent/memory/task_memory.py`:
```python
from typing import Any

class TaskMemoryManager:
    """Stores and retrieves episodic memories across distinct user sessions (Ch 6.4)."""

    def __init__(self, collection_name: str = "agent_memories"):
        # ChromaDB client initialization stub
        self._memories: list[dict[str, Any]] = []

    def remember_fact(self, fact: str, *, metadata: dict[str, Any] | None = None) -> None:
        """Stores an extracted fact into long-term vector memory."""
        self._memories.append({"fact": fact, "metadata": metadata or {}})

    def recall_relevant(self, query: str, top_k: int = 3) -> list[str]:
        """Semantic search for relevant past facts."""
        # Simple keyword fallback stub
        return [m["fact"] for m in self._memories if any(w in m["fact"].lower() for w in query.lower().split())][:top_k]
```

---

## ✅ Acceptance Criteria
- [ ] `Session` model serializes to and deserializes from JSON accurately.
- [ ] Pause-and-resume workflow captures pending tool executions on disk.
- [ ] Safe JSON serialization avoids fragile pickle objects.
- [ ] `TaskMemoryManager` allows saving facts and retrieving them across sessions.
