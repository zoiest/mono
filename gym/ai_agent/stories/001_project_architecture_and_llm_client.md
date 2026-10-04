# Story 001: Project Setup, Architecture & Provider-Agnostic LLM Client

## User Story
**As an** AI Agent developer,  
**I want to** establish a clean Python project package structure and implement an abstract, provider-agnostic LLM client (supporting OpenAI, Anthropic, Gemini via LiteLLM) with streaming and structured output,  
**So that** the agent codebase has clean separation of concerns, strict type safety, predictable error handling, and vendor portability.

---

## 📖 Book Alignment
* **Book:** *Build an AI Agent (From Scratch)* ([Study Notes](../bin/build_an_ai_agent_notes.md#chapter-1-what-is-an-ai-agent))
  - Chapter 1: *What is an AI agent?* (1.2 Understanding LLM agents, 1.3 Workflow vs. agent)
  - Chapter 2: *The brain of AI agents: LLMs* (2.2 LLM API basics, unifying providers with LiteLLM)
* **Book:** *Effective Python (3rd Edition)* ([Study Notes](../bin/effective_python_v3_notes.md#chapter-1-pythonic-thinking))
  - **Item 1 & 2**: Know Which Version of Python You’re Using (Python 3.12+) & Follow PEP 8
  - **Item 31**: Return Dedicated Result Objects Instead of Requiring Function Callers to Unpack
  - **Item 36 & 37**: Use None for Dynamic Defaults; Enforce Clarity with Keyword-Only Arguments
  - **Item 117 & 119**: Use Virtual Environments & Use Packages to Organize Modules
  - **Item 121**: Define a Root Exception to Insulate Callers from APIs
  - **Item 124**: Consider Static Analysis via typing to Obviate Bugs

---

## 🎯 What You Will Learn
1. Organizing an AI agent codebase with modern Python packaging conventions (`pyproject.toml`, `src/agent/`).
2. Defining a root exception hierarchy (`AgentBaseException`) to isolate client code from low-level API failures.
3. Returning typed dataclass result objects (`ModelResponse`, `TokenUsage`) instead of loose dictionaries.
4. Implementing a provider-agnostic LLM client using `typing.Protocol` and `LiteLLM`.
5. Testing LLM clients using mocks (`unittest.mock`) to prevent external API calls during CI.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Define Root Exception Hierarchy
In `src/agent/core/exceptions.py`:
```python
class AgentBaseException(Exception):
    """Root exception for all agent domain errors (Effective Python Item 121)."""
    pass

class LlmProviderError(AgentBaseException):
    """Raised when an LLM provider API call fails."""
    def __init__(self, message: str, *, provider: str, status_code: int | None = None):
        super().__init__(f"[{provider}] {message}")
        self.provider = provider
        self.status_code = status_code

class ModelTimeoutError(LlmProviderError):
    """Raised when a completion request exceeds its configured timeout."""
    pass
```

### 2. Define Typed Result Models
In `src/agent/core/models.py`:
```python
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class TokenUsage:
    """Metrics capturing token expenditure (Effective Python Item 31, 56)."""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

@dataclass
class ToolCallRequest:
    """Represents a tool call requested by the model."""
    id: str
    name: str
    arguments: dict[str, Any]

@dataclass
class ModelResponse:
    """Structured result object from the LLM client (Effective Python Item 31)."""
    content: str | None = None
    tool_calls: list[ToolCallRequest] = field(default_factory=list)
    usage: TokenUsage = field(default_factory=TokenUsage)
    finish_reason: str = "stop"
    raw_response: dict[str, Any] | None = None
```

### 3. Implement Provider-Agnostic `LlmClient` Interface
In `src/agent/llm/client.py`:
```python
from typing import Protocol, Any, runtime_checkable
import litellm
from agent.core.exceptions import LlmProviderError, ModelTimeoutError
from agent.core.models import ModelResponse, ToolCallRequest, TokenUsage

@runtime_checkable
class LlmClient(Protocol):
    """Protocol defining provider-agnostic completion behavior (Item 124)."""
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
    """Concrete LLM client adapter wrapping LiteLLM (Ch 2.2)."""

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
        except litellm.Timeout as e:
            raise ModelTimeoutError(str(e), provider=target_model) from e
        except Exception as e:
            raise LlmProviderError(str(e), provider=target_model) from e

        choice = res.choices[0]
        message = choice.message

        tool_calls = []
        if hasattr(message, "tool_calls") and message.tool_calls:
            for tc in message.tool_calls:
                import json
                tool_calls.append(
                    ToolCallRequest(
                        id=tc.id,
                        name=tc.function.name,
                        arguments=json.loads(tc.function.arguments),
                    )
                )

        usage = TokenUsage(
            prompt_tokens=res.usage.prompt_tokens,
            completion_tokens=res.usage.completion_tokens,
            total_tokens=res.usage.total_tokens,
        )

        return ModelResponse(
            content=message.content,
            tool_calls=tool_calls,
            usage=usage,
            finish_reason=choice.finish_reason,
            raw_response=res.model_dump(),
        )
```

### 4. Verify with Mocks
In `tests/test_llm_client.py`:
```python
import pytest
from unittest.mock import patch, AsyncMock
from agent.llm.client import LiteLlmClient

@pytest.mark.asyncio
async def test_lite_llm_client_complete():
    client = LiteLlmClient(default_model="gpt-4o")
    with patch("litellm.acompletion", new_callable=AsyncMock) as mock_complete:
        mock_complete.return_value.choices = [
            AsyncMock(
                message=AsyncMock(content="Hello world", tool_calls=None),
                finish_reason="stop",
            )
        ]
        mock_complete.return_value.usage = AsyncMock(
            prompt_tokens=10, completion_tokens=5, total_tokens=15
        )
        mock_complete.return_value.model_dump.return_value = {}

        response = await client.complete([{"role": "user", "content": "Hi"}])
        assert response.content == "Hello world"
        assert response.usage.total_tokens == 15
```

---

## ✅ Acceptance Criteria
- [ ] Root exception hierarchy defined in `src/agent/core/exceptions.py`.
- [ ] Strongly typed dataclasses created in `src/agent/core/models.py`.
- [ ] `LlmClient` protocol and `LiteLlmClient` adapter pass strict `mypy` checks.
- [ ] Unit tests with mocks verify error propagation and response mapping without live API calls.
