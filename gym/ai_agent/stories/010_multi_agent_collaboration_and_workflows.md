# Story 010: Multi-Agent Collaboration: Workflows, Agent-as-Tool & Handoffs

## User Story
**As an** AI Agent developer,  
**I want to** build multi-agent orchestration architectures supporting Workflows (Sequential/Parallel/Loop), Agent-as-Tool, and Agent Transfer (Handoff trees),  
**So that** specialized agents (e.g. Researcher, Coder, Reviewer) can collaborate on complex projects with isolated contexts and clear separation of responsibility.

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
1. Orchestrating deterministic agent workflows: Sequential, Parallel fan-out, and Iterative feedback.
2. Concurrent agent execution with modern `asyncio.TaskGroup` and `ExceptionGroup`.
3. Implementing the "Agent as Tool" pattern with strict context isolation.
4. Implementing the "Agent Transfer" pattern with hierarchical handoff trees.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Parallel Agent Workflow with `asyncio.TaskGroup`
In `src/agent/multi/workflows.py`:
```python
import asyncio
from typing import Any
from agent.core.agent import Agent

async def run_parallel_agents(agents: list[Agent], prompt: str) -> list[str]:
    """Executes multiple specialized agents concurrently using modern TaskGroup (Ch 9.3 & Item 77-83)."""
    results: list[str] = [""] * len(agents)

    async def _worker(idx: int, agent: Agent):
        results[idx] = await agent.run(prompt)

    try:
        async with asyncio.TaskGroup() as tg:
            for i, ag in enumerate(agents):
                tg.create_task(_worker(i, ag))
    except* Exception as eg:  # Python 3.11+ ExceptionGroup handling (Item 83)
        print(f"One or more agents failed in parallel run: {eg.exceptions}")
        raise

    return results
```

### 2. Implement the "Agent as Tool" Pattern
In `src/agent/multi/agent_tool.py`:
```python
from agent.core.agent import Agent
from agent.tools.base import tool, ToolSpec

def make_agent_as_tool(sub_agent: Agent, *, name: str, description: str) -> ToolSpec:
    """Wraps an Agent as a callable tool with strict context isolation (Ch 9.4 & Item 50)."""
    @tool(name=name, description=description)
    def call_sub_agent(sub_task_prompt: str) -> str:
        # Note: In an async runtime, we await sub_agent.run()
        import asyncio
        loop = asyncio.get_event_loop()
        # Isolates scratchpad tokens; only returns distilled final answer
        return loop.run_until_complete(sub_agent.run(sub_task_prompt))

    return call_sub_agent
```

### 3. Implement Agent Transfer (Handoff) Pattern
In `src/agent/multi/transfer.py`:
```python
from agent.tools.base import tool

class AgentTransferRouter:
    """Transfers execution control between specialized agents in a tree (Ch 9.5)."""

    def __init__(self, agent_directory: dict[str, str]):
        self.directory = agent_directory

    def make_transfer_tool(self):
        @tool(name="transfer_to_agent", description="Handoff the task to a specialized agent.")
        def transfer_to_agent(target_agent: str, context_summary: str) -> str:
            if target_agent not in self.directory:
                return f"Error: Agent '{target_agent}' does not exist in registry."
            return f"HANDOFF_SIGNAL:{target_agent}:{context_summary}"
        return transfer_to_agent
```

---

## ✅ Acceptance Criteria
- [ ] Parallel workflow executes agents concurrently using `asyncio.TaskGroup`.
- [ ] Concurrent errors are caught with `ExceptionGroup` and `except*`.
- [ ] `AgentTool` isolates child agent thought scratchpads from parent context.
- [ ] Agent Transfer routes tasks dynamically between specialized agents.
