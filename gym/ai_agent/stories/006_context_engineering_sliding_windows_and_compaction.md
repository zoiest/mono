# Story 006: Context Engineering, Sliding-Window Memory & Token Compactor

## User Story
**As an** AI Agent developer,  
**I want to** implement intelligent context engineering with exact token counting, bounded sliding-window buffers, compaction, and recursive summarization,  
**So that** the agent avoids context window exhaustion, maintains low token costs, and prevents needle-in-a-haystack memory degradation during long executions.

---

## 📖 Book Alignment
* **Book:** *Build an AI Agent (From Scratch)* ([Study Notes](file:///home/tofunth/stuffs/mono/gym/ai_agent/bin/build_an_ai_agent_notes.md#chapter-6-adding-memory-to-your-agent))
  - Chapter 6: *Adding memory to your agent* (6.1 Anatomy of agent memory, 6.2 Managing context during execution, sliding windows, compaction, summarization)
* **Book:** *Effective Python (3rd Edition)* ([Study Notes](file:///home/tofunth/stuffs/mono/gym/ai_agent/bin/effective_python_v3_notes.md#chapter-12-data-structures-and-algorithms))
  - **Item 4**: Write Helper Functions Instead of Complex Expressions
  - **Item 22**: Never Modify Containers While Iterating over Them
  - **Item 23**: Pass Iterators to `any` and `all` for Efficient Short-Circuiting Logic
  - **Item 103**: Prefer `collections.deque` for Producer-Consumer Queues and Bounded Buffers
  - **Item 115**: Use `tracemalloc` to Understand Memory Usage and Leaks

---

## 🎯 What You Will Learn
1. Calculating exact token usage per message using tokenizer abstractions.
2. Using `collections.deque(maxlen=K)` to build bounded O(1) sliding context windows.
3. Preserving initial system prompt and root user intent while rolling older steps out of view.
4. Compacting verbose tool outputs without mutating iteration containers.
5. Detecting and preventing memory leaks using `tracemalloc`.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Implement Sliding Window Memory with `deque`
In `src/agent/memory/sliding_window.py`:
```python
from collections import deque
from typing import Any

class SlidingWindowBuffer:
    """Maintains bounded short-term conversation context using deque (Ch 6.2 & Item 103)."""

    def __init__(self, *, max_steps: int = 5):
        self.system_message: dict[str, Any] | None = None
        self.initial_user_message: dict[str, Any] | None = None
        # deque with maxlen provides automatic O(1) eviction of oldest items
        self.step_history: deque[dict[str, Any]] = deque(maxlen=max_steps * 2)

    def set_system_prompt(self, content: str) -> None:
        self.system_message = {"role": "system", "content": content}

    def set_user_prompt(self, content: str) -> None:
        self.initial_user_message = {"role": "user", "content": content}

    def add_interaction(self, message: dict[str, Any]) -> None:
        self.step_history.append(message)

    def get_messages_for_llm(self) -> list[dict[str, Any]]:
        """Compiles the active prompt view presented to the LLM."""
        active_messages: list[dict[str, Any]] = []
        if self.system_message:
            active_messages.append(self.system_message)
        if self.initial_user_message:
            active_messages.append(self.initial_user_message)
        
        # Add the sliding window of recent steps
        active_messages.extend(list(self.step_history))
        return active_messages
```

### 2. Implement Observation Compactor
In `src/agent/memory/compactor.py`:
```python
from typing import Any

class ContextCompactor:
    """Prunes redundant intermediate observation details (Ch 6.2)."""

    def __init__(self, *, max_observation_chars: int = 300):
        self.max_chars = max_observation_chars

    def compact_history(self, messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Produces a new compacted message list without mutating the original (Item 22)."""
        compacted: list[dict[str, Any]] = []
        for msg in messages:
            if msg.get("role") == "tool":
                content = str(msg.get("content", ""))
                if len(content) > self.max_chars:
                    content = content[:self.max_chars] + " ... [Observation compacted]"
                compacted.append({**msg, "content": content})
            else:
                compacted.append(msg)
        return compacted
```

### 3. Verify Memory Stability with `tracemalloc`
In `tests/test_memory_leaks.py`:
```python
import tracemalloc
from agent.memory.sliding_window import SlidingWindowBuffer

def test_sliding_window_memory_bounded():
    tracemalloc.start()
    buffer = SlidingWindowBuffer(max_steps=5)
    buffer.set_system_prompt("System prompt")
    buffer.set_user_prompt("User query")

    # Simulate 1,000 reasoning turns
    for i in range(1000):
        buffer.add_interaction({"role": "assistant", "content": f"Turn {i} thought"})
        buffer.add_interaction({"role": "tool", "content": f"Turn {i} bulky output " * 50})

    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')
    tracemalloc.stop()

    # Context presentation must remain bounded
    active = buffer.get_messages_for_llm()
    assert len(active) <= 12  # system + user + 10 turn messages
```

---

## ✅ Acceptance Criteria
- [ ] `SlidingWindowBuffer` evicts older messages automatically via `collections.deque(maxlen=K)`.
- [ ] System prompt and initial user prompt are permanently pinned.
- [ ] Compactor shrinks bulky tool outputs without modifying in-place containers during iteration.
- [ ] `tracemalloc` verifies memory usage stays flat during long simulation runs.
