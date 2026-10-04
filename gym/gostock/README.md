# gostock: Multi-Provider Stock Data Web Application & Learning Project

Welcome to the **`gostock`** project! This project is designed as an end-to-end practical journey to master the Go programming language and industry best practices by following the techniques in **_Go in Practice, Second Edition_** by Nathan Kozyra.

---

## 📖 Project Overview

`gostock` is a modular, high-performance financial data aggregator and web dashboard. It fetches, standardizes, and caches real-time and historical stock data from multiple providers (**Yahoo Finance**, **Finviz**, and local test mocks).

- **Go Module**: `github.com/zoiest/mono/gym/gostock`

### Key Features
- **Multi-Source Ingestion**: Pluggable provider architecture with automatic failover between data sources.
- **High-Performance Concurrency**: Goroutines, channels, and worker pools for bounded, concurrent stock queries.
- **Thread-Safe Caching**: Generic in-memory cache with TTL to minimize redundant network traffic.
- **Observability**: Standard structured logging using Go's `log/slog`.
- **Modern HTTP Server**: REST API powered by Go 1.22+ enhanced `http.ServeMux` with pattern matching and path parameters.
- **Embedded Web UI**: Server-rendered dashboard via `html/template` with single-binary asset embedding via `embed.FS`.
- **Real-Time Price Ticker**: Live stock price updates delivered to the browser using **Server-Sent Events (SSE)**.
- **Production Ready**: 12-factor configuration, graceful shutdown, health probes (`/healthz`, `/readyz`), and minimal scratch/distroless Docker builds.

---

## 📁 Repository Layout

The project follows standard Go package layout conventions:

```
.
├── README.md                 # Overall architecture, book mapping, and guide
├── stories/                  # Step-by-step User Stories (001 - 022)
├── writings/                 # Org-mode notes & HTML summaries (synced with Drive, gitignored)
│   ├── index.org             # Master Org-Roam index and MOC
│   └── ch*.org               # Chapter summaries, recipes, and idioms
├── cmd/
│   ├── gostock-cli/          # Command-line interface entrypoint
│   └── gostock-server/       # HTTP web application entrypoint
├── internal/                 # Private application logic (enforced by Go compiler)
│   ├── config/               # Configuration management (flags, env, config files)
│   ├── domain/               # Domain models, enums, custom errors
│   ├── provider/             # Provider implementations
│   │   ├── yahoo/            # Yahoo Finance client
│   │   ├── finviz/           # Finviz client/scraper
│   │   └── mock/             # Test fixtures and mock provider
│   ├── cache/                # Thread-safe in-memory generic cache
│   ├── service/              # Aggregator engine & worker pool
│   ├── server/               # HTTP router, middleware, REST handlers
│   └── sse/                  # Server-Sent Events broker
├── web/                      # Frontend assets
│   ├── templates/            # HTML templates (layouts, views, partials)
│   └── static/               # CSS, JS, icons (embedded into binary)
├── Dockerfile                # Multi-stage container build
├── go.mod
└── go.sum
```

---

## 📑 Org-Mode Book Summaries & Quick References

Comprehensive, high-yield summaries for each chapter of *Go in Practice (Second Edition)* are formatted as Org-mode notes compatible with **Org-Roam** (including stable `:ID:` properties, tags, and cross-links):

