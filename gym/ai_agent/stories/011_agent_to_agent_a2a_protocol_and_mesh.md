# Story 011: Agent-to-Agent (A2A) Financial Protocol & Signals Mesh

## User Story
**As a** quantitative research developer,  
**I want to** implement the Agent-to-Agent (A2A) protocol with standardized Agent Cards and task endpoints over HTTP,  
**So that** distributed financial agents (e.g. Remote News Agent in Cloud A, Execution Agent on premises) can discover each other and collaborate over the network.

---

## 📖 Book Alignment
* **Book:** *Build an AI Agent (From Scratch)* ([Study Notes](../bin/build_an_ai_agent_notes.md#chapter-9-orchestrating-multi-agent-systems))
  - Chapter 9: *Orchestrating multi-agent systems* (9.6 A2A: Collaborating across networks, Agent Card, Server, Client)
* **Book:** *Effective Python (3rd Edition)* ([Study Notes](../bin/effective_python_v3_notes.md#chapter-14-collaboration))
  - **Item 81 & 82**: Manage Asynchronous Network I/O with Proper Timeouts
  - **Item 118**: Write Docstrings for Every Function, Class, and Module
  - **Item 119**: Use Packages to Organize Modules and Expose Stable APIs
  - **Item 121**: Define Distinct Root Exceptions (`A2AConnectionError`, `RemoteAgentTimeout`)
  - **Item 124**: Enforce Strict Typing via Pydantic Schemas

---

## 🎯 What You Will Learn
1. Defining standardized financial `AgentCard` metadata for remote signal providers.
2. Building an A2A Server exposing `/.well-known/agent.json` and ticker task endpoints.
3. Implementing an async `RemoteTickerAgentClient` connecting remote market models to local workflows.
4. Handling network timeouts and disconnects gracefully with typed exceptions.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Financial Agent Card Specification
In `src/agent/a2a/models.py`:
```python
from pydantic import BaseModel, Field
from typing import Any

class MarketSkillDeclaration(BaseModel):
    name: str
    description: str
    supported_asset_classes: list[str] = Field(default_factory=lambda: ["EQUITY"])

class FinancialAgentCard(BaseModel):
    agent_id: str
    name: str
    description: str
    endpoint_url: str
    skills: list[MarketSkillDeclaration] = Field(default_factory=list)

class TickerTaskRequest(BaseModel):
    task_id: str
    ticker: str
    lookback_days: int = 7

class TickerTaskResponse(BaseModel):
    task_id: str
    ticker: str
    sentiment_signal: str
    confidence: float
```

### 2. Implement Financial A2A Server
In `src/agent/a2a/server.py`:
```python
from fastapi import FastAPI
from agent.a2a.models import FinancialAgentCard, TickerTaskRequest, TickerTaskResponse
from agent.core.agent import FinancialReActAgent

def create_financial_a2a_server(card: FinancialAgentCard, agent: FinancialReActAgent) -> FastAPI:
    app = FastAPI(title=card.name)

    @app.get("/.well-known/agent.json", response_model=FinancialAgentCard)
    async def get_card():
        return card

    @app.post("/tasks/analyze_ticker", response_model=TickerTaskResponse)
    async def analyze(req: TickerTaskRequest):
        summary = await agent.analyze_ticker(req.ticker)
        return TickerTaskResponse(
            task_id=req.task_id,
            ticker=req.ticker,
            sentiment_signal="BULLISH" if "BULLISH" in summary else "NEUTRAL",
            confidence=0.88,
        )

    return app
```

---

## ✅ Acceptance Criteria
- [ ] `FinancialAgentCard` conforms to standard specification and is discoverable over HTTP.
- [ ] A2A Server dispatches ticker analysis tasks and returns structured signals.
- [ ] Remote client connects to distributed signal agents with timeout management.
- [ ] Network errors map cleanly to domain exceptions.
