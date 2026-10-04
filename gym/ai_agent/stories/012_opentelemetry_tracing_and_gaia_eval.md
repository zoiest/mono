# Story 012: Financial Signal Evaluation, Backtesting & LLM-as-a-Judge

## User Story
**As a** quantitative research developer,  
**I want to** instrument the agent with OpenTelemetry tracing and build an automated evaluation pipeline using historical earnings surprises and LLM-as-a-Judge rubrics in CI/CD,  
**So that** we can quantitatively measure ticker signal precision, monitor token costs per ticker, and prevent performance regressions.

---

## 📖 Book Alignment
* **Book:** *Build an AI Agent (From Scratch)* ([Study Notes](../writings/build_an_ai_agent_notes.md#chapter-10-evaluating-agents))
  - Chapter 10: *Evaluating agents* (10.1 Observing an agent, OpenTelemetry, 10.2 Datasets & rubrics, 10.3 LLM-as-a-judge, 10.4 Operations & CI/CD)
* **Book:** *Effective Python (3rd Edition)* ([Study Notes](../writings/effective_python_v3_notes.md#chapter-13-testing-and-debugging))
  - **Item 94–96**: Profile Performance Bottlenecks with `cProfile`
  - **Item 108–110**: Verify Behaviors in `TestCase` Subclasses; Prefer Integration Tests; Isolate Tests
  - **Item 111 & 112**: Use Mocks to Test Complex Dependencies in CI
  - **Item 113**: Use `assertAlmostEqual` / `pytest.approx` to Control Precision in Floating Point Evaluation Metrics

---

## 🎯 What You Will Learn
1. Instrumenting ticker analysis runs and tool dispatches with OpenTelemetry tracing.
2. Creating a financial benchmark dataset of historical earnings headlines and subsequent price moves.
3. Implementing an LLM-as-a-Judge to evaluate reasoning rigor and penalize hallucinated numbers.
4. Setting up a mock-based regression test suite for GitHub Actions CI.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Instrument Financial Agent with OpenTelemetry
In `src/agent/telemetry/tracer.py`:
```python
from contextlib import contextmanager
from typing import Iterator

class FinancialAgentTracer:
    """Generates distributed traces across ticker analysis runs and news queries (Ch 10.1)."""

    @contextmanager
    def span(self, name: str, ticker: str) -> Iterator[None]:
        print(f"[TRACE START] {name} for {ticker}")
        try:
            yield
        finally:
            print(f"[TRACE END] {name} for {ticker}")
```

### 2. Implement Financial Signal Judge
In `src/agent/eval/financial_judge.py`:
```python
from dataclasses import dataclass
from agent.llm.client import LlmClient

@dataclass
class FinancialSignalVerdict:
    passed: bool
    score: float  # 0.0 to 1.0
    critique: str

class FinancialSignalJudge:
    def __init__(self, llm: LlmClient):
        self.llm = llm

    async def evaluate_signal(self, ticker: str, agent_output: str, ground_truth_catalyst: str) -> FinancialSignalVerdict:
        prompt = (
            f"You are a Senior Quantitative Portfolio Manager judging an AI equity analyst.
"
            f"Ticker: {ticker}
"
            f"Ground Truth Reality: {ground_truth_catalyst}
"
            f"Agent Thesis: {agent_output}

"
            f"Evaluate if the agent captured the true catalyst. Output 'VERDICT: PASS' or 'VERDICT: FAIL'."
        )
        res = await self.llm.complete([{"role": "user", "content": prompt}])
        content = res.content or ""
        passed = "VERDICT: PASS" in content
        return FinancialSignalVerdict(passed=passed, score=1.0 if passed else 0.0, critique=content)
```

### 3. CI Regression Test Harness
In `tests/test_signal_eval_regression.py`:
```python
import pytest

def test_signal_accuracy_score_tolerance():
    accuracy = 0.8499999
    # Control floating point tolerances (Item 113)
    assert accuracy == pytest.approx(0.85, abs=1e-3)
```

---

## ✅ Acceptance Criteria
- [ ] OpenTelemetry tracer generates spans for `ticker.analyze`, news fetching, and tool calls.
- [ ] `FinancialSignalJudge` evaluates reasoning validity against ground-truth earnings surprises.
- [ ] Score metrics verified with `pytest.approx` and floating-point tolerances.
- [ ] CI suite runs deterministically without consuming live API tokens.