- **Master Index & Cheat Sheet**: [writings/index.org](writings/index.org)
- [Ch 01: Getting Started with Go](writings/ch01_getting_started.org) — Toolchain, environment variables, modules
- [Ch 02: Building CLI Applications](writings/ch02_cli_applications.org) — Flags, enums (`iota`), config hierarchy, OS signals
- [Ch 03: Structs, Interfaces & Generics](writings/ch03_structs_interfaces_generics.org) — Struct tags, JSON, composition, generics
- [Ch 04: Handling Errors & Panics](writings/ch04_error_handling_and_panics.org) — Sentinel errors, `%w` wrapping, `errors.Is`/`As`, `defer`/`recover`
- [Ch 05: Concurrency in Go](writings/ch05_concurrency_in_go.org) — Goroutines, `sync.WaitGroup`, `sync.RWMutex`, channels, worker pools
- [Ch 06: Testing, Logging & Benchmarking](writings/ch06_testing_logging_benchmarking.org) — `log/slog`, table-driven tests, `httptest`, fuzzing, benchmarks
- [Ch 07: File Access & Networking](writings/ch07_file_access_and_networking.org) — `bufio`, TCP/UDP, Server-Sent Events (SSE)
- [Ch 08: Building an HTTP Server](writings/ch08_building_http_server.org) — Go 1.22+ `ServeMux`, path values, composable middleware
- [Ch 09: HTML & Email Template Patterns](writings/ch09_html_and_email_templates.org) — `html/template`, `FuncMap`, layouts, XSS safety
- [Ch 10: Sending and Receiving Data](writings/ch10_sending_receiving_data.org) — `embed.FS`, static assets, streaming CSV exports
- [Ch 11: Working with External Services](writings/ch11_external_services_rest_grpc.org) — `http.Client` pooling, timeouts, backoff retries, gRPC
- [Ch 12: Cloud-Ready Applications](writings/ch12_cloud_and_microservices.org) — Health probes, runtime metrics, distroless Docker
- [Ch 13: Reflection and Advanced Go](writings/ch13_reflection_and_advanced_go.org) — Struct tags, Laws of Reflection, `go:generate`

---

## 🗺️ Roadmap & User Stories

The learning journey is divided into 7 sequential phases containing 22 focused user stories. Track your implementation progress in the table below:

### 📊 User Stories Status Table

