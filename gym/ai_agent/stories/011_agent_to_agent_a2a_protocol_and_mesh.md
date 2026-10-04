# Story 011: Agent-to-Agent (A2A) Protocol & Distributed Network Agent Mesh

## User Story
**As an** AI Agent developer,  
**I want to** implement the Agent-to-Agent (A2A) protocol with standardized Agent Cards and HTTP/SSE endpoints,  
**So that** agents distributed across different machines, processes, and network boundaries can advertise capabilities and collaborate remotely.

---

## 📖 Book Alignment
* **Book:** *Build an AI Agent (From Scratch)* ([Study Notes](file:///home/tofunth/stuffs/mono/gym/ai_agent/bin/build_an_ai_agent_notes.md#chapter-9-orchestrating-multi-agent-systems))
  - Chapter 9: *Orchestrating multi-agent systems* (9.6 A2A: Collaborating across networks, Agent Card, Server, Client)
* **Book:** *Effective Python (3rd Edition)* ([Study Notes](file:///home/tofunth/stuffs/mono/gym/ai_agent/bin/effective_python_v3_notes.md#chapter-14-collaboration))
  - **Item 81 & 82**: Manage Asynchronous Network I/O with Proper Timeouts and Graceful Task Cancellation
  - **Item 118**: Write Docstrings for Every Function, Class, and Module
  - **Item 119**: Use Packages to Organize Modules and Expose Stable APIs
  - **Item 121**: Define Distinct Root Exceptions (`A2AConnectionError`, `RemoteAgentTimeout`)
  - **Item 124**: Enforce Strict Typing via Pydantic Schemas

---

## 🎯 What You Will Learn
1. Defining standardized `AgentCard` metadata models for network capability discovery.
2. Building an A2A Server exposing `/.well-known/agent.json` and task dispatch endpoints.
3. Implementing an async `RemoteAgentClient` connecting remote agents to local agent registries.
4. Handling network failures, timeouts, and disconnects gracefully with typed exceptions.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Define Agent Card Specification
In `src/agent/a2a/models.py`:
```python
from pydantic import BaseModel, Field
from typing import Any

class SkillDeclaration(BaseModel):
    name: str
    description: str
    input_schema: dict[str, Any]

class AgentCard(BaseModel):
    """Standard descriptor for network-discoverable agents (Ch 9.6 & Item 124)."""
    agent_id: str
    name: str
    description: str
    version: str = "1.0.0"
    endpoint_url: str
    skills: list[SkillDeclaration] = Field(default_factory=list)

class TaskRequest(BaseModel):
    task_id: str
    instruction: str
    context: dict[str, Any] = Field(default_factory=dict)

class TaskResponse(BaseModel):
    task_id: str
    status: str
    result: str
```

### 2. Implement A2A Server
In `src/agent/a2a/server.py`:
```python
from fastapi import FastAPI
from agent.a2a.models import AgentCard, TaskRequest, TaskResponse
from agent.core.agent import Agent

def create_a2a_app(agent_card: AgentCard, local_agent: Agent) -> FastAPI:
    """Creates an ASGI application exposing the agent to the network mesh (Ch 9.6)."""
    app = FastAPI(title=agent_card.name, description=agent_card.description)

    @app.get("/.well-known/agent.json", response_model=AgentCard)
    async def get_agent_card() -> AgentCard:
        return agent_card

    @app.post("/tasks", response_model=TaskResponse)
    async def dispatch_task(req: TaskRequest) -> TaskResponse:
        answer = await local_agent.run(req.instruction)
        return TaskResponse(
            task_id=req.task_id,
            status="completed",
            result=answer,
        )

    return app
```

### 3. Implement Remote Agent Client
In `src/agent/a2a/client.py`:
```python
import httpx
from agent.core.exceptions import AgentBaseException
from agent.a2a.models import AgentCard, TaskRequest, TaskResponse

class A2AConnectionError(AgentBaseException):
    """Raised when communication with a remote agent fails (Item 121)."""
    pass

class RemoteAgentClient:
    """Client adapter for calling remote agents over HTTP (Ch 9.6)."""

    def __init__(self, base_url: str, *, timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def fetch_card(self) -> AgentCard:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.get(f"{self.base_url}/.well-known/agent.json")
            if resp.status_code != 200:
                raise A2AConnectionError(f"Failed to fetch Agent Card from {self.base_url}")
            return AgentCard(**resp.json())

    async def execute_task(self, instruction: str) -> str:
        req = TaskRequest(task_id="remote-1", instruction=instruction)
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(f"{self.base_url}/tasks", json=req.model_dump())
            if resp.status_code != 200:
                raise A2AConnectionError(f"Remote task execution failed: {resp.text}")
            res = TaskResponse(**resp.json())
            return res.result
```

---

## ✅ Acceptance Criteria
- [ ] `AgentCard` conforms to standard JSON specification.
- [ ] A2A server serves `/.well-known/agent.json` and `/tasks` cleanly.
- [ ] `RemoteAgentClient` communicates with remote agents over HTTP with timeouts.
- [ ] Network errors cleanly mapped to `A2AConnectionError`.
