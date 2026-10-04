# Story 003: Financial ReAct Reasoning Engine & Signal Extraction

## User Story
**As a** quantitative research developer,  
**I want to** build a ReAct (Thought-Action-Observation) reasoning engine powered by an `ExecutionContext`,  
**So that** the agent can take a stock ticker, decide which news feeds and valuation metrics to query, synthesize observations, and output a validated trading signal.

---

## 📖 Book Alignment
* **Book:** *Build an AI Agent (From Scratch)* ([Study Notes](../writings/build_an_ai_agent_notes.md#chapter-4-the-react-loop-executioncontext))
  - Chapter 4: *The ReAct loop* (4.1 Understanding ReAct, 4.5 ExecutionContext, 4.6 Implementing the agent: run, step, think, act, 4.7 Structured output)
* **Book:** *Effective Python (3rd Edition)* ([Study Notes](../writings/effective_python_v3_notes.md#chapter-1-pythonic-thinking))
  - **Item 8**: Prevent Repetition with Assignment Expressions (`:=` walrus operator)
  - **Item 9**: Consider `match` for Destructuring in Flow Control (signal state matching)
  - **Item 19 & 20**: Avoid `else` Blocks After Loops; Never Use Loop Variables After the Loop Ends
  - **Item 21**: Be Defensive when Iterating over Message Histories
  - **Item 80 & 87**: Take Advantage of Each Block in `try/except/else/finally`

---

## 🎯 What You Will Learn
1. Designing the `ExecutionContext` to track news queries, model thoughts, and observations.
2. Implementing the financial ReAct loop: `run()` -> `step()` -> `think()` -> `act()`.
3. Pattern matching with `match...case` on model responses (tool calls vs final signal).
4. Guarding against endless search loops with `max_iterations` and loop detection.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Build the Financial `ExecutionContext`
In `src/agent/core/context.py`:
```python
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from agent.core.models import SentimentSignal

@dataclass
class FinancialStepRecord:
    step_number: int
    thought: str | None
    tool_name: str | None = None
    tool_args: dict[str, Any] | None = None
    observation: str | None = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

class ExecutionContext:
    """Tracks the market analysis context and extracted signal (Ch 4.5)."""

    def __init__(self, ticker: str, system_prompt: str, user_prompt: str):
        self.ticker = ticker.upper()
        self.messages: list[dict[str, Any]] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        self.steps: list[FinancialStepRecord] = []
        self.is_finished: bool = False
        self.final_signal: SentimentSignal | None = None
        self.final_answer: str | None = None

    def add_assistant_turn(self, content: str | None, tool_calls: list[Any] | None = None) -> None:
        msg: dict[str, Any] = {"role": "assistant"}
        if content:
            msg["content"] = content
        if tool_calls:
            msg["tool_calls"] = [
                {"id": tc.id, "type": "function", "function": {"name": tc.name, "arguments": str(tc.arguments)}}
                for tc in tool_calls
            ]
        self.messages.append(msg)

    def add_observation(self, tool_call_id: str, name: str, observation: str) -> None:
        self.messages.append({"role": "tool", "tool_call_id": tool_call_id, "name": name, "content": observation})
```

### 2. Implement Financial Signal ReAct Agent
In `src/agent/core/agent.py`:
```python
from agent.core.context import ExecutionContext, FinancialStepRecord
from agent.core.models import SentimentSignal, SignalDirection
from agent.llm.client import LlmClient
from agent.tools.registry import ToolRegistry

FINANCIAL_SYSTEM_PROMPT = """You are an autonomous equity research AI agent.
Your goal is to gather recent news and fundamentals for the requested ticker,
analyze the catalysts, and extract a definitive sentiment signal (BULLISH, BEARISH, NEUTRAL)."""

class FinancialReActAgent:
    def __init__(self, llm: LlmClient, tools: ToolRegistry, *, max_steps: int = 8):
        self.llm = llm
        self.tools = tools
        self.max_steps = max_steps

    async def analyze_ticker(self, ticker: str) -> str:
        prompt = f"Analyze ticker {ticker}. Fetch recent news and output your signal."
        ctx = ExecutionContext(ticker, FINANCIAL_SYSTEM_PROMPT, prompt)

        for step_idx in range(1, self.max_steps + 1):
            response = await self.llm.complete(ctx.messages, tools=self.tools.get_schemas())

            match response.tool_calls:  # Pattern matching (Item 9)
                case []:
                    # Reasoning completed, final analysis produced
                    ctx.is_finished = True
                    ctx.final_answer = response.content
                    return response.content or "Analysis complete."
                case list() as tool_calls:
                    ctx.add_assistant_turn(response.content, tool_calls)
                    for tc in tool_calls:
                        try:
                            obs = self.tools.execute(tc.name, tc.arguments)
                        except Exception as e:
                            obs = f"Tool failure: {e}"
                        ctx.add_observation(tc.id, tc.name, obs)
                        ctx.steps.append(FinancialStepRecord(step_idx, response.content, tc.name, tc.arguments, obs))

        raise RuntimeError(f"Analysis for {ticker} exceeded {self.max_steps} steps.")
```

---

## ✅ Acceptance Criteria
- [ ] `ExecutionContext` stores step records and message turns.
- [ ] Agent autonomously requests `fetch_ticker_news` for the target ticker.
- [ ] ReAct loop processes observations and terminates when final signal is reached.
- [ ] Step limits prevent infinite execution loops.