| Story | Title | Phase | Book Technique (*Go in Practice 2nd Ed*) | Status |
| :---: | :--- | :---: | :--- | :---: |
| [001](stories/001_project_setup_and_module_initialization.md) | Project Setup & Module Initialization | Phase 1 | Ch 1 (Toolchain, Workspace, Modules) | Done |
| [002](stories/002_domain_models_struct_tags_and_enums.md) | Domain Models, Struct Tags & Enums | Phase 1 | Ch 2.1 & 3.1 (Structs, Enums with iota, JSON) | ⏳ Todo |
| [003](stories/003_multi_source_configuration_loader.md) | Multi-Source Configuration Loader | Phase 1 | Ch 2.1 & 2.2 (Flags, Env Vars, Config Files) | ⏳ Todo |
| [004](stories/004_provider_interface_and_yahoo_client.md) | Provider Interface & Yahoo Finance Client | Phase 2 | Ch 3.3 & 11.1 (Interfaces, http.Client, JSON) | ⏳ Todo |
| [005](stories/005_idiomatic_error_handling_and_wrapping.md) | Idiomatic Error Handling & Error Wrapping | Phase 2 | Ch 4.1 & 4.2 (Sentinel Errors, %w, errors.Is/As) | ⏳ Todo |
| [006](stories/006_finviz_provider_and_composite_fallback.md) | Finviz Provider & Composite Fallback Engine | Phase 2 | Ch 3.3 & 11.2 (Composition, Fault Tolerance) | ⏳ Todo |
| [007](stories/007_concurrent_multi_symbol_fetcher.md) | Concurrent Multi-Symbol Fetcher | Phase 3 | Ch 5.1 & 5.2 (Goroutines, sync.WaitGroup) | ⏳ Todo |
| [008](stories/008_worker_pool_with_rate_limiting.md) | Worker Pool with Rate Limiting | Phase 3 | Ch 5.3 (Channels, Worker Pools, Timeouts) | ⏳ Todo |
| [009](stories/009_thread_safe_in_memory_cache.md) | Thread-Safe In-Memory Cache with TTL | Phase 3 | Ch 3.4 & 5.2 (sync.RWMutex, Generics) | ⏳ Todo |
| [010](stories/010_structured_logging_with_slog.md) | Structured Logging with slog | Phase 4 | Ch 6.1 & 6.2 (log/slog, Handlers, Attributes) | ⏳ Todo |
| [011](stories/011_table_driven_testing_and_http_mocks.md) | Table-Driven Testing & HTTP Mocks | Phase 4 | Ch 6.3 (Table Tests, httptest.Server, Coverage) | ⏳ Todo |
| [012](stories/012_fuzz_testing_and_benchmarking.md) | Fuzz Testing & Allocation Benchmarking | Phase 4 | Ch 6.3 & 6.4 (testing.F, testing.B, Allocs) | ⏳ Todo |
| [013](stories/013_rest_api_with_enhanced_servemux.md) | REST API with Go 1.22+ Enhanced ServeMux | Phase 5 | Ch 8.1 & 11.4 (Routing Verbs, Path Values) | ⏳ Todo |
| [014](stories/014_composable_middleware_pipeline.md) | Composable Middleware Pipeline | Phase 5 | Ch 4.3 & 8.2 (Middlewares, Panic Recovery, CORS) | ⏳ Todo |
| [015](stories/015_server_configuration_and_graceful_shutdown.md) | Server Configuration & Graceful Shutdown | Phase 5 | Ch 2.3 & 8.2 (OS Signals, Server Timeouts) | ⏳ Todo |
| [016](stories/016_server_rendered_ui_with_html_template.md) | Server-Rendered UI with html/template | Phase 6 | Ch 9.1 (html/template, Layouts, FuncMap) | ⏳ Todo |
| [017](stories/017_single_binary_static_file_embedding.md) | Single-Binary Static File Embedding | Phase 6 | Ch 10.1 (embed.FS, Embedded Static Assets) | ⏳ Todo |
| [018](stories/018_real_time_streaming_with_sse.md) | Real-Time Price Streaming with SSE | Phase 6 | Ch 5.3 & 7.4 (Server-Sent Events, http.Flusher) | ⏳ Todo |
| [019](stories/019_historical_data_export_to_csv.md) | Historical Data Export to CSV | Phase 6 | Ch 7.1 & 10.2 (CSV Streams, io.Writer) | ⏳ Todo |
| [020](stories/020_cloud_health_probes_and_metrics.md) | Cloud Health Probes & Runtime Metrics | Phase 7 | Ch 12.4 (/healthz, /readyz, runtime.MemStats) | ⏳ Todo |
| [021](stories/021_minimal_distroless_dockerization.md) | Minimal Distroless Dockerization | Phase 7 | Ch 12.1 & 12.5 (Multi-stage Docker, Static binary) | ⏳ Todo |
| [022](stories/022_struct_tag_validation_and_codegen.md) | Dynamic Struct Tag Validation & Codegen | Phase 7 | Ch 13.1, 13.2 & 13.3 (Reflection, go:generate) | ⏳ Todo |

### Phase 1: Environment, CLI Foundation & Domain Modeling
* [001: Project Setup & Module Initialization](stories/001_project_setup_and_module_initialization.md) *(Ch 1: Toolchain, Modules, Workspace)*
* [002: Domain Models, Struct Tags & Enums](stories/002_domain_models_struct_tags_and_enums.md) *(Ch 2.1 & 3.1: Structs, Enums with iota, JSON serialization)*
* [003: Multi-Source Configuration Loader](stories/003_multi_source_configuration_loader.md) *(Ch 2.1 & 2.2: Flags, Env vars, Config files)*

### Phase 2: External API Ingestion & Robust Error Handling
* [004: Provider Interface & Yahoo Finance Client](stories/004_provider_interface_and_yahoo_client.md) *(Ch 3.3 & 11.1: Interfaces, http.Client, JSON mapping)*
* [005: Idiomatic Error Handling & Error Wrapping](stories/005_idiomatic_error_handling_and_wrapping.md) *(Ch 4.1 & 4.2: Sentinel errors, %w wrapping, errors.Is/As)*
* [006: Finviz Provider & Composite Fallback Engine](stories/006_finviz_provider_and_composite_fallback.md) *(Ch 3.3 & 11.2: Composition, Fault tolerance, Failover)*

