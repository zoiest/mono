# Story 009: Sandboxed CodeAct Engine & Progressive Agent Skills

## User Story
**As an** AI Agent developer,  
**I want to** implement the CodeAct paradigm where the agent writes and executes Python/Bash code inside a sandboxed environment (Docker / E2B) and can load Agent Skills progressively,  
**So that** the agent can manipulate arbitrary files, perform complex calculations, and scale its capabilities dynamically without exhausting prompt token limits.

---

## 📖 Book Alignment
* **Book:** *Build an AI Agent (From Scratch)* ([Study Notes](../bin/build_an_ai_agent_notes.md#chapter-8-empowering-agents-with-code-execution-codeact))
  - Chapter 8: *Empowering agents with code execution* (8.1 Giving agents a computer, 8.2 Sandboxes, 8.3 Porting tools, 8.5 Agent Skills & progressive tool disclosure)
* **Book:** *Effective Python (3rd Edition)* ([Study Notes](../bin/effective_python_v3_notes.md#chapter-9-concurrency-and-parallelism))
  - **Item 72 & 73**: Use `subprocess` to Manage Child Processes; Handle Pipes and Timeouts Safely
  - **Item 84 & 85**: Prevent Resource Leaks; Catch Specific Exceptions
  - **Item 98**: Lazy-Load Modules with Dynamic Imports to Reduce Startup Time
  - **Item 111 & 112**: Use Mocks to Test Code with Complex Sandbox Dependencies

---

## 🎯 What You Will Learn
1. The CodeAct paradigm: writing executable code as universal actions instead of static tools.
2. Sandboxing Python code execution via `subprocess.run` with wall-clock timeouts.
3. Capturing `stdout` and `stderr` safely to feed execution results back into agent reasoning.
4. Implementing progressive tool disclosure (Agent Skills) to reduce prompt token bloat.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Implement Subprocess Sandbox Runner
In `src/agent/sandbox/runner.py`:
```python
import subprocess
import sys
from dataclasses import dataclass
from agent.core.exceptions import AgentBaseException

class SandboxExecutionError(AgentBaseException):
    """Raised when code execution in sandbox fails or times out."""
    pass

@dataclass
class ExecutionResult:
    stdout: str
    stderr: str
    exit_code: int

class LocalSubprocessSandbox:
    """Safely executes generated Python code in isolated subprocess with timeout (Ch 8.2 & Item 72)."""

    def __init__(self, *, default_timeout: float = 15.0):
        self.timeout = default_timeout

    def run_python_code(self, code: str) -> ExecutionResult:
        try:
            completed = subprocess.run(
                [sys.executable, "-c", code],
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )
            return ExecutionResult(
                stdout=completed.stdout,
                stderr=completed.stderr,
                exit_code=completed.returncode,
            )
        except subprocess.TimeoutExpired as e:
            raise SandboxExecutionError(f"Execution timed out after {self.timeout}s.") from e
        except Exception as e:
            raise SandboxExecutionError(f"Subprocess runner failed: {e}") from e
```

### 2. Implement the CodeAct Tool
In `src/agent/tools/codeact_tool.py`:
```python
from agent.tools.base import tool
from agent.sandbox.runner import LocalSubprocessSandbox

def make_codeact_tool(sandbox: LocalSubprocessSandbox):
    @tool(name="execute_python", description="Execute arbitrary Python code in an isolated sandbox environment.")
    def execute_python(code: str) -> str:
        res = sandbox.run_python_code(code)
        output = []
        if res.stdout:
            output.append(f"STDOUT:
{res.stdout}")
        if res.stderr:
            output.append(f"STDERR:
{res.stderr}")
        output.append(f"EXIT CODE: {res.exit_code}")
        return "
".join(output)
    return execute_python
```

### 3. Progressive Skill Disclosure System
In `src/agent/skills/manager.py`:
```python
import importlib
from typing import Any

class SkillRegistry:
    """Progressive disclosure of skills: descriptions upfront, imports on demand (Ch 8.5 & Item 98)."""

    def __init__(self):
        self._skill_catalogue = {
            "excel_analyzer": "agent.skills.excel:analyze_excel",
            "pdf_merger": "agent.skills.pdf:merge_pdfs",
        }

    def get_skill_directory_prompt(self) -> str:
        """Provides brief descriptions of available skills without full schemas."""
        lines = ["Available On-Demand Skills:"]
        for name in self._skill_catalogue:
            lines.append(f"- {name}")
        return "
".join(lines)

    def load_skill(self, name: str) -> Any:
        """Dynamic import only when LLM requests the skill (Item 98)."""
        if name not in self._skill_catalogue:
            raise ValueError(f"Unknown skill: {name}")
        module_path, func_name = self._skill_catalogue[name].split(":")
        mod = importlib.import_module(module_path)
        return getattr(mod, func_name)
```

---

## ✅ Acceptance Criteria
- [ ] `LocalSubprocessSandbox` safely isolates code execution with timeout enforcement.
- [ ] `execute_python` tool returns structured stdout, stderr, and exit codes.
- [ ] Progressive skill loader uses dynamic imports (`importlib`) to load skills on demand.
- [ ] Unit tests mock subprocess execution for fast deterministic testing.
