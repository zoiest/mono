# Story 008: Metacognitive Financial Task Planning & Signal Reflection

## User Story
**As a** quantitative research developer,  
**I want to** equip the agent with structured planning and self-reflection tools,  
**So that** complex multi-ticker inquiries (e.g. "Assess supply-chain contagion from NVDA earnings on TSM and ASML") are broken into disciplined research subtasks with automated error reflection.

---

## 📖 Book Alignment
* **Book:** *Build an AI Agent (From Scratch)* ([Study Notes](../bin/build_an_ai_agent_notes.md#chapter-7-planning-and-reflection-for-complex-tasks))
  - Chapter 7: *Planning and reflection for complex tasks* (7.1 Giving agents time to think, 7.2 Planning tool, 7.3 Reflection tool, 7.4 Failure recovery)
* **Book:** *Effective Python (3rd Edition)* ([Study Notes](../bin/effective_python_v3_notes.md#chapter-1-pythonic-thinking))
  - **Item 4**: Write Helper Functions Instead of Complex Expressions
  - **Item 9**: Consider `match` for Destructuring in Flow Control (plan step state matching)
  - **Item 11**: Prefer Interpolated F-Strings over C-Style Format Strings
  - **Item 31**: Return Dedicated Result Objects (`ResearchPlan`, `PlanStep`)

---

## 🎯 What You Will Learn
1. Mitigating next-step bias by introducing explicit milestone planning for complex equities.
2. Defining typed `Plan` state machines tracking multi-ticker research progress.
3. Using `match...case` to transition step statuses (`PENDING`, `INVESTIGATING`, `COMPLETED`, `FAILED`).
4. Creating a reflection tool to critique contradictory news signals before committing to a final signal.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Multi-Ticker Research Plan Models
In `src/agent/planning/financial_plan.py`:
```python
from dataclasses import dataclass, field
from enum import Enum

class ResearchStepStatus(str, Enum):
    PENDING = "pending"
    INVESTIGATING = "investigating"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class ResearchStep:
    step_id: int
    ticker: str
    objective: str
    status: ResearchStepStatus = ResearchStepStatus.PENDING
    findings: str | None = None

class FinancialResearchPlan:
    def __init__(self, overarching_thesis: str, subtasks: list[tuple[str, str]]):
        self.thesis = overarching_thesis
        self.steps = [
            ResearchStep(step_id=i+1, ticker=ticker, objective=obj)
            for i, (ticker, obj) in enumerate(subtasks)
        ]

    def update_step(self, step_id: int, status: str, findings: str) -> None:
        target = next((s for s in self.steps if s.step_id == step_id), None)
        if not target:
            return

        match status.lower():  # Pattern matching (Item 9)
            case "completed":
                target.status = ResearchStepStatus.COMPLETED
                target.findings = findings
            case "failed":
                target.status = ResearchStepStatus.FAILED
                target.findings = findings
            case "investigating":
                target.status = ResearchStepStatus.INVESTIGATING

    def format_plan(self) -> str:
        lines = [f"Thesis Goal: {self.thesis}"]
        for s in self.steps:
            lines.append(f"[{s.status.value.upper()}] Step {s.step_id} ({s.ticker}): {s.objective}")
        return "
".join(lines)
```

### 2. Implement Signal Reflection & Critique Tool
In `src/agent/planning/reflection.py`:
```python
from agent.tools.base import tool

@tool(name="reflect_on_signals", description="Critique conflicting news vs financial metrics.")
def reflect_on_signals(bullish_catalysts: str, bearish_catalysts: str) -> str:
    """Synthesizes conflicting market news to produce a calibrated confidence score."""
    return (
        f"Reflection Analysis:
"
        f"- Bullish factors evaluated: {bullish_catalysts}
"
        f"- Bearish factors evaluated: {bearish_catalysts}
"
        f"- Recommendation: Verify guidance statements before issuing directional signal."
    )
```

---

## ✅ Acceptance Criteria
- [ ] Structured plan decomposes multi-ticker research into ordered steps.
- [ ] Step transitions handled cleanly using `match...case`.
- [ ] Reflection tool evaluates competing bullish and bearish catalysts.
- [ ] Final plan output presents clear verification status.