### Phase 3: High-Performance Concurrency & In-Memory Caching
* [007: Concurrent Multi-Symbol Fetcher](stories/007_concurrent_multi_symbol_fetcher.md) *(Ch 5.1 & 5.2: Goroutines, sync.WaitGroup, Race conditions)*
* [008: Worker Pool with Rate Limiting](stories/008_worker_pool_with_rate_limiting.md) *(Ch 5.3: Channels, Buffers, Worker pools, Timeouts)*
* [009: Thread-Safe In-Memory Cache with TTL](stories/009_thread_safe_in_memory_cache.md) *(Ch 3.4 & 5.2: sync.RWMutex, Generics, Cache eviction)*

### Phase 4: Observability, Testing & Benchmarking
* [010: Structured Logging with slog](stories/010_structured_logging_with_slog.md) *(Ch 6.1 & 6.2: log/slog, Handlers, Structured context)*
* [011: Table-Driven Testing & HTTP Mocks](stories/011_table_driven_testing_and_http_mocks.md) *(Ch 6.3: Table-driven tests, httptest.Server, Code coverage)*
* [012: Fuzz Testing & Allocation Benchmarking](stories/012_fuzz_testing_and_benchmarking.md) *(Ch 6.3 & 6.4: testing.F, testing.B, Zero-allocation tuning)*

### Phase 5: Production HTTP Web Server & REST API
* [013: REST API with Go 1.22+ Enhanced ServeMux](stories/013_rest_api_with_enhanced_servemux.md) *(Ch 8.1 & 11.4: Routing with verbs and path parameters)*
* [014: Composable Middleware Pipeline](stories/014_composable_middleware_pipeline.md) *(Ch 4.3 & 8.2: Panic recovery, Request logging, CORS)*
* [015: Server Configuration & Graceful Shutdown](stories/015_server_configuration_and_graceful_shutdown.md) *(Ch 2.3 & 8.2: OS signals, Context cancellation, Timeouts)*

### Phase 6: Web Dashboard, Static Embedding & Real-Time Streaming
* [016: Server-Rendered UI with html/template](stories/016_server_rendered_ui_with_html_template.md) *(Ch 9.1: Template inheritance, FuncMap, XSS protection)*
* [017: Single-Binary Static File Embedding](stories/017_single_binary_static_file_embedding.md) *(Ch 10.1: embed.FS, Embedded assets, Standalone binary)*
* [018: Real-Time Price Streaming with SSE](stories/018_real_time_streaming_with_sse.md) *(Ch 5.3 & 7.4: Server-Sent Events, http.Flusher, Channel broadcasting)*
* [019: Historical Data Export to CSV](stories/019_historical_data_export_to_csv.md) *(Ch 7.1 & 10.2: File streams, encoding/csv, io.Writer)*

### Phase 7: Cloud-Ready Packaging & Advanced Go Patterns
* [020: Cloud Health Probes & Runtime Metrics](stories/020_cloud_health_probes_and_metrics.md) *(Ch 12.4: /healthz, /readyz, runtime.MemStats)*
* [021: Minimal Distroless Dockerization](stories/021_minimal_distroless_dockerization.md) *(Ch 12.1 & 12.5: Multi-stage Dockerfile, CGO_ENABLED=0)*
* [022: Dynamic Struct Tag Validation & Codegen](stories/022_struct_tag_validation_and_codegen.md) *(Ch 13.1, 13.2 & 13.3: Reflection, Struct tags, go:generate)*

---

## 📚 Book Mapping Matrix

