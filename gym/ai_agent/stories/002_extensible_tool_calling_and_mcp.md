# Story 002: Extensible Tool Calling Engine & MCP Protocol Integration

## User Story
**As an** AI Agent developer,  
**I want to** build a declarative tool definition framework with automated JSON schema extraction, runtime validation, and support for Model Context Protocol (MCP),  
**So that** the LLM can safely discover, validate, and execute local tools (calculator, web search) as well as remote MCP server capabilities.

---

## 📖 Book Alignment
* **Book:** *Build an AI Agent (From Scratch)* ([Study Notes](../bin/build_an_ai_agent_notes.md#chapter-3-enabling-actions-tool-use))
  - Chapter 3: *Enabling actions: Tool use* (3.1 Types of LLM tools, 3.2 How tool calling works, Model Context Protocol)
* **Book:** *Effective Python (3rd Edition)* ([Study Notes](../bin/effective_python_v3_notes.md#chapter-5-functions))
  - **Item 26 & 27**: Prefer `get` over `in`/`KeyError`; Prefer `defaultdict` over `setdefault`
  - **Item 29**: Compose Classes Instead of Deeply Nesting Dictionaries (`ToolSpec`, `ToolResult`)
  - **Item 32**: Prefer Raising Exceptions to Returning None (`ToolExecutionError`)
  - **Item 38**: Define Function Decorators with `functools.wraps`
  - **Item 50**: Use Composition over Inheritance for Tool Adapters
  - **Item 91**: Avoid `eval` and `exec` Unless You're Building a Sandbox

---

## 🎯 What You Will Learn
1. Using `@functools.wraps` to build a clean `@tool` decorator that inspects signatures and type hints.
2. Converting Python functions automatically into OpenAPI-compatible JSON Schemas for LLM function calling.
3. Building an AST-safe mathematical expression evaluator without security risks of `eval()`.
4. Implementing an in-memory `ToolRegistry` with validation, type coercion, and domain exceptions.
5. Connecting remote Model Context Protocol (MCP) servers to local agent tool registries.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Build the `@tool` Decorator
In `src/agent/tools/base.py`:
```python
import functools
import inspect
from dataclasses import dataclass
from typing import Callable, Any, get_type_hints
from agent.core.exceptions import AgentBaseException

class ToolExecutionError(AgentBaseException):
    """Raised when tool execution fails (Item 32)."""
    pass

@dataclass
class ToolSpec:
    """Declarative representation of an agent tool (Item 29)."""
    name: str
    description: str
    parameters: dict[str, Any]
    func: Callable[..., Any]

def tool(name: str | None = None, description: str | None = None):
    """Decorator that wraps a Python function into an LLM-callable ToolSpec (Item 38)."""
    def decorator(fn: Callable[..., Any]) -> ToolSpec:
        tool_name = name or fn.__name__
        tool_desc = description or (inspect.getdoc(fn) or "No description provided.")
        
        # Build JSON Schema properties from function annotations
        type_hints = get_type_hints(fn)
        sig = inspect.signature(fn)
        
        properties: dict[str, Any] = {}
        required: list[str] = []

        type_map = {
            str: "string",
            int: "integer",
            float: "number",
            bool: "boolean",
            list: "array",
            dict: "object",
        }

        for param_name, param in sig.parameters.items():
            if param_name == "return":
                continue
            param_type = type_hints.get(param_name, str)
            json_type = type_map.get(param_type, "string")
            properties[param_name] = {"type": json_type}
            if param.default is inspect.Parameter.empty:
                required.append(param_name)

        parameters_schema = {
            "type": "object",
            "properties": properties,
            "required": required,
        }

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)

        return ToolSpec(
            name=tool_name,
            description=tool_desc.strip(),
            parameters=parameters_schema,
            func=wrapper,
        )
    return decorator
```

### 2. Implement Built-in Safe Tools (Calculator & Search)
In `src/agent/tools/builtins.py`:
```python
import ast
import operator
from agent.tools.base import tool, ToolExecutionError

# Safe AST-based calculator: avoids dangerous eval() (Item 91)
_SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}

def _eval_expr(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    elif isinstance(node, ast.BinOp) and type(node.op) in _SAFE_OPERATORS:
        return _SAFE_OPERATORS[type(node.op)](_eval_expr(node.left), _eval_expr(node.right))
    elif isinstance(node, ast.UnaryOp) and type(node.op) in _SAFE_OPERATORS:
        return _SAFE_OPERATORS[type(node.op)](_eval_expr(node.operand))
    raise ToolExecutionError(f"Unsupported math expression or syntax: {ast.dump(node)}")

@tool(name="calculator", description="Safely calculate mathematical expressions without code evaluation.")
def calculator(expression: str) -> str:
    """Calculates math expressions, e.g. '3 * (4 + 2)'."""
    try:
        parsed = ast.parse(expression, mode='eval').body
        result = _eval_expr(parsed)
        return str(result)
    except Exception as e:
        raise ToolExecutionError(f"Math calculation failed for '{expression}': {e}") from e

@tool(name="web_search", description="Search the web for real-time information.")
def web_search(query: str, max_results: int = 3) -> str:
    """Mock web search tool simulating search engine results."""
    return f"Search results for '{query}': [1] Summary facts for query."
```

### 3. Implement the `ToolRegistry`
In `src/agent/tools/registry.py`:
```python
from collections import defaultdict
from typing import Any
from agent.tools.base import ToolSpec, ToolExecutionError

class ToolRegistry:
    """Central registry for discovering and executing agent tools (Ch 3.2)."""

    def __init__(self):
        self._tools: dict[str, ToolSpec] = {}

    def register(self, tool_spec: ToolSpec) -> None:
        self._tools[tool_spec.name] = tool_spec

    def get_schemas(self) -> list[dict[str, Any]]:
        """Export tools into OpenAI / LiteLLM function calling format."""
        return [
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.parameters,
                },
            }
            for t in self._tools.values()
        ]

    def execute(self, name: str, arguments: dict[str, Any]) -> str:
        tool_spec = self._tools.get(name)
        if not tool_spec:
            raise ToolExecutionError(f"Tool '{name}' is not registered.")
        try:
            res = tool_spec.func(**arguments)
            return str(res)
        except TypeError as e:
            raise ToolExecutionError(f"Invalid arguments for tool '{name}': {e}") from e
        except Exception as e:
            raise ToolExecutionError(f"Tool '{name}' failed during execution: {e}") from e
```

---

## ✅ Acceptance Criteria
- [ ] `@tool` decorator preserves function metadata using `@functools.wraps`.
- [ ] Automatic JSON Schema matches parameters and type annotations.
- [ ] Calculator evaluates math safely without `eval()`.
- [ ] `ToolRegistry.execute()` cleanly validates arguments and wraps runtime failures in `ToolExecutionError`.
