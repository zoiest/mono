# Story 005: Financial Filesystem Tools & Signal Alert Approvals

## User Story
**As a** quantitative research developer,  
**I want to** give the agent safe filesystem tools to inspect market data CSVs/reports and implement human approval callbacks before emitting high-risk trade signals,  
**So that** local research files are parsed safely while preventing rogue or unverified automated orders from executing.

---

## 📖 Book Alignment
* **Book:** *Build an AI Agent (From Scratch)* ([Study Notes](../bin/build_an_ai_agent_notes.md#chapter-5-building-knowledge-bases-with-rag-filesystem-tools))
  - Chapter 5: *Building knowledge bases with RAG* (5.4 Structure-based search, 5.5 Extending agents with callbacks, human-in-the-loop approvals)
* **Book:** *Effective Python (3rd Edition)* ([Study Notes](../bin/effective_python_v3_notes.md#chapter-5-functions))
  - **Item 33**: Know How Closures Interact with Variable Scope and `nonlocal`
  - **Item 39**: Prefer `functools.partial` over lambda Expressions for Callback Handlers
  - **Item 86**: Consider `contextlib` and `with` Statements for Reusable Setup/Teardown
  - **Item 110**: Isolate Tests from Each Other with `setUp`, `tearDown`, and `tmp_path` Fixtures

---

## 🎯 What You Will Learn
1. Building safe market data filesystem tools with directory traversal guards.
2. Unpacking and parsing historical ticker archive packages (`.zip` / `.csv`).
3. Implementing lifecycle event hooks (`on_signal_generated`, `on_tool_call`).
4. Building a Human-in-the-Loop (HITL) approval gate for trades exceeding risk thresholds.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Build Safe Market Data Filesystem Tools
In `src/agent/tools/market_fs.py`:
```python
import os
import csv
from agent.tools.base import tool, ToolExecutionError

class SafeMarketDataWorkspace:
    def __init__(self, root_dir: str):
        self.root_dir = os.path.realpath(root_dir)

    def resolve(self, path: str) -> str:
        real = os.path.realpath(os.path.join(self.root_dir, path))
        if not real.startswith(self.root_dir):
            raise ToolExecutionError(f"Access denied: path '{path}' escapes market data directory.")
        return real

def make_market_fs_tools(ws: SafeMarketDataWorkspace):
    @tool(name="read_price_csv", description="Inspect recent OHLCV prices from ticker CSV file.")
    def read_csv(filename: str, rows: int = 5) -> str:
        path = ws.resolve(filename)
        try:
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                header = next(reader)
                data = [next(reader) for _ in range(rows)]
                return f"Columns: {header}
First {rows} records:
" + "
".join(str(r) for r in data)
        except Exception as e:
            raise ToolExecutionError(f"Failed to read CSV '{filename}': {e}") from e

    return [read_csv]
```

### 2. Implement Human Approval Callback for High-Risk Signals
In `src/agent/core/callbacks.py`:
```python
from typing import Callable
from agent.core.models import SentimentSignal

class TradeAlertGate:
    """Human approval callback intercepting high-conviction market signals (Ch 5.5)."""

    def __init__(self, min_confidence_threshold: float = 0.85):
        self.threshold = min_confidence_threshold
        self.approvals_log: list[str] = []

    def make_approval_callback(self, confirm_fn: Callable[[str], bool]):
        def on_signal(signal: SentimentSignal) -> bool:
            if signal.confidence >= self.threshold:
                prompt = f"ATTENTION: {signal.direction.value} signal generated for {signal.ticker} with {signal.confidence*100:.1f}% confidence. Approve?"
                approved = confirm_fn(prompt)
                status = "APPROVED" if approved else "REJECTED"
                self.approvals_log.append(f"{signal.ticker}: {status}")
                return approved
            return True
        return on_signal
```

---

## ✅ Acceptance Criteria
- [ ] `SafeMarketDataWorkspace` prevents access outside the designated market data directory.
- [ ] `read_price_csv` parses historical pricing rows without memory overhead.
- [ ] High-confidence signals trigger the human approval callback.
- [ ] Rejection halts execution and prevents unverified orders.