| Book Chapter (*Go in Practice 2nd Ed*) | Key Techniques Covered | Mapped User Stories |
| :--- | :--- | :--- |
| **Chapter 1: Getting Started** | Go toolchain, modules, workspace | [001](stories/001_project_setup_and_module_initialization.md) |
| **Chapter 2: CLI Foundation** | Flags, Enums, Config hierarchy, Server lifecycle | [002](stories/002_domain_models_struct_tags_and_enums.md), [003](stories/003_multi_source_configuration_loader.md), [015](stories/015_server_configuration_and_graceful_shutdown.md) |
| **Chapter 3: Structs & Interfaces** | Struct tags, JSON, Interfaces, Generics | [002](stories/002_domain_models_struct_tags_and_enums.md), [004](stories/004_provider_interface_and_yahoo_client.md), [006](stories/006_finviz_provider_and_composite_fallback.md), [009](stories/009_thread_safe_in_memory_cache.md) |
| **Chapter 4: Error Handling** | Nil checks, Sentinel errors, `%w` wrapping, Panic/Recover | [005](stories/005_idiomatic_error_handling_and_wrapping.md), [014](stories/014_composable_middleware_pipeline.md) |
| **Chapter 5: Concurrency** | CSP, `sync.WaitGroup`, `sync.RWMutex`, Channels, Worker pool | [007](stories/007_concurrent_multi_symbol_fetcher.md), [008](stories/008_worker_pool_with_rate_limiting.md), [009](stories/009_thread_safe_in_memory_cache.md), [018](stories/018_real_time_streaming_with_sse.md) |
| **Chapter 6: Testing & Logging** | Clean code, `slog`, Table tests, Fuzzing, Benchmarks | [010](stories/010_structured_logging_with_slog.md), [011](stories/011_table_driven_testing_and_http_mocks.md), [012](stories/012_fuzz_testing_and_benchmarking.md) |
| **Chapter 7: Files & Networking** | CSV files, WebSockets / Server-Sent Events | [018](stories/018_real_time_streaming_with_sse.md), [019](stories/019_historical_data_export_to_csv.md) |
| **Chapter 8: HTTP Server** | Routing with verbs/path values, Middleware, Handlers | [013](stories/013_rest_api_with_enhanced_servemux.md), [014](stories/014_composable_middleware_pipeline.md), [015](stories/015_server_configuration_and_graceful_shutdown.md) |
| **Chapter 9: HTML Templates** | `html/template`, Layouts, Partials, FuncMap | [016](stories/016_server_rendered_ui_with_html_template.md) |
| **Chapter 10: Static Data & Forms** | `embed.FS`, Asset serving, Streaming responses | [017](stories/017_single_binary_static_file_embedding.md), [019](stories/019_historical_data_export_to_csv.md) |
| **Chapter 11: External Services** | `http.Client` timeouts, REST clients, Fault handling | [004](stories/004_provider_interface_and_yahoo_client.md), [006](stories/006_finviz_provider_and_composite_fallback.md), [013](stories/013_rest_api_with_enhanced_servemux.md) |
| **Chapter 12: Cloud & Microservices** | Health checks, Runtime stats, Multi-stage Docker | [020](stories/020_cloud_health_probes_and_metrics.md), [021](stories/021_minimal_distroless_dockerization.md) |
| **Chapter 13: Reflection & Codegen** | Custom tags, Reflection inspection, `go:generate` | [022](stories/022_struct_tag_validation_and_codegen.md) |

---

## 🚀 How to Work Through This Project

1. Start with [stories/001_project_setup_and_module_initialization.md](stories/001_project_setup_and_module_initialization.md).
2. For each story:
   - Read the corresponding section in [downloads/Go_in_Practice_Second_Edition.pdf](downloads/Go_in_Practice_Second_Edition.pdf).
   - Implement the acceptance criteria in your code.
   - Run tests and linters: `go test -v ./...` and `go vet ./...`.
   - Mark the acceptance criteria as completed.
