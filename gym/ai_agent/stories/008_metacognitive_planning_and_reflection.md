# Story 008: Metacognitive Task Planning, Decomposition & Reflection Engine

## User Story
**As an** AI Agent developer,  
**I want to** empower the agent with explicit task decomposition, milestone planning, and self-reflection tools,  
**So that** the agent can systematically solve complex multi-hop problems, monitor its own progress, detect errors, and recover from failures without user intervention.

---

## 📖 Book Alignment
* **Book:** *Build an AI Agent (From Scratch)* ([Study Notes](file:///home/tofunth/stuffs/mono/gym/ai_agent/bin/build_an_ai_agent_notes.md#chapter-7-planning-and-reflection-for-complex-tasks))
  - Chapter 7: *Planning and reflection for complex tasks* (7.1 Giving agents time to think, 7.2 Planning, 7.3 Reflection, 7.4 Integrating planning & reflection)
* **Book:** *Effective Python (3rd Edition)* ([Study Notes](file:///home/tofunth/stuffs/mono/gym/ai_agent/bin/effective_python_v3_notes.md#chapter-1-pythonic-thinking))
  - **Item 4**: Write Helper Functions Instead of Complex Expressions
  - **Item 9**: Consider `match` for Destructuring in Flow Control (plan state machine)
  - **Item 11**: Prefer Interpolated F-Strings over C-Style Formatting
  - **Item 31**: Return Dedicated Result Objects (`Plan`, `PlanStep`, `ReflectionReport`)
  - **Item 54**: Compose Functionality with Protocol / Mix-in Classes

---

## 🎯 What You Will Learn
1. Overcoming the myopic bias of pure ReAct loops using explicit planning decomposition.
2. Defining typed Plan and Step state machines (`Pending`, `In_Progress`, `Completed`, `Failed`).
3. Using `match...case` pattern matching on plan execution states.
4. Building a reflection tool for failure diagnosis and automated replanning.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Define Plan Data Models & State Enum
In `src/agent/planning/models.py`:
```python
from dataclasses import dataclass, field
from enum import Enum

class StepStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class PlanStep:
    step_id: int
    description: str
    status: StepStatus = StepStatus.PENDING
    result: str | None = None

@dataclass
class Plan:
    goal: str
    steps: list[PlanStep] = field(default_factory=list)

    def format_status(self) -> str:
        lines = [f"Goal: {self.goal}"]
        for s in self.steps:
            marker = {
                StepStatus.PENDING: "[ ]",
                StepStatus.IN_PROGRESS: "[>]",
                StepStatus.COMPLETED: "[X]",
                StepStatus.FAILED: "[!]",
            }[s.status]
            lines.append(f"{marker} Step {s.step_id}: {s.description}")
        return "
".join(lines)
```

### 2. Implement Planning and Reflection Tools
In `src/agent/planning/tools.py`:
```python
from agent.tools.base import tool
from agent.planning.models import Plan, PlanStep, StepStatus

class PlanningModule:
    """Provides planning and self-reflection tools to the agent (Ch 7)."""

    def __init__(self):
        self.current_plan: Plan | None = None

    def get_tools(self) -> list:
        @tool(name="create_plan", description="Create an initial multi-step execution plan.")
        def create_plan(goal: str, subtasks: list[str]) -> str:
            steps = [PlanStep(step_id=i+1, description=desc) for i, desc in enumerate(subtasks)]
            self.current_plan = Plan(goal=goal, steps=steps)
            return f"Plan initialized:
{self.current_plan.format_status()}"

        @tool(name="update_step_status", description="Update status of a plan step.")
        def update_step(step_id: int, status: str, result_summary: str = "") -> str:
            if not self.current_plan:
                return "Error: No active plan."
            target = next((s for s in self.current_plan.steps if s.step_id == step_id), None)
            if not target:
                return f"Error: Step {step_id} not found."

            match status.lower():  # Pattern matching on step status (Item 9)
                case "completed":
                    target.status = StepStatus.COMPLETED
                    target.result = result_summary
                case "failed":
                    target.status = StepStatus.FAILED
                    target.result = result_summary
                case "in_progress":
                    target.status = StepStatus.IN_PROGRESS
                case _:
                    return f"Unknown status: {status}"

            return f"Updated plan:
{self.current_plan.format_status()}"

        @tool(name="reflect_and_critique", description="Reflect on current findings and diagnose issues.")
        def reflect(current_observation: str, expected_outcome: str) -> str:
            # Reflection reasoning output
            return (
                f"Reflection Analysis:
"
                f"- Observation: {current_observation}
"
                f"- Expected: {expected_outcome}
"
                f"- Verdict: Continue to next step or adjust query."
            )

        return [create_plan, update_step, reflect]
```

---

## ✅ Acceptance Criteria
- [ ] Structured plan decomposes complex queries into ordered milestones.
- [ ] Step statuses transition cleanly between `Pending`, `In_Progress`, `Completed`, `Failed`.
- [ ] Pattern matching (`match...case`) handles state updates idiomatically.
- [ ] Reflection tool diagnoses failures and suggests corrections.
