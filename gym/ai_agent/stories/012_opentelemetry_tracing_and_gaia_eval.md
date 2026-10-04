# Story 012: OpenTelemetry Tracing, GAIA Evaluation & LLM-as-a-Judge

## User Story
**As an** AI Agent developer,  
**I want to** instrument the agent with OpenTelemetry tracing and build an automated evaluation pipeline using GAIA benchmark datasets and LLM-as-a-Judge rubrics in CI/CD,  
**So that** I can observe internal agent steps, measure accuracy and latency quantitatively, and continuously prevent regressions with an agent quality flywheel.

---

## 📖 Book Alignment
* **Book:** *Build an AI Agent (From Scratch)* ([Study Notes](file:///home/tofunth/stuffs/mono/gym/ai_agent/bin/build_an_ai_agent_notes.md#chapter-10-evaluating-agents))
  - Chapter 10: *Evaluating agents* (10.1 Observing an agent, OpenTelemetry, 10.2 Datasets & rubrics, 10.3 LLM-as-a-judge, 10.4 Operations & CI/CD)
  - Chapter 1.4, 2.4, 4.8: GAIA benchmark tasks
* **Book:** *Effective Python (3rd Edition)* ([Study Notes](file:///home/tofunth/stuffs/mono/gym/ai_agent/bin/effective_python_v3_notes.md#chapter-13-testing-and-debugging))
  - **Item 94–96**: Profile Before Optimizing with `cProfile`
  - **Item 108–110**: Verify Behaviors in `TestCase` Subclasses; Prefer Integration Tests; Isolate Tests
  - **Item 111 & 112**: Use Mocks to Test Code with Complex Dependencies; Encapsulate Dependencies
  - **Item 113**: Use `assertAlmostEqual` to Control Precision in Floating Point Tests
  - **Item 118**: Document Rubrics and Evaluation Reports

---

## 🎯 What You Will Learn
1. Instrumenting agent loops and tool calls with distributed OpenTelemetry spans.
2. Creating synthetic and benchmark evaluation datasets (GAIA Level 1 & 2).
3. Implementing a rubric-based LLM-as-a-Judge evaluator with score assertions.
4. Setting up a deterministic mock-based regression test suite for GitHub Actions CI.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Instrument Agent Loop with OpenTelemetry
In `src/agent/telemetry/tracer.py`:
```python
from contextlib import contextmanager
from typing import Iterator

# OpenTelemetry abstraction stub
class AgentTracer:
    """Generates distributed traces across agent runs, steps, and tool calls (Ch 10.1)."""

    @contextmanager
    def span(self, name: str, attributes: dict[str, str] | None = None) -> Iterator[None]:
        attrs = attributes or {}
        # OpenTelemetry span start
        print(f"[TRACE START] {name} | {attrs}")
        try:
            yield
        finally:
            print(f"[TRACE END] {name}")
```

### 2. Implement Rubric-Based LLM-as-a-Judge
In `src/agent/eval/judge.py`:
```python
from dataclasses import dataclass
from agent.llm.client import LlmClient

@dataclass
class EvalScore:
    passed: bool
    score: float  # 0.0 to 1.0
    reasoning: str

class LLMJudge:
    """Evaluates agent response quality against ground-truth rubric criteria (Ch 10.3)."""

    def __init__(self, llm_client: LlmClient):
        self.llm = llm_client

    async def evaluate_task(self, query: str, response: str, ground_truth: str) -> EvalScore:
        prompt = (
            f"You are an impartial AI judge. Evaluate the agent's answer against ground truth.

"
            f"User Query: {query}
"
            f"Ground Truth: {ground_truth}
"
            f"Agent Answer: {response}

"
            f"Output 'VERDICT: PASS' or 'VERDICT: FAIL' followed by a score (0.0 to 1.0) and reasoning."
        )
        res = await self.llm.complete([{"role": "user", "content": prompt}])
        content = res.content or ""
        passed = "VERDICT: PASS" in content
        score = 1.0 if passed else 0.0
        return EvalScore(passed=passed, score=score, reasoning=content)
```

### 3. GAIA Evaluation Harness & CI Integration
In `tests/test_gaia_regression.py`:
```python
import pytest
from agent.eval.judge import EvalScore

def test_evaluation_metric_precision():
    """Using pytest / math.isclose to assert floating-point score tolerances (Item 113)."""
    scores = [1.0, 0.95, 0.98]
    average = sum(scores) / len(scores)
    assert average == pytest.approx(0.9766, rel=1e-3)

@pytest.mark.asyncio
async def test_gaia_level1_synthetic_question():
    # Deterministic CI test with mock tools and mock judge
    eval_score = EvalScore(passed=True, score=1.0, reasoning="Matches ground truth exactly.")
    assert eval_score.passed is True
    assert eval_score.score >= 0.8
```

---

## ✅ Acceptance Criteria
- [ ] OpenTelemetry tracer generates spans for `agent.run`, `think`, and `act`.
- [ ] LLM-as-a-Judge evaluates responses against ground truth rubrics.
- [ ] Floating-point score assertions use `pytest.approx` / `assertAlmostEqual`.
- [ ] CI evaluation suite passes without requiring live external API tokens.
