# Story 010: Multi-Agent Collaboration: News, Quant & Risk Agents

## User Story
**As a** quantitative research developer,  
**I want to** orchestrate a multi-agent team (News Sentiment Agent, Quantitative Technical Agent, and Risk Manager) using concurrent workflows and agent handoffs,  
**So that** multiple specialized agents analyze a ticker in parallel and synthesize an institutional-grade investment signal.

---

## 📖 Book Alignment
* **Book:** *Build an AI Agent (From Scratch)* ([Study Notes](../bin/build_an_ai_agent_notes.md#chapter-9-orchestrating-multi-agent-systems))
  - Chapter 9: *Orchestrating multi-agent systems* (9.1 Why multi-agent?, 9.2 Three collaboration patterns, 9.3 Workflows, 9.4 Agent as Tool, 9.5 Agent Transfer)
* **Book:** *Effective Python (3rd Edition)* ([Study Notes](../bin/effective_python_v3_notes.md#chapter-9-concurrency-and-parallelism))
  - **Item 18**: Use `zip` to Process Iterators in Parallel
  - **Item 50**: Use Composition over Inheritance (`AgentTool` wraps `Agent`)
  - **Item 77–82**: Use Coroutines to Run Concurrent I/O; Use `asyncio.TaskGroup`
  - **Item 83**: Handle Concurrent Errors with `ExceptionGroup` and `except*`
  - **Item 103**: Prefer `collections.deque` / `asyncio.Queue` for Producer-Consumer Queues

---

## 🎯 What You Will Learn
1. Structuring specialized financial agents: News Sentiment Specialist, Technical Analyst, Risk Overseer.
2. Concurrent agent fan-out using modern `asyncio.TaskGroup` and `ExceptionGroup`.
3. Implementing the "Agent as Tool" pattern with strict context isolation.
4. Implementing the "Agent Transfer" pattern to pass a ticker evaluation from research to trade risk review.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Concurrent Multi-Agent Financial Research
In `src/agent/multi/financial_team.py`:
```python
import asyncio
from agent.core.agent import FinancialReActAgent

async def run_parallel_ticker_analysis(
    news_agent: FinancialReActAgent,
    quant_agent: FinancialReActAgent,
    ticker: str,
) -> dict[str, str]:
    """Runs news sentiment and quantitative technical analysis concurrently (Ch 9.3 & Item 77-83)."""
    results = {}

    async def _run_news():
        results["news_sentiment"] = await news_agent.analyze_ticker(ticker)

    async def _run_quant():
        results["quant_indicators"] = await quant_agent.analyze_ticker(ticker)

    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(_run_news())
            tg.create_task(_run_quant())
    except* Exception as eg:
        print(f"One or more financial analysis agents failed: {eg.exceptions}")
        raise

    return results
```

### 2. Risk Manager Agent-as-Tool
In `src/agent/multi/risk_agent_tool.py`:
```python
from agent.tools.base import tool, ToolSpec
from agent.core.agent import FinancialReActAgent

def make_risk_reviewer_tool(risk_agent: FinancialReActAgent) -> ToolSpec:
    """Wraps the Risk Manager Agent as a callable tool with context isolation (Ch 9.4 & Item 50)."""
    @tool(name="consult_risk_manager", description="Request portfolio risk and drawdown review for a proposed ticker signal.")
    def review_risk(ticker: str, signal: str, proposed_position_size: float) -> str:
        import asyncio
        loop = asyncio.get_event_loop()
        prompt = f"Evaluate risk for {ticker}: Signal={signal}, PositionSize={proposed_position_size}%"
        # Isolated context: only the risk approval / sizing recommendation returns
        return loop.run_until_complete(risk_agent.analyze_ticker(prompt))
    return review_risk
```

---

## ✅ Acceptance Criteria
- [ ] News Sentiment and Quant agents run concurrently via `asyncio.TaskGroup`.
- [ ] Concurrent errors are caught with `ExceptionGroup` and `except*`.
- [ ] `AgentTool` isolates sub-agent scratchpad tokens while returning final risk advice.
- [ ] Multi-agent workflow produces a synthesized investment recommendation for target ticker.
