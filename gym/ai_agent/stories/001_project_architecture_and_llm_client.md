# Story 001: Project Setup & Financial LLM Client Adapter

## User Story
**As a** quantitative research developer,  
**I want to** establish a clean Python project structure and build a provider-agnostic LLM client with structured signal schemas,  
**So that** our financial agent can reliably analyze market headlines, extract sentiment signals, and support multiple model providers (OpenAI, Anthropic, Gemini) with strict type safety.

---

## 📖 Book Alignment
* **Book:** *Build an AI Agent (From Scratch)* ([Study Notes](../bin/build_an_ai_agent_notes.md#chapter-1-what-is-an-ai-agent))
  - Chapter 1: *What is an AI agent?* (1.2 Understanding LLM agents, 1.3 Workflow vs. agent)
  - Chapter 2: *The brain of AI agents: LLMs* (2.2 LLM API basics, unifying providers with LiteLLM, structured outputs)
* **Book:** *Effective Python (3rd Edition)* ([Study Notes](../bin/effective_python_v3_notes.md#chapter-1-pythonic-thinking))
  - **Item 1 & 2**: Know Which Version of Python You’re Using (Python 3.12+) & Follow PEP 8
  - **Item 31**: Return Dedicated Result Objects Instead of Requiring Callers to Unpack More Than Three Variables
  - **Item 36 & 37**: Use None for Dynamic Defaults; Enforce Clarity with Keyword-Only Arguments
  - **Item 117 & 119**: Use Virtual Environments & Use Packages to Organize Modules
  - **Item 121**: Define a Root Exception to Insulate Callers from APIs
  - **Item 124**: Consider Static Analysis via typing to Obviate Bugs

---

## 🎯 What You Will Learn
1. Organizing a financial AI agent repository with modern packaging (`pyproject.toml`, `src/agent/`).
2. Defining domain-specific exception hierarchies (`FinancialAgentException`, `TickerNotFoundError`).
3. Returning typed dataclasses for market sentiment signals (`SentimentSignal`, `ModelResponse`).
4. Writing a provider-agnostic LLM adapter with `LiteLLM` and `typing.Protocol`.
5. Unit testing LLM completion logic using mocks to ensure test speed and zero API costs.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Define Financial Domain Exceptions
In `src/agent/core/exceptions.py`:
```python
class FinancialAgentException(Exception):
    """Root exception for all financial agent errors (Effective Python Item 121)."""
    pass

class LlmProviderError(FinancialAgentException):
    """Raised when LLM provider API call fails."""
    def __init__(self, message: str, *, provider: str):
        super().__init__(f"[{provider}] {message}")
        self.provider = provider

class InvalidTickerError(FinancialAgentException):
    """Raised when an invalid or unquoted ticker symbol is supplied."""
    pass
```

### 2. Define Typed Financial Signal Data Models
In `src/agent/core/models.py`:
```python
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

class SignalDirection(str, Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"

@dataclass(frozen=True)
class SentimentSignal:
    """Structured trading signal extracted from news/filings (Item 31, 56)."""
    ticker: str
    direction: SignalDirection
    confidence: float  # 0.0 to 1.0
    summary: str
    catalysts: list[str] = field(default_factory=list)

@dataclass
class ToolCallRequest:
    id: str
    name: str
    arguments: dict[str, Any]

@dataclass
class ModelResponse:
    content: str | None = None
    tool_calls: list[ToolCallRequest] = field(default_factory=list)
    signal: SentimentSignal | None = None
    total_tokens: int = 0
    finish_reason: str = "stop"
```

### 3. Implement Provider-Agnostic Financial LLM Client
In `src/agent/llm/client.py`:
```python
from typing import Protocol, Any, runtime_checkable
import litellm
from agent.core.exceptions import LlmProviderError
from agent.core.models import ModelResponse, ToolCallRequest

@runtime_checkable
class LlmClient(Protocol):
    async def complete(
        self,
        messages: list[dict[str, Any]],
        *,
        model: str,
        temperature: float = 0.0,
        tools: list[dict[str, Any]] | None = None,
        timeout: float = 30.0,
    ) -> ModelResponse:
        ...

class LiteLlmClient:
    """Adapter wrapping LiteLLM for financial intelligence extraction (Ch 2.2)."""

    def __init__(self, *, default_model: str = "gpt-4o"):
        self.default_model = default_model

    async def complete(
        self,
        messages: list[dict[str, Any]],
        *,
        model: str | None = None,
        temperature: float = 0.0,
        tools: list[dict[str, Any]] | None = None,
        timeout: float = 30.0,
    ) -> ModelResponse:
        target_model = model or self.default_model
        params: dict[str, Any] = {
            "model": target_model,
            "messages": messages,
            "temperature": temperature,
            "timeout": timeout,
        }
        if tools:
            params["tools"] = tools

        try:
            res = await litellm.acompletion(**params)
        except Exception as e:
            raise LlmProviderError(str(e), provider=target_model) from e

        msg = res.choices[0].message
        tool_calls = []
        if getattr(msg, "tool_calls", None):
            import json
            for tc in msg.tool_calls:
                tool_calls.append(
                    ToolCallRequest(
                        id=tc.id,
                        name=tc.function.name,
                        arguments=json.loads(tc.function.arguments),
                    )
                )

        return ModelResponse(
            content=msg.content,
            tool_calls=tool_calls,
            total_tokens=res.usage.total_tokens,
            finish_reason=res.choices[0].finish_reason,
        )
```

### 4. Verify Client with Unit Tests
In `tests/test_financial_client.py`:
```python
import pytest
from unittest.mock import patch, AsyncMock
from agent.llm.client import LiteLlmClient

@pytest.mark.asyncio
async def test_financial_client_completion():
    client = LiteLlmClient(default_model="gpt-4o")
    with patch("litellm.acompletion", new_callable=AsyncMock) as mock_complete:
        mock_complete.return_value.choices = [
            AsyncMock(
                message=AsyncMock(content="AAPL reports record Q4 earnings.", tool_calls=None),
                finish_reason="stop",
            )
        ]
        mock_complete.return_value.usage.total_tokens = 45

        resp = await client.complete([{"role": "user", "content": "Analyze AAPL"}])
        assert "AAPL" in resp.content
        assert resp.total_tokens == 45
```

---

## ✅ Acceptance Criteria
- [ ] Root exception hierarchy defined in `src/agent/core/exceptions.py`.
- [ ] Strongly typed `SentimentSignal` and `ModelResponse` dataclasses created.
- [ ] `LlmClient` protocol and `LiteLlmClient` adapter pass strict `mypy` typing checks.
- [ ] Unit tests verify mock completion and error propagation.
