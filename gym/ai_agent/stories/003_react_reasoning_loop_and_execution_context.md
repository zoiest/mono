# Story 003: The ReAct Reasoning Loop & ExecutionContext Engine

## User Story
**As an** AI Agent developer,  
**I want to** implement the core ReAct (Thought-Action-Observation) reasoning engine powered by an `ExecutionContext` state container,  
**So that** the agent can autonomously reason about tasks, select and execute tools, process observations, and converge on final solutions while preventing runaway loops.

---

## 📖 Book Alignment
* **Book:** *Build an AI Agent (From Scratch)* ([Study Notes](../bin/build_an_ai_agent_notes.md#chapter-4-the-react-loop--executioncontext))
  - Chapter 4: *The ReAct loop* (4.1 Understanding ReAct, 4.5 ExecutionContext, 4.6 Implementing the agent: run, step, think, act)
* **Book:** *Effective Python (3rd Edition)* ([Study Notes](../bin/effective_python_v3_notes.md#chapter-1-pythonic-thinking))
  - **Item 8**: Prevent Repetition with Assignment Expressions (`:=` walrus operator)
  - **Item 9**: Consider `match` for Destructuring in Flow Control
  - **Item 19 & 20**: Avoid `else` Blocks After Loops; Never Use Loop Variables After the Loop Ends
  - **Item 21**: Be Defensive when Iterating over Arguments
  - **Item 80 & 87**: Take Advantage of Each Block in `try/except/else/finally`; Use traceback for Enhanced Reporting

---

## 🎯 What You Will Learn
1. Structuring `ExecutionContext` to encapsulate mutable agent runtime history and metadata cleanly.
2. Implementing the ReAct loop: `run()` -> `step()` -> `think()` -> `act()`.
3. Using structural pattern matching (`match...case`) on model finish reasons and tool call payloads.
4. Designing loop guards and thresholds to prevent infinite execution cycles.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Build the `ExecutionContext` State Container
In `src/agent/core/context.py`:
```python
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from agent.core.models import TokenUsage

@dataclass
class ExecutionStep:
    """Record of a single reasoning/action step (Item 31, 51)."""
    step_number: int
    thought: str | None
    tool_name: str | None = None
    tool_args: dict[str, Any] | None = None
    observation: str | None = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

class ExecutionContext:
    """Central nervous system of the agent storing messages and step histories (Ch 4.5)."""

    def __init__(self, system_prompt: str, user_prompt: str):
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        self.messages: list[dict[str, Any]] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        self.steps: list[ExecutionStep] = []
        self.cumulative_usage = TokenUsage()
        self.is_finished = False
        self.final_answer: str | None = None

    def add_assistant_message(self, content: str | None, tool_calls: list[Any] | None = None) -> None:
        msg: dict[str, Any] = {"role": "assistant"}
        if content:
            msg["content"] = content
        if tool_calls:
            msg["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {"name": tc.name, "arguments": str(tc.arguments)},
                }
                for tc in tool_calls
            ]
        self.messages.append(msg)

    def add_tool_observation(self, tool_call_id: str, name: str, observation: str) -> None:
        self.messages.append({
            "role": "tool",
            "tool_call_id": tool_call_id,
            "name": name,
            "content": observation,
        })
```

### 2. Implement the ReAct Agent Engine
In `src/agent/core/agent.py`:
```python
from agent.core.context import ExecutionContext, ExecutionStep
from agent.core.exceptions import AgentBaseException
from agent.core.models import ModelResponse
from agent.llm.client import LlmClient
from agent.tools.registry import ToolRegistry

class MaxIterationsError(AgentBaseException):
    """Raised when agent loop exceeds configured maximum iterations."""
    pass

class Agent:
    """Autonomous agent implementing the ReAct reasoning loop (Ch 4.6)."""

    def __init__(
        self,
        llm_client: LlmClient,
        tool_registry: ToolRegistry,
        *,
        system_prompt: str = "You are a helpful autonomous AI agent.",
        max_steps: int = 10,
    ):
        self.llm = llm_client
        self.tools = tool_registry
        self.system_prompt = system_prompt
        self.max_steps = max_steps

    async def run(self, prompt: str) -> str:
        """Runs the complete agent execution cycle until completion (Item 19)."""
        ctx = ExecutionContext(self.system_prompt, prompt)

        for step_idx in range(1, self.max_steps + 1):
            await self._step(ctx, step_idx)
            if ctx.is_finished:
                return ctx.final_answer or ""

        raise MaxIterationsError(f"Agent reached maximum iterations ({self.max_steps}) without finishing.")

    async def _step(self, ctx: ExecutionContext, step_idx: int) -> None:
        """Executes a single Think -> Act -> Observe cycle."""
        # 1. Think: call LLM with context messages and tool schemas
        schemas = self.tools.get_schemas()
        response: ModelResponse = await self.llm.complete(
            ctx.messages,
            tools=schemas if schemas else None,
        )

        # 2. Pattern match finish state (Item 9)
        match response.tool_calls:
            case []:
                # Model finished reasoning and returned final text
                ctx.is_finished = True
                ctx.final_answer = response.content
                ctx.add_assistant_message(response.content)
                ctx.steps.append(ExecutionStep(step_number=step_idx, thought=response.content))
            case list() as tool_calls:
                # 3. Act: Model emitted one or more tool calls
                ctx.add_assistant_message(response.content, tool_calls)
                for tc in tool_calls:
                    try:
                        observation = self.tools.execute(tc.name, tc.arguments)
                    except Exception as err:
                        observation = f"Error executing tool '{tc.name}': {err}"

                    ctx.add_tool_observation(tc.id, tc.name, observation)
                    ctx.steps.append(
                        ExecutionStep(
                            step_number=step_idx,
                            thought=response.content,
                            tool_name=tc.name,
                            tool_args=tc.arguments,
                            observation=observation,
                        )
                    )
```

---

## ✅ Acceptance Criteria
- [ ] `ExecutionContext` maintains clean separation between message history and structured step logs.
- [ ] Agent correctly executes the ReAct cycle (Think -> Act -> Observe).
- [ ] Pattern matching with `match...case` cleanly handles final answers vs tool calls.
- [ ] Loop guard raises `MaxIterationsError` if max step budget is exceeded.
