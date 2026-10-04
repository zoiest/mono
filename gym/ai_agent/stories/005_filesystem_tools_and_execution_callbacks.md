# Story 005: Filesystem Navigation Tools & Agent Execution Callbacks

## User Story
**As an** AI Agent developer,  
**I want to** provide the agent with safe filesystem exploration tools (directory listing, file reading, zip archive extraction) and an extensible callback system,  
**So that** the agent can inspect complex local directory structures to solve GAIA benchmark tasks while allowing humans to approve sensitive actions and compress outputs.

---

## 📖 Book Alignment
* **Book:** *Build an AI Agent (From Scratch)* ([Study Notes](../bin/build_an_ai_agent_notes.md#chapter-5-building-knowledge-bases-with-rag--filesystem-tools))
  - Chapter 5: *Building knowledge bases with RAG* (5.4 Structure-based search & filesystem tools, 5.5 Extending agents with callbacks)
* **Book:** *Effective Python (3rd Edition)* ([Study Notes](../bin/effective_python_v3_notes.md#chapter-5-functions))
  - **Item 33**: Know How Closures Interact with Variable Scope and `nonlocal`
  - **Item 39**: Prefer `functools.partial` over lambda Expressions for Glue Functions
  - **Item 86**: Consider `contextlib` and `with` Statements for Reusable Behavior
  - **Item 110**: Isolate Tests from Each Other with `setUp`, `tearDown`, and Fixtures

---

## 🎯 What You Will Learn
1. Building sandboxed filesystem tools with strict directory traversal validation (`os.path.realpath`).
2. Handling zip archive inspection and extraction for GAIA benchmark datasets.
3. Designing an agent event callback architecture (`on_step_start`, `on_tool_call`, `on_tool_result`).
4. Implementing a human-in-the-loop (HITL) approval callback to block dangerous tool calls.
5. Implementing observation compression callbacks to avoid context bloating.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Build Safe Filesystem Tools
In `src/agent/tools/filesystem.py`:
```python
import os
import zipfile
from agent.tools.base import tool, ToolExecutionError

class SafeWorkspace:
    """Guarantees all file operations stay bounded within root workspace."""
    def __init__(self, root_dir: str):
        self.root_dir = os.path.realpath(root_dir)

    def _resolve(self, relative_path: str) -> str:
        resolved = os.path.realpath(os.path.join(self.root_dir, relative_path))
        if not resolved.startswith(self.root_dir):
            raise ToolExecutionError(f"Access denied: path '{relative_path}' is outside workspace.")
        return resolved

def make_filesystem_tools(workspace: SafeWorkspace) -> list:
    @tool(name="list_directory", description="Lists files and subdirectories at path.")
    def list_dir(path: str = ".") -> str:
        real_path = workspace._resolve(path)
        try:
            entries = os.listdir(real_path)
            return "
".join(entries) if entries else "(empty directory)"
        except Exception as e:
            raise ToolExecutionError(f"Cannot list directory '{path}': {e}") from e

    @tool(name="read_file_head", description="Read the first N lines of a file.")
    def read_head(path: str, max_lines: int = 30) -> str:
        real_path = workspace._resolve(path)
        try:
            with open(real_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = [f.readline() for _ in range(max_lines)]
                return "".join(lines)
        except Exception as e:
            raise ToolExecutionError(f"Cannot read file '{path}': {e}") from e

    @tool(name="extract_zip", description="Extract a zip archive into a destination directory.")
    def extract_zip(zip_path: str, dest_dir: str = ".") -> str:
        real_zip = workspace._resolve(zip_path)
        real_dest = workspace._resolve(dest_dir)
        try:
            with zipfile.ZipFile(real_zip, "r") as z:
                z.extractall(real_dest)
            return f"Successfully extracted '{zip_path}' into '{dest_dir}'"
        except Exception as e:
            raise ToolExecutionError(f"Zip extraction failed: {e}") from e

    return [list_dir, read_head, extract_zip]
```

### 2. Implement Agent Lifecycle Callbacks
In `src/agent/core/callbacks.py`:
```python
from typing import Callable, Any
from agent.tools.base import ToolExecutionError

class CallbackManager:
    """Manages lifecycle hooks during agent execution (Ch 5.5)."""

    def __init__(self):
        self.on_tool_call_hooks: list[Callable[[str, dict[str, Any]], None]] = []
        self.on_tool_result_hooks: list[Callable[[str, str], str]] = []

    def register_tool_call_hook(self, hook: Callable[[str, dict[str, Any]], None]) -> None:
        self.on_tool_call_hooks.append(hook)

    def register_result_modifier(self, modifier: Callable[[str, str], str]) -> None:
        self.on_tool_result_hooks.append(modifier)

    def trigger_tool_call(self, name: str, args: dict[str, Any]) -> None:
        for hook in self.on_tool_call_hooks:
            hook(name, args)

    def process_result(self, name: str, result: str) -> str:
        current = result
        for modifier in self.on_tool_result_hooks:
            current = modifier(name, current)
        return current
```

### 3. Human Approval Callback & Result Compactor
```python
def make_human_approval_hook(sensitive_tools: set[str], confirm_fn: Callable[[str], bool]):
    def approval_hook(tool_name: str, args: dict[str, Any]) -> None:
        if tool_name in sensitive_tools:
            allowed = confirm_fn(f"Execute {tool_name} with {args}?")
            if not allowed:
                raise ToolExecutionError(f"Action '{tool_name}' rejected by human operator.")
    return approval_hook

def make_result_truncator(max_chars: int = 1000):
    def truncator(tool_name: str, result: str) -> str:
        if len(result) > max_chars:
            return result[:max_chars] + f"
... [Truncated {len(result) - max_chars} characters]"
        return result
    return truncator
```

---

## ✅ Acceptance Criteria
- [ ] SafeWorkspace blocks path traversal attacks (`../../`).
- [ ] Filesystem tools inspect directories and extract zip archives safely.
- [ ] Callbacks can intercept tool invocations before execution.
- [ ] Result compression callback truncates oversized outputs to save tokens.
