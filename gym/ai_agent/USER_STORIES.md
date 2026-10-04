# Financial AI Agent Roadmap: News & Signal Extraction Pipeline

A practical engineering curriculum and backlog for building an autonomous **Financial Intelligence & Signal Extraction AI Agent Pipeline** from scratch, mastering modern Pythonic design patterns, idioms, and engineering best practices.

**Source Literature**:
- 📖 *Build an AI Agent (From Scratch)* — Jungjun Hur & Younghee Song (Manning, 2026)
- 🐍 *Effective Python (3rd Edition)* — Brett Slatkin (Addison-Wesley, 2024 / Python 3.13)

**Study Notes & References**:
- 📘 [Build an AI Agent Study Notes](bin/build_an_ai_agent_notes.md)
- 🐍 [Effective Python (3rd Edition) Study Notes](bin/effective_python_v3_notes.md)

**Individual Story Guides** (Step-by-Step Code Examples):
- 📁 [stories/ Directory](stories/)

**GitHub Project Board**: [https://github.com/users/zoiest/projects/3/](https://github.com/users/zoiest/projects/3/)

---

## Story Overview & Progress Map

| Story ID | Title | Priority | Size | Status | Key Agent Concepts | Effective Python Items |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| [**Story 001**](stories/001_project_architecture_and_llm_client.md) | Setup & Financial LLM Client Adapter | **P0** | **M** | `Ready` | Architecture, LiteLLM Adapter, Signal Schemas | Items 1, 2, 31, 36, 37, 117-121, 124 |
| [**Story 002**](stories/002_extensible_tool_calling_and_mcp.md) | Financial Tool Engine & News Fetcher | **P0** | **L** | `Backlog` | Function Calling, AST Calc, News Tools, MCP | Items 26-29, 32, 38, 50, 91, 111 |
| [**Story 003**](stories/003_react_reasoning_loop_and_execution_context.md) | Financial ReAct Reasoning Engine & Signals | **P0** | **L** | `Backlog` | ReAct Cycle, Market State Machine, Stop Guards | Items 8, 9, 12, 19, 20, 21, 80, 87 |
| [**Story 004**](stories/004_rag_knowledge_base_and_vector_search.md) | Financial RAG & SEC Filings Vector Search | **P1** | **M** | `Backlog` | SEC Chunking, Embeddings, Top-K Vector Search | Items 24, 40, 43, 99, 100, 101, 104 |
| [**Story 005**](stories/005_filesystem_tools_and_execution_callbacks.md) | Market Filesystem Tools & Alert Approvals | **P1** | **M** | `Backlog` | Price CSVs, Workspace Guard, HITL Approval | Items 26, 33, 39, 86, 110 |
| [**Story 006**](stories/006_context_engineering_sliding_windows_and_compaction.md) | Sliding Windows & News Stream Compactor | **P0** | **L** | `Backlog` | Token Accounting, Deque, Headline Compaction | Items 4, 22, 23, 103, 115 |
| [**Story 007**](stories/007_multiturn_sessions_hitl_and_chromadb.md) | Multiturn Sessions & ChromaDB Ticker Memory | **P1** | **L** | `Backlog` | Market Sessions, Ticker Vector Memory | Items 27, 28, 31, 87, 105, 107 |
| [**Story 008**](stories/008_metacognitive_planning_and_reflection.md) | Multi-Ticker Planning & Signal Reflection | **P1** | **M** | `Backlog` | Research Plan, Catalyst Critique, Replanning | Items 4, 9, 11, 31, 54 |
| [**Story 009**](stories/009_sandboxed_codeact_and_progressive_skills.md) | Sandboxed CodeAct for Quant Indicators | **P0** | **XL** | `Backlog` | CodeAct, Subprocess Sandbox, Pandas/NumPy | Items 72, 73, 84, 85, 98, 111, 116 |
| [**Story 010**](stories/010_multi_agent_collaboration_and_workflows.md) | Multi-Agent Team: News, Quant & Risk Agents | **P1** | **XL** | `Backlog` | Parallel Fan-out, Agent-as-Tool, Handoffs | Items 18, 50, 77-83, 103 |
| [**Story 011**](stories/011_agent_to_agent_a2a_protocol_and_mesh.md) | A2A Financial Protocol & Signals Mesh | **P2** | **L** | `Backlog` | Market Agent Cards, HTTP/SSE Signals Mesh | Items 81, 82, 118, 119, 121, 124 |
| [**Story 012**](stories/012_opentelemetry_tracing_and_gaia_eval.md) | Signal Backtesting Eval & LLM-as-a-Judge | **P0** | **L** | `Backlog` | Telemetry, Earnings Surprise Eval, CI Gates | Items 94-96, 108-113, 118 |

---

## Detailed User Stories

### [Story 001: Project Setup & Financial LLM Client Adapter](stories/001_project_architecture_and_llm_client.md)
- **User Story**:
  - **As a** quantitative research developer,
  - **I want to** establish a clean Python project structure and build a provider-agnostic LLM client with structured signal schemas,
  - **So that** our financial agent can reliably analyze market headlines, extract sentiment signals, and support multiple model providers (OpenAI, Anthropic, Gemini) with strict type safety.
- **Book References**:
  - *Build an AI Agent*: Chapters 1 & 2 ([Notes](bin/build_an_ai_agent_notes.md#chapter-1-what-is-an-ai-agent)).
  - *Effective Python*: Items 1, 2, 31, 36, 37, 117-121, 124 ([Notes](bin/effective_python_v3_notes.md#chapter-1-pythonic-thinking)).
- **Deliverables**: Package layout, `FinancialAgentException` hierarchy, `SentimentSignal` dataclass, `LiteLlmClient` protocol.

---

### [Story 002: Financial Tool Engine & News Fetcher (Finviz / Yahoo)](stories/002_extensible_tool_calling_and_mcp.md)
- **User Story**:
  - **As a** quantitative research developer,
  - **I want to** build a declarative tool calling engine and implement live financial news and market quote fetching tools,
  - **So that** the LLM can query real-time market data, company news feeds, and calculate financial valuation metrics without hallucinations.
- **Book References**:
  - *Build an AI Agent*: Chapter 3 ([Notes](bin/build_an_ai_agent_notes.md#chapter-3-enabling-actions-tool-use)).
  - *Effective Python*: Items 26-29, 32, 38, 50, 91, 111 ([Notes](bin/effective_python_v3_notes.md#chapter-5-functions)).
- **Deliverables**: `@tool` decorator (`functools.wraps`), AST-safe `calculate_metric`, `fetch_ticker_news`, `ToolRegistry`.

---

### [Story 003: Financial ReAct Reasoning Engine & Signal Extraction](stories/003_react_reasoning_loop_and_execution_context.md)
- **User Story**:
  - **As a** quantitative research developer,
  - **I want to** build a ReAct (Thought-Action-Observation) reasoning engine powered by an `ExecutionContext`,
  - **So that** the agent can take a stock ticker, decide which news feeds and valuation metrics to query, synthesize observations, and output a validated trading signal.
- **Book References**:
  - *Build an AI Agent*: Chapter 4 ([Notes](bin/build_an_ai_agent_notes.md#chapter-4-the-react-loop-executioncontext)).
  - *Effective Python*: Items 8, 9, 12, 19, 20, 21, 80, 87 ([Notes](bin/effective_python_v3_notes.md#chapter-1-pythonic-thinking)).
- **Deliverables**: `ExecutionContext` state machine, `FinancialReActAgent.analyze_ticker()`, `match...case` pattern matching on tool calls vs signal.

---

### [Story 004: Financial RAG Knowledge Base & SEC Filings Vector Search](stories/004_rag_knowledge_base_and_vector_search.md)
- **User Story**:
  - **As a** quantitative research developer,
  - **I want to** build a Retrieval-Augmented Generation (RAG) vector index to chunk and search SEC 10-K/10-Q filings and long financial news articles,
  - **So that** the agent can ground its ticker signal on verified financial statements, risk factors, and earnings guidance without hallucinations.
- **Book References**:
  - *Build an AI Agent*: Chapter 5.1-5.3 ([Notes](bin/build_an_ai_agent_notes.md#chapter-5-building-knowledge-bases-with-rag-filesystem-tools)).
  - *Effective Python*: Items 24, 40, 43, 99, 100, 101, 104 ([Notes](bin/effective_python_v3_notes.md#chapter-6-comprehensions-and-generators)).
- **Deliverables**: Generator-based SEC chunker, `FinancialVectorStore` with cosine similarity and `heapq.nlargest` top-K search.

---

### [Story 005: Financial Filesystem Tools & Signal Alert Approvals](stories/005_filesystem_tools_and_execution_callbacks.md)
- **User Story**:
  - **As a** quantitative research developer,
  - **I want to** give the agent safe filesystem tools to inspect market data CSVs/reports and implement human approval callbacks before emitting high-risk trade signals,
  - **So that** local research files are parsed safely while preventing rogue or unverified automated orders from executing.
- **Book References**:
  - *Build an AI Agent*: Chapter 5.4-5.5 ([Notes](bin/build_an_ai_agent_notes.md#chapter-5-building-knowledge-bases-with-rag-filesystem-tools)).
  - *Effective Python*: Items 26, 33, 39, 86, 110 ([Notes](bin/effective_python_v3_notes.md#chapter-5-functions)).
- **Deliverables**: `SafeMarketDataWorkspace` path validator, `read_price_csv`, `TradeAlertGate` human-in-the-loop callback.

---

### [Story 006: Context Engineering, Sliding Windows & News Stream Compactor](stories/006_context_engineering_sliding_windows_and_compaction.md)
- **User Story**:
  - **As a** quantitative research developer,
  - **I want to** implement context engineering with sliding windows and headline compaction,
  - **So that** the agent can digest hundreds of real-time financial news alerts for a ticker without exceeding LLM context windows or incurring runaway token costs.
- **Book References**:
  - *Build an AI Agent*: Chapter 6.1-6.2 ([Notes](bin/build_an_ai_agent_notes.md#chapter-6-adding-memory-to-your-agent)).
  - *Effective Python*: Items 4, 22, 23, 103, 115 ([Notes](bin/effective_python_v3_notes.md#chapter-12-data-structures-and-algorithms)).
- **Deliverables**: `TickerNewsBuffer` using `collections.deque(maxlen=K)`, `FinancialNewsCompactor`, memory leak verification.

---

### [Story 007: Multiturn Market Research Sessions & ChromaDB Ticker Memory](stories/007_multiturn_sessions_hitl_and_chromadb.md)
- **User Story**:
  - **As a** quantitative research developer,
  - **I want to** implement stateful session persistence and an episodic memory store backed by ChromaDB,
  - **So that** analyst queries about a ticker persist across multiturn interactions and past market theses and signals are remembered across separate days.
- **Book References**:
  - *Build an AI Agent*: Chapter 6.3-6.4 ([Notes](bin/build_an_ai_agent_notes.md#chapter-6-adding-memory-to-your-agent)).
  - *Effective Python*: Items 27, 28, 31, 87, 105, 107 ([Notes](bin/effective_python_v3_notes.md#chapter-12-data-structures-and-algorithms)).
- **Deliverables**: `MarketResearchSession` JSON persistence, `TickerMemoryManager` vector episodic recall across trading days.

---

### [Story 008: Metacognitive Financial Task Planning & Signal Reflection](stories/008_metacognitive_planning_and_reflection.md)
- **User Story**:
  - **As a** quantitative research developer,
  - **I want to** equip the agent with structured planning and self-reflection tools,
  - **So that** complex multi-ticker inquiries (e.g. "Assess supply-chain contagion from NVDA earnings on TSM and ASML") are broken into disciplined research subtasks with automated error reflection.
- **Book References**:
  - *Build an AI Agent*: Chapter 7 ([Notes](bin/build_an_ai_agent_notes.md#chapter-7-planning-and-reflection-for-complex-tasks)).
  - *Effective Python*: Items 4, 9, 11, 31, 54 ([Notes](bin/effective_python_v3_notes.md#chapter-1-pythonic-thinking)).
- **Deliverables**: `FinancialResearchPlan` state machine, `reflect_on_signals` critique tool comparing contradictory catalysts.

---

### [Story 009: Sandboxed CodeAct for Quantitative & Technical Analysis](stories/009_sandboxed_codeact_and_progressive_skills.md)
- **User Story**:
  - **As a** quantitative research developer,
  - **I want to** enable the CodeAct paradigm so the agent can write and execute Python code in an isolated sandbox (running Pandas, NumPy, TA-Lib),
  - **So that** the agent can compute custom technical indicators (RSI, Moving Averages, Volatility) and correlate pricing data with news release dates on the fly.
- **Book References**:
  - *Build an AI Agent*: Chapter 8 ([Notes](bin/build_an_ai_agent_notes.md#chapter-8-empowering-agents-with-code-execution-codeact)).
  - *Effective Python*: Items 72, 73, 84, 85, 98, 111, 116 ([Notes](bin/effective_python_v3_notes.md#chapter-9-concurrency-and-parallelism)).
- **Deliverables**: `LocalQuantSandbox` runner with subprocess timeouts, `execute_quant_code` tool.

---

### [Story 010: Multi-Agent Collaboration: News, Quant & Risk Agents](stories/010_multi_agent_collaboration_and_workflows.md)
- **User Story**:
  - **As a** quantitative research developer,
  - **I want to** orchestrate a multi-agent team (News Sentiment Agent, Quantitative Technical Agent, and Risk Manager) using concurrent workflows and agent handoffs,
  - **So that** multiple specialized agents analyze a ticker in parallel and synthesize an institutional-grade investment signal.
- **Book References**:
  - *Build an AI Agent*: Chapter 9.1-9.5 ([Notes](bin/build_an_ai_agent_notes.md#chapter-9-orchestrating-multi-agent-systems)).
  - *Effective Python*: Items 18, 50, 77-83, 103 ([Notes](bin/effective_python_v3_notes.md#chapter-9-concurrency-and-parallelism)).
- **Deliverables**: `run_parallel_ticker_analysis` with `asyncio.TaskGroup`, `make_risk_reviewer_tool` context-isolated sub-agent adapter.

---

### [Story 011: Agent-to-Agent (A2A) Financial Protocol & Signals Mesh](stories/011_agent_to_agent_a2a_protocol_and_mesh.md)
- **User Story**:
  - **As a** quantitative research developer,
  - **I want to** implement the Agent-to-Agent (A2A) protocol with standardized Agent Cards and task endpoints over HTTP,
  - **So that** distributed financial agents (e.g. Remote News Agent in Cloud A, Execution Agent on premises) can discover each other and collaborate over the network.
- **Book References**:
  - *Build an AI Agent*: Chapter 9.6 ([Notes](bin/build_an_ai_agent_notes.md#chapter-9-orchestrating-multi-agent-systems)).
  - *Effective Python*: Items 81, 82, 118, 119, 121, 124 ([Notes](bin/effective_python_v3_notes.md#chapter-14-collaboration)).
- **Deliverables**: `FinancialAgentCard` specification, FastAPI A2A server, distributed market signals mesh client.

---

### [Story 012: Financial Signal Evaluation, Backtesting & LLM-as-a-Judge](stories/012_opentelemetry_tracing_and_gaia_eval.md)
- **User Story**:
  - **As a** quantitative research developer,
  - **I want to** instrument the agent with OpenTelemetry tracing and build an automated evaluation pipeline using historical earnings surprises and LLM-as-a-Judge rubrics in CI/CD,
  - **So that** we can quantitatively measure ticker signal precision, monitor token costs per ticker, and prevent performance regressions.
- **Book References**:
  - *Build an AI Agent*: Chapter 10, 1.4, 2.4 ([Notes](bin/build_an_ai_agent_notes.md#chapter-10-evaluating-agents)).
  - *Effective Python*: Items 94-96, 108-113, 118 ([Notes](bin/effective_python_v3_notes.md#chapter-13-testing-and-debugging)).
- **Deliverables**: `FinancialAgentTracer` OpenTelemetry spans, `FinancialSignalJudge`, CI regression test suite.
