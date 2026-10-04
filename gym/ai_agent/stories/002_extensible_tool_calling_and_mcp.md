# Story 002: Financial Tool Engine & News Fetcher (Finviz / Yahoo)

## User Story
**As a** quantitative research developer,  
**I want to** build a declarative tool calling engine and implement live financial news and market quote fetching tools,  
**So that** the LLM can query real-time market data, company news feeds, and calculate financial valuation metrics without hallucinations.

---

## 📖 Book Alignment
* **Book:** *Build an AI Agent (From Scratch)* ([Study Notes](../bin/build_an_ai_agent_notes.md#chapter-3-enabling-actions-tool-use))
  - Chapter 3: *Enabling actions: Tool use* (3.1 Types of LLM tools, 3.2 Function calling mechanics, Model Context Protocol)
* **Book:** *Effective Python (3rd Edition)* ([Study Notes](../bin/effective_python_v3_notes.md#chapter-5-functions))
  - **Item 26 & 27**: Prefer `get` over `in`/`KeyError`; Prefer `defaultdict` over `setdefault`
  - **Item 29**: Compose Classes Instead of Deeply Nesting Dictionaries (`ToolSpec`, `ToolResult`)
  - **Item 32**: Prefer Raising Exceptions to Returning None (`ToolExecutionError`)
  - **Item 38**: Define Function Decorators with `functools.wraps`
  - **Item 91**: Avoid `eval` and `exec` for Financial Math Calculations
  - **Item 111 & 112**: Encapsulate External API Dependencies for Unit Test Mocking

---

## 🎯 What You Will Learn
1. Building a `@tool` decorator that transforms Python functions into OpenAI-compatible JSON Schemas.
2. Implementing an AST-safe financial ratio calculator (P/E, Debt-to-Equity, YoY growth) without `eval()`.
3. Creating a financial news fetcher tool that parses recent headlines for target tickers.
4. Implementing a `ToolRegistry` with parameter validation and domain exception handling.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Build the `@tool` Decorator
In `src/agent/tools/base.py`:
```python
import functools
import inspect
from dataclasses import dataclass
from typing import Callable, Any, get_type_hints
from agent.core.exceptions import FinancialAgentException

class ToolExecutionError(FinancialAgentException):
    pass

@dataclass
class ToolSpec:
    name: str
    description: str
    parameters: dict[str, Any]
    func: Callable[..., Any]

def tool(name: str | None = None, description: str | None = None):
    def decorator(fn: Callable[..., Any]) -> ToolSpec:
        tool_name = name or fn.__name__
        tool_desc = description or (inspect.getdoc(fn) or "No description.")
        
        type_hints = get_type_hints(fn)
        sig = inspect.signature(fn)
        
        properties: dict[str, Any] = {}
        required: list[str] = []
        type_map = {str: "string", int: "integer", float: "number", bool: "boolean", list: "array"}

        for p_name, param in sig.parameters.items():
            if p_name == "return":
                continue
            properties[p_name] = {"type": type_map.get(type_hints.get(p_name, str), "string")}
            if param.default is inspect.Parameter.empty:
                required.append(p_name)

        @functools.wraps(fn)  # Preserves metadata (Item 38)
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)

        return ToolSpec(
            name=tool_name,
            description=tool_desc.strip(),
            parameters={"type": "object", "properties": properties, "required": required},
            func=wrapper,
        )
    return decorator
```

### 2. Implement Financial News & Metric Tools
In `src/agent/tools/finance.py`:
```python
import ast
import operator
from agent.tools.base import tool, ToolExecutionError

_MATH_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub,
    ast.Mult: operator.mul, ast.Div: operator.truediv,
}

def _eval_math(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    elif isinstance(node, ast.BinOp) and type(node.op) in _MATH_OPS:
        return _MATH_OPS[type(node.op)](_eval_math(node.left), _eval_math(node.right))
    raise ToolExecutionError("Unsupported mathematical operation.")

@tool(name="calculate_metric", description="Calculate financial ratios (e.g. PE = price / eps).")
def calculate_metric(formula: str) -> str:
    try:
        tree = ast.parse(formula, mode='eval').body
        return f"{_eval_math(tree):.4f}"
    except Exception as e:
        raise ToolExecutionError(f"Calculation failed for '{formula}': {e}") from e

@tool(name="fetch_ticker_news", description="Fetch the latest market news headlines and summaries for a ticker.")
def fetch_ticker_news(ticker: str, limit: int = 5) -> str:
    """Fetches news articles for a given stock symbol."""
    ticker = ticker.upper().strip()
    # Mock news database for testing / initial implementation
    mock_news = {
        "NVDA": [
            "NVIDIA announces next-gen Blackwell Ultra architecture with 30% higher AI throughput.",
            "Hyperscalers increase FY2025 AI CapEx forecast by $15B.",
            "Export restrictions on select semiconductor chips under review."
        ],
        "AAPL": [
            "Apple Intelligence rolling out to international English markets next month.",
            "iPhone 16 Pro channel checks indicate resilient demand in North America.",
        ]
    }
    articles = mock_news.get(ticker, [f"No breaking news found for ticker {ticker}."])
    formatted = [f"[{i+1}] {headline}" for i, headline in enumerate(articles[:limit])]
    return f"Latest news for {ticker}:
" + "
".join(formatted)
```

### 3. Implement `ToolRegistry`
In `src/agent/tools/registry.py`:
```python
from agent.tools.base import ToolSpec, ToolExecutionError

class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, ToolSpec] = {}

    def register(self, t: ToolSpec) -> None:
        self._tools[t.name] = t

    def get_schemas(self) -> list[dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.parameters,
                }
            }
            for t in self._tools.values()
        ]

    def execute(self, name: str, args: dict) -> str:
        if name not in self._tools:
            raise ToolExecutionError(f"Tool '{name}' not found.")
        return str(self._tools[name].func(**args))
```

---

## ✅ Acceptance Criteria
- [ ] `@tool` decorator automatically builds JSON Schema matching parameter annotations.
- [ ] AST math evaluator computes financial ratios without using `eval()`.
- [ ] `fetch_ticker_news` tool formats recent ticker headlines cleanly.
- [ ] `ToolRegistry` executes tools and wraps exceptions in `ToolExecutionError`.
