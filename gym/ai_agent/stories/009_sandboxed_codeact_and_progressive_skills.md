# Story 009: Sandboxed CodeAct for Quantitative & Technical Analysis

## User Story
**As a** quantitative research developer,  
**I want to** enable the CodeAct paradigm so the agent can write and execute Python code in an isolated sandbox (running Pandas, NumPy, TA-Lib),  
**So that** the agent can compute custom technical indicators (RSI, Moving Averages, Volatility) and correlate pricing data with news release dates on the fly.

---

## 📖 Book Alignment
* **Book:** *Build an AI Agent (From Scratch)* ([Study Notes](../writings/build_an_ai_agent_notes.md#chapter-8-empowering-agents-with-code-execution-codeact))
  - Chapter 8: *Empowering agents with code execution* (8.1 Giving agents a computer, 8.2 Sandboxes, 8.3 Porting tools, 8.5 Agent Skills & progressive tool disclosure)
* **Book:** *Effective Python (3rd Edition)* ([Study Notes](../writings/effective_python_v3_notes.md#chapter-9-concurrency-and-parallelism))
  - **Item 72 & 73**: Use `subprocess` Safely with Timeouts and Stdio Capture
  - **Item 84 & 85**: Prevent Resource Leaks with Context Managers; Catch Specific Exceptions
  - **Item 98**: Lazy-Load Modules with Dynamic Imports to Reduce Startup
  - **Item 111 & 112**: Use Mocks to Test Complex Sandbox Dependencies

---

## 🎯 What You Will Learn
1. The CodeAct paradigm for financial intelligence: letting LLMs write scripts for arbitrary quantitative analysis.
2. Executing untrusted Python scripts safely in a subprocess sandbox with timeout constraints.
3. Capturing stdout calculations (e.g. 50-day SMA, 200-day SMA, RSI) and feeding them back into reasoning context.
4. Implementing progressive skill disclosure (importing heavy quantitative libraries on demand).

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Subprocess Quant Sandbox Runner
In `src/agent/sandbox/quant_runner.py`:
```python
import subprocess
import sys
from dataclasses import dataclass
from agent.core.exceptions import FinancialAgentException

class SandboxTimeoutError(FinancialAgentException):
    pass

@dataclass
class QuantExecutionResult:
    stdout: str
    stderr: str
    exit_code: int

class LocalQuantSandbox:
    """Executes financial Python analysis scripts in isolated child processes (Ch 8.2 & Item 72)."""

    def __init__(self, timeout: float = 15.0):
        self.timeout = timeout

    def execute_script(self, code: str) -> QuantExecutionResult:
        try:
            res = subprocess.run(
                [sys.executable, "-c", code],
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )
            return QuantExecutionResult(res.stdout, res.stderr, res.returncode)
        except subprocess.TimeoutExpired as e:
            raise SandboxTimeoutError(f"Quant analysis exceeded {self.timeout}s timeout.") from e
```

### 2. Expose the CodeAct Execution Tool
In `src/agent/tools/quant_tool.py`:
```python
from agent.tools.base import tool
from agent.sandbox.quant_runner import LocalQuantSandbox

def make_quant_code_tool(sandbox: LocalQuantSandbox):
    @tool(name="execute_quant_code", description="Run Python code to calculate technical indicators or analyze price arrays.")
    def run_quant_code(python_code: str) -> str:
        result = sandbox.execute_script(python_code)
        output = []
        if result.stdout:
            output.append(f"CALCULATION RESULTS:
{result.stdout}")
        if result.stderr:
            output.append(f"ERRORS:
{result.stderr}")
        return "
".join(output) if output else "Script executed with empty output."
    return run_quant_code
```

---

## ✅ Acceptance Criteria
- [ ] Quant sandbox runs Python scripts with strict timeout limits.
- [ ] Agent successfully writes code to calculate financial indicators (e.g. moving averages, price changes).
- [ ] Script results are fed back into agent execution context as observations.
- [ ] Syntax or runtime errors are caught cleanly and returned to the model for self-correction.
