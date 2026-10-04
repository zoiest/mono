# AI Agent Learning & Implementation Roadmap: User Stories Backlog

A practical curriculum and engineering backlog for building an autonomous AI Agent from scratch while mastering modern Pythonic design patterns, idioms, and engineering best practices.

**Study Notes & References**:
- 📘 [Build an AI Agent Study Notes](file:///home/tofunth/stuffs/mono/gym/ai_agent/bin/build_an_ai_agent_notes.md)
- 🐍 [Effective Python (3rd Edition) Study Notes](file:///home/tofunth/stuffs/mono/gym/ai_agent/bin/effective_python_v3_notes.md)

**Source Literature**:
- 📖 *Build an AI Agent (From Scratch)* — Jungjun Hur & Younghee Song (Manning, 2026)
- 🐍 *Effective Python (3rd Edition)* — Brett Slatkin (Addison-Wesley, 2024 / Python 3.13)

**Individual Story Guides** (Step-by-Step Code Examples):
- 📁 [stories/ Directory](file:///home/tofunth/stuffs/mono/gym/ai_agent/stories/)

**GitHub Project Board**: [https://github.com/users/zoiest/projects/3/](https://github.com/users/zoiest/projects/3/)

---

## Story Overview & Progress Map

| Story ID | Title | Priority | Size | Status | Key Agent Concepts | Effective Python Items |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| [**Story 1**](file:///home/tofunth/stuffs/mono/gym/ai_agent/stories/001_project_architecture_and_llm_client.md) | Project Architecture & Provider-Agnostic LLM Client | **P0** | **M** | `Ready` | Architecture, LiteLLM Adapter, Streaming | Items 1, 2, 31, 36, 37, 117-121, 124 |
| [**Story 2**](file:///home/tofunth/stuffs/mono/gym/ai_agent/stories/002_extensible_tool_calling_and_mcp.md) | Extensible Tool Calling Engine & MCP Protocol | **P0** | **L** | `Backlog` | Function Calling, Schemas, Calc/Search, MCP | Items 26-29, 32, 38, 50, 111, 112 |
| [**Story 3**](file:///home/tofunth/stuffs/mono/gym/ai_agent/stories/003_react_reasoning_loop_and_execution_context.md) | ReAct Reasoning Loop & ExecutionContext Engine | **P0** | **L** | `Backlog` | ReAct Cycle, State Machine, Stop Guards | Items 8, 9, 12, 19, 20, 21, 87 |
| [**Story 4**](file:///home/tofunth/stuffs/mono/gym/ai_agent/stories/004_rag_knowledge_base_and_vector_search.md) | RAG Knowledge Base, Vector Search & Chunking | **P1** | **M** | `Backlog` | Embeddings, Chunking, Top-K Vector Search | Items 24, 40, 43, 99, 100, 101, 104 |
| [**Story 5**](file:///home/tofunth/stuffs/mono/gym/ai_agent/stories/005_filesystem_tools_and_execution_callbacks.md) | Filesystem Navigation Tools & Execution Callbacks | **P1** | **M** | `Backlog` | File/Zip Tools, GAIA Gym, Callbacks, HITL | Items 26, 28, 33, 39, 86, 110 |
| [**Story 6**](file:///home/tofunth/stuffs/mono/gym/ai_agent/stories/006_context_engineering_sliding_windows_and_compaction.md) | Context Engineering, Sliding Windows & Compaction | **P0** | **L** | `Backlog` | Token Accounting, Deque, Compaction, Summary | Items 4, 22, 23, 103, 115 |
| [**Story 7**](file:///home/tofunth/stuffs/mono/gym/ai_agent/stories/007_multiturn_sessions_hitl_and_chromadb.md) | Multiturn Sessions, HITL Pause/Resume & ChromaDB | **P1** | **L** | `Backlog` | SessionManager, Pause/Resume, TaskMemory | Items 27, 28, 31, 87, 105, 107 |
| [**Story 8**](file:///home/tofunth/stuffs/mono/gym/ai_agent/stories/008_metacognitive_planning_and_reflection.md) | Metacognitive Task Planning & Reflection Engine | **P1** | **M** | `Backlog` | Plan-and-Solve, Self-Critique, Replanning | Items 4, 9, 11, 31, 54 |
| [**Story 9**](file:///home/tofunth/stuffs/mono/gym/ai_agent/stories/009_sandboxed_codeact_and_progressive_skills.md) | Sandboxed CodeAct Engine & Progressive Skills | **P0** | **XL** | `Backlog` | CodeAct, Docker/E2B Sandbox, Dynamic Skills | Items 72, 73, 84, 85, 98, 111, 116 |
| [**Story 10**](file:///home/tofunth/stuffs/mono/gym/ai_agent/stories/010_multi_agent_collaboration_and_workflows.md) | Multi-Agent Collaboration: Workflows & Handoffs | **P1** | **XL** | `Backlog` | Workflows, Agent-as-Tool, Agent Transfer | Items 18, 50, 77-83, 103 |
| [**Story 11**](file:///home/tofunth/stuffs/mono/gym/ai_agent/stories/011_agent_to_agent_a2a_protocol_and_mesh.md) | Agent-to-Agent (A2A) Network Protocol & Mesh | **P2** | **L** | `Backlog` | Agent Cards, HTTP/SSE, Distributed Mesh | Items 81, 82, 118, 119, 121, 124 |
| [**Story 12**](file:///home/tofunth/stuffs/mono/gym/ai_agent/stories/012_opentelemetry_tracing_and_gaia_eval.md) | OpenTelemetry Tracing, GAIA Eval & LLM-as-Judge | **P0** | **L** | `Backlog` | Observability, Traces, GAIA Benchmark, CI/CD | Items 94-96, 108-113, 118 |

---

## Detailed User Stories

### [Story 1: Project Architecture & Provider-Agnostic LLM Client](file:///home/tofunth/stuffs/mono/gym/ai_agent/stories/001_project_architecture_and_llm_client.md) Project Architecture & Provider-Agnostic LLM Client
- **User Story**:
  - **As an** AI Agent developer,
  - **I want to** establish a clean Python project package structure and implement an abstract, provider-agnostic LLM client (supporting OpenAI, Anthropic, Gemini via LiteLLM) with streaming and structured output,
  - **So that** the agent codebase has clean separation of concerns, strict type safety, predictable error handling, and vendor portability.
- **Book References**:
  - *Build an AI Agent* ([Notes](file:///home/tofunth/stuffs/mono/gym/ai_agent/bin/build_an_ai_agent_notes.md)): Chapters 1 & 2 (LLM fundamentals, LiteLLM provider adapter, structured outputs, async calls).
  - *Effective Python* ([Notes](file:///home/tofunth/stuffs/mono/gym/ai_agent/bin/effective_python_v3_notes.md)): Items 1, 2, 31, 36, 37, 117-121, 124.
- **Technical Scope**:
  - Layout: `src/agent/core/`, `src/agent/llm/`, `src/agent/tools/`, `tests/`.
  - Packaging with `pyproject.toml` (Ruff, Mypy, Pytest).
  - Abstract `LlmClient` Protocol & `LiteLlmClient` implementation.
  - Root exceptions: `AgentBaseException`, `LlmProviderError`, `ModelTimeoutError`.
  - Dataclass response objects (`ModelResponse`, `TokenUsage`).
- **Acceptance Criteria**:
  - [ ] Strict type checking passes (`mypy --strict`).
  - [ ] Provider switching functions without changing consumer agent code.
  - [ ] Unit tests with mocks verify error propagation and response parsing.

---

### [Story 2: Extensible Tool Calling Engine & MCP Protocol Integration](file:///home/tofunth/stuffs/mono/gym/ai_agent/stories/002_extensible_tool_calling_and_mcp.md) Extensible Tool Calling Engine & MCP Protocol Integration
- **User Story**:
  - **As an** AI Agent developer,
  - **I want to** build a declarative tool definition framework with automated JSON schema extraction, runtime validation, and support for Model Context Protocol (MCP),
  - **So that** the LLM can safely discover, validate, and execute local tools (calculator, web search) as well as remote MCP server capabilities.
- **Book References**:
  - *Build an AI Agent* ([Notes](file:///home/tofunth/stuffs/mono/gym/ai_agent/bin/build_an_ai_agent_notes.md)): Chapter 3 (Tool calling mechanics, schemas, calculator, web search, MCP).
  - *Effective Python* ([Notes](file:///home/tofunth/stuffs/mono/gym/ai_agent/bin/effective_python_v3_notes.md)): Items 26-29, 32, 38, 50, 111, 112.
- **Technical Scope**:
  - `@tool` decorator leveraging `functools.wraps` and inspect module.
  - `ToolRegistry` with schema generation.
  - Built-in Calculator and Web Search tools.
  - Model Context Protocol (MCP) client connector.
- **Acceptance Criteria**:
  - [ ] Decorator correctly produces valid OpenAPI/JSONSchema specs.
  - [ ] Input arguments validated against type annotations before execution.
  - [ ] Domain-specific exceptions (`ToolExecutionError`) cleanly raised.
  - [ ] MCP client discovers and executes remote tools.

---

### [Story 3: The ReAct Reasoning Loop & ExecutionContext Engine](file:///home/tofunth/stuffs/mono/gym/ai_agent/stories/003_react_reasoning_loop_and_execution_context.md) The ReAct Reasoning Loop & ExecutionContext Engine
- **User Story**:
  - **As an** AI Agent developer,
  - **I want to** implement the core ReAct (Thought-Action-Observation) reasoning engine powered by an `ExecutionContext` state container,
  - **So that** the agent can autonomously reason about tasks, select and execute tools, process observations, and converge on final solutions while preventing runaway loops.
- **Book References**:
  - *Build an AI Agent* ([Notes](file:///home/tofunth/stuffs/mono/gym/ai_agent/bin/build_an_ai_agent_notes.md)): Chapter 4 (ExecutionContext, `run()`, `step()`, `think()`, `act()`, stop conditions).
  - *Effective Python* ([Notes](file:///home/tofunth/stuffs/mono/gym/ai_agent/bin/effective_python_v3_notes.md)): Items 8, 9, 12, 19, 20, 21, 87.
- **Technical Scope**:
  - Stateful `ExecutionContext` with immutable step logs.
  - ReAct agent methods: `run()`, `step()`, `think()`, `act()`.
  - Loop guards: `max_iterations`, loop detection heuristics.
  - `match...case` pattern matching on tool calls vs final stop tokens.
- **Acceptance Criteria**:
  - [ ] End-to-end execution solves multi-hop questions.
  - [ ] Loop guards raise `MaxStepsExceededException` when threshold reached.
  - [ ] State history cleanly formatted with `repr`/`str`.

---

### [Story 4: RAG Knowledge Base, Vector Search & Text Chunking Pipeline](file:///home/tofunth/stuffs/mono/gym/ai_agent/stories/004_rag_knowledge_base_and_vector_search.md) RAG Knowledge Base, Vector Search & Text Chunking Pipeline
- **User Story**:
  - **As an** AI Agent developer,
  - **I want to** build a Retrieval-Augmented Generation (RAG) subsystem with text chunking, embedding generation, and vector similarity search,
  - **So that** the agent can ground its reasoning and tool answers on external documents, knowledge bases, and fetched web content without hallucinating.
- **Book References**:
  - *Build an AI Agent* ([Notes](file:///home/tofunth/stuffs/mono/gym/ai_agent/bin/build_an_ai_agent_notes.md)): Chapter 5.1 - 5.3 (Vector search, embeddings, chunking, vector indexing).
  - *Effective Python* ([Notes](file:///home/tofunth/stuffs/mono/gym/ai_agent/bin/effective_python_v3_notes.md)): Items 24, 40, 43, 99, 100, 101, 104.
- **Technical Scope**:
  - Chunking generator functions yielding overlapping text chunks.
  - In-memory vector store using cosine similarity and `heapq.nlargest` for top-K retrieval.
  - `knowledge_base_search` tool integrated into the agent tool registry.
- **Acceptance Criteria**:
  - [ ] Generator-based chunking processes large documents without memory spikes.
  - [ ] Cosine similarity search retrieves relevant passages accurately.
  - [ ] Agent leverages retrieved passages to answer domain queries.

---

### [Story 5: Filesystem Navigation Tools & Agent Execution Callbacks](file:///home/tofunth/stuffs/mono/gym/ai_agent/stories/005_filesystem_tools_and_execution_callbacks.md) Filesystem Navigation Tools & Agent Execution Callbacks
- **User Story**:
  - **As an** AI Agent developer,
  - **I want to** provide the agent with safe filesystem exploration tools (directory listing, file reading, zip archive extraction) and an extensible callback system,
  - **So that** the agent can inspect complex local directory structures to solve GAIA benchmark tasks while allowing humans to approve sensitive actions and compress outputs.
- **Book References**:
  - *Build an AI Agent* ([Notes](file:///home/tofunth/stuffs/mono/gym/ai_agent/bin/build_an_ai_agent_notes.md)): Chapter 5.4 - 5.5 (GAIA filesystem tools, callbacks, human approval, result compression).
  - *Effective Python* ([Notes](file:///home/tofunth/stuffs/mono/gym/ai_agent/bin/effective_python_v3_notes.md)): Items 26, 28, 33, 39, 86, 110.
- **Technical Scope**:
  - Secure filesystem tools (`list_directory`, `read_file_head`, `extract_zip_archive`).
  - Sandbox path validation preventing directory traversal.
  - Agent callback hooks: `on_step_start`, `on_tool_call`, `on_tool_result`, `on_step_end`.
  - Human-in-the-loop (HITL) approval callback and result compression callback.
- **Acceptance Criteria**:
  - [ ] Safe filesystem traversal prevents unauthorized path escapes.
  - [ ] Callback pipeline allows non-invasive hooking into execution events.
  - [ ] HITL callback pauses execution until user approval.

---

### [Story 6: Context Engineering, Sliding-Window Memory & Token Budget Compactor](file:///home/tofunth/stuffs/mono/gym/ai_agent/stories/006_context_engineering_sliding_windows_and_compaction.md) Context Engineering, Sliding-Window Memory & Token Budget Compactor
- **User Story**:
  - **As an** AI Agent developer,
  - **I want to** implement intelligent context engineering with exact token counting, bounded sliding-window buffers, compaction, and recursive summarization,
  - **So that** the agent avoids context window exhaustion, maintains low token costs, and prevents needle-in-a-haystack memory degradation during long executions.
- **Book References**:
  - *Build an AI Agent* ([Notes](file:///home/tofunth/stuffs/mono/gym/ai_agent/bin/build_an_ai_agent_notes.md)): Chapter 6.1 - 6.2 (Anatomy of memory, sliding window, token counting, compaction, summarization).
  - *Effective Python* ([Notes](file:///home/tofunth/stuffs/mono/gym/ai_agent/bin/effective_python_v3_notes.md)): Items 4, 22, 23, 103, 115.
- **Technical Scope**:
  - Token counting module using `tiktoken`.
  - `collections.deque(maxlen=K)` sliding-window buffer preserving system prompt.
  - Observation compaction and background LLM summarization.
  - Memory leak verification with `tracemalloc`.
- **Acceptance Criteria**:
  - [ ] Bounded context prevents context overflow errors.
  - [ ] Compaction reduces token size while preserving semantic content.
  - [ ] `tracemalloc` verifies zero memory leaks across 100+ simulated steps.

---

### [Story 7: Multiturn Sessions, HITL Pause/Resume & Long-Term Memory (ChromaDB)](file:///home/tofunth/stuffs/mono/gym/ai_agent/stories/007_multiturn_sessions_hitl_and_chromadb.md) Multiturn Sessions, HITL Pause/Resume & Long-Term Memory (ChromaDB)
- **User Story**:
  - **As an** AI Agent developer,
  - **I want to** implement stateful `SessionManager` with pause-and-resume workflows for human approvals, and an episodic long-term memory store using ChromaDB,
  - **So that** agent conversations persist across sessions, human-in-the-loop workflows run asynchronously, and agents learn facts and user preferences across distinct interactions.
- **Book References**:
  - *Build an AI Agent* ([Notes](file:///home/tofunth/stuffs/mono/gym/ai_agent/bin/build_an_ai_agent_notes.md)): Chapter 6.3 - 6.4 (SessionManager, pause/resume, ChromaDB TaskMemoryManager).
  - *Effective Python* ([Notes](file:///home/tofunth/stuffs/mono/gym/ai_agent/bin/effective_python_v3_notes.md)): Items 27, 28, 31, 87, 105, 107.
- **Technical Scope**:
  - `Session` and `SessionManager` with JSON-safe serialization.
  - Execution state suspension and resumption upon human response.
  - ChromaDB vector store for long-term memory extraction and retrieval.
- **Acceptance Criteria**:
  - [ ] Sessions persist across process restarts.
  - [ ] Pause-and-resume workflow halts execution and resumes seamlessly upon approval.
  - [ ] Episodic facts are stored and retrieved semantically in subsequent sessions.

---

### [Story 8: Metacognitive Task Planning, Decomposition & Reflection Engine](file:///home/tofunth/stuffs/mono/gym/ai_agent/stories/008_metacognitive_planning_and_reflection.md) Metacognitive Task Planning, Decomposition & Reflection Engine
- **User Story**:
  - **As an** AI Agent developer,
  - **I want to** empower the agent with explicit task decomposition, milestone planning, and self-reflection tools,
  - **So that** the agent can systematically solve complex multi-hop problems, monitor its own progress, detect errors, and recover from failures without user intervention.
- **Book References**:
  - *Build an AI Agent* ([Notes](file:///home/tofunth/stuffs/mono/gym/ai_agent/bin/build_an_ai_agent_notes.md)): Chapter 7 (Planning and reflection, plan-and-solve, self-critique, error recovery).
  - *Effective Python* ([Notes](file:///home/tofunth/stuffs/mono/gym/ai_agent/bin/effective_python_v3_notes.md)): Items 4, 9, 11, 31, 54.
- **Technical Scope**:
  - Structured plan data model (`Plan`, `PlanStep`) and `planning_tool`.
  - `reflection_tool` for evaluating intermediate outputs against plan goals.
  - Automated failure recovery triggered on repeated tool errors.
- **Acceptance Criteria**:
  - [ ] Agent generates and tracks milestone plans for complex queries.
  - [ ] Reflection tool detects faulty intermediate steps and triggers replanning.
  - [ ] `match...case` cleanly dispatches based on plan step statuses.

---

### [Story 9: Sandboxed CodeAct Engine & Progressive Agent Skills](file:///home/tofunth/stuffs/mono/gym/ai_agent/stories/009_sandboxed_codeact_and_progressive_skills.md) Sandboxed CodeAct Engine & Progressive Agent Skills
- **User Story**:
  - **As an** AI Agent developer,
  - **I want to** implement the CodeAct paradigm where the agent writes and executes Python/Bash code inside a sandboxed environment (Docker / E2B) and can load Agent Skills progressively,
  - **So that** the agent can manipulate arbitrary files, perform complex calculations, and scale its capabilities dynamically without exhausting prompt token limits.
- **Book References**:
  - *Build an AI Agent* ([Notes](file:///home/tofunth/stuffs/mono/gym/ai_agent/bin/build_an_ai_agent_notes.md)): Chapter 8 (CodeAct, sandboxes, E2B/Docker, workspace CLI, progressive tool disclosure / Agent Skills).
  - *Effective Python* ([Notes](file:///home/tofunth/stuffs/mono/gym/ai_agent/bin/effective_python_v3_notes.md)): Items 72, 73, 84, 85, 98, 111, 116.
- **Technical Scope**:
  - `SandboxRunner` interface supporting Docker/E2B environments.
  - CodeAct execution loop with stdout/stderr capture and timeouts.
  - Dynamic skill loading mechanism using dynamic imports (`importlib`).
- **Acceptance Criteria**:
  - [ ] Safe execution of Python/Bash scripts inside isolated sandbox.
  - [ ] Progressive tool disclosure loads tool definitions on demand, cutting prompt token usage by >40%.
  - [ ] Execution errors fed back to agent for autonomous debugging.

---

### [Story 10: Multi-Agent Collaboration: Workflows, Agent-as-Tool & Handoffs](file:///home/tofunth/stuffs/mono/gym/ai_agent/stories/010_multi_agent_collaboration_and_workflows.md) Multi-Agent Collaboration: Workflows, Agent-as-Tool & Handoffs
- **User Story**:
  - **As an** AI Agent developer,
  - **I want to** build multi-agent orchestration architectures supporting Workflows (Sequential/Parallel/Loop), Agent-as-Tool, and Agent Transfer (Handoff trees),
  - **So that** specialized agents (e.g. Researcher, Coder, Reviewer) can collaborate on complex projects with isolated contexts and clear separation of responsibility.
- **Book References**:
  - *Build an AI Agent* ([Notes](file:///home/tofunth/stuffs/mono/gym/ai_agent/bin/build_an_ai_agent_notes.md)): Chapter 9.1 - 9.5 (Multi-agent patterns, sequential/parallel/loop workflows, AgentTool, context isolation, Agent Transfer).
  - *Effective Python* ([Notes](file:///home/tofunth/stuffs/mono/gym/ai_agent/bin/effective_python_v3_notes.md)): Items 18, 50, 77-83, 103.
- **Technical Scope**:
  - Workflows: Sequential, Parallel (`asyncio.TaskGroup`), Iterative loops.
  - `AgentTool` pattern for isolated sub-agent execution.
  - Agent Transfer pattern for hierarchical delegation trees.
- **Acceptance Criteria**:
  - [ ] Parallel agents execute concurrently with `asyncio.TaskGroup` and `ExceptionGroup`.
  - [ ] `AgentTool` prevents child agent thought scratchpads from bloating parent context.
  - [ ] Multi-agent collaboration completes complex end-to-end task.

---

### [Story 11: Agent-to-Agent (A2A) Protocol & Distributed Network Agent Mesh](file:///home/tofunth/stuffs/mono/gym/ai_agent/stories/011_agent_to_agent_a2a_protocol_and_mesh.md) Agent-to-Agent (A2A) Protocol & Distributed Network Agent Mesh
- **User Story**:
  - **As an** AI Agent developer,
  - **I want to** implement the Agent-to-Agent (A2A) protocol with standardized Agent Cards and HTTP/SSE endpoints,
  - **So that** agents distributed across different machines, processes, and network boundaries can advertise capabilities and collaborate remotely.
- **Book References**:
  - *Build an AI Agent* ([Notes](file:///home/tofunth/stuffs/mono/gym/ai_agent/bin/build_an_ai_agent_notes.md)): Chapter 9.6 (A2A protocol, Agent Card specification, task request/response contracts, A2A Server/Client).
  - *Effective Python* ([Notes](file:///home/tofunth/stuffs/mono/gym/ai_agent/bin/effective_python_v3_notes.md)): Items 81, 82, 118, 119, 121, 124.
- **Technical Scope**:
  - Pydantic `AgentCard` schema and endpoint `/.well-known/agent.json`.
  - FastAPI / ASGI server for handling tasks and SSE streaming.
  - `RemoteAgentClient` for cross-network discovery and invocation.
- **Acceptance Criteria**:
  - [ ] Agent Cards conform to standard JSON schema.
  - [ ] Remote agent callable as if it were a local tool.
  - [ ] Network failures and timeouts handled gracefully with typed exceptions.

---

### [Story 12: OpenTelemetry Tracing, GAIA Evaluation & LLM-as-a-Judge](file:///home/tofunth/stuffs/mono/gym/ai_agent/stories/012_opentelemetry_tracing_and_gaia_eval.md) OpenTelemetry Tracing, GAIA Evaluation & LLM-as-a-Judge
- **User Story**:
  - **As an** AI Agent developer,
  - **I want to** instrument the agent with OpenTelemetry tracing and build an automated evaluation pipeline using GAIA benchmark datasets and LLM-as-a-Judge rubrics in CI/CD,
  - **So that** I can observe internal agent steps, measure accuracy and latency quantitatively, and continuously prevent regressions with an agent quality flywheel.
- **Book References**:
  - *Build an AI Agent* ([Notes](file:///home/tofunth/stuffs/mono/gym/ai_agent/bin/build_an_ai_agent_notes.md)): Chapters 1.4, 2.4, 4.8, 10 (OpenTelemetry, GAIA benchmark runner, LLM-as-a-judge rubrics, CI/CD flywheel).
  - *Effective Python* ([Notes](file:///home/tofunth/stuffs/mono/gym/ai_agent/bin/effective_python_v3_notes.md)): Items 94-96, 108-113, 118.
- **Technical Scope**:
  - OpenTelemetry tracer instrumenting runs, steps, LLM calls, and tool executions.
  - Rubric-based LLM-as-a-judge evaluation harness.
  - GAIA benchmark runner and GitHub Actions CI workflow with mocks.
- **Acceptance Criteria**:
  - [ ] Detailed spans and traces exported to OpenTelemetry collector/console.
  - [ ] Evaluator scores outputs against ground-truth rubrics.
  - [ ] CI pipeline validates pull requests without consuming live API tokens.
