# rustock: Multi-Provider Stock Data Web Application & Rust Learning Project

Welcome to the **`rustock`** project (located in `gym/gostock`)! This project is an end-to-end practical journey to master the **Rust programming language** and industry best practices by using ***The Rust Programming Language*** (Steve Klabnik & Carol Nichols — [doc.rust-lang.org/book](https://doc.rust-lang.org/book/)) as the primary reference.

---

## 📖 Project Overview

`rustock` is a modular, high-performance financial data aggregator and web dashboard written in Rust. It fetches, standardizes, and caches real-time and historical stock data from multiple providers (**Yahoo Finance**, **Finviz**, and local test mocks).

- **Cargo Package**: `rustock` (`edition = "2024"`)

### Key Features
- **Multi-Source Ingestion**: Pluggable `StockProvider` trait architecture with automatic failover via `CompositeProvider`.
- **Fearless Async Concurrency**: `tokio` tasks, `JoinSet`, `Semaphore` concurrency bounds, and `mpsc` channels with compile-time data-race freedom (`Send` + `Sync`).
- **Thread-Safe Caching**: Generic `TtlCache<K, V>` backed by `std::sync::RwLock` and `Arc` to minimize redundant network traffic.
- **Observability**: Structured, span-aware logging and diagnostics using `tracing` and `tracing-subscriber`.
- **Production Async HTTP Server**: REST API powered by `axum`, `tokio`, and composable `tower` / `tower-http` middleware layers.
- **Embedded Web UI**: Compile-time type-safe HTML rendering via `askama` with single-binary static asset embedding via `rust-embed`.
- **Real-Time Price Ticker**: Live stock price updates pushed to the browser using **Server-Sent Events (SSE)** over `tokio::sync::broadcast`.
- **Production Ready**: 12-factor configuration, graceful `SIGINT`/`SIGTERM` shutdown, Kubernetes health probes (`/healthz`, `/readyz`), lock-free `AtomicU64` metrics, and minimal `musl` + `distroless` Docker builds.

---

## 📁 Repository Layout

The project follows standard Rust Cargo library + multi-binary conventions (and evolves into a Cargo Workspace in Story 022):

```text
.
├── README.md                 # Architecture, TRPL book mapping, and learning roadmap
├── Cargo.toml                # Package manifest, dependencies, and binary targets
├── stories/                  # Step-by-step User Stories (001 - 022)
├── src/
│   ├── lib.rs                # Library crate root exposing public modules
│   ├── bin/
│   │   ├── rustock_cli.rs    # Command-line interface binary (`rustock-cli`)
│   │   └── rustock_server.rs # HTTP web application binary (`rustock-server`)
│   ├── config/               # Multi-source configuration loader (CLI, env, files)
│   ├── domain/               # Domain models, enums, custom Result error types
│   ├── provider/             # StockProvider trait & implementations
│   │   ├── yahoo.rs          # Yahoo Finance async HTTP client
│   │   ├── finviz.rs         # Finviz client/scraper
│   │   ├── mock.rs           # Deterministic mock provider for offline use
│   │   └── composite.rs      # Ordered fallback orchestrator
│   ├── cache/                # Generic thread-safe TTL cache
│   ├── service/              # Aggregator engine & rate-limited worker pool
│   ├── server/               # Axum router, Tower middleware, REST & HTML handlers
│   ├── sse/                  # Server-Sent Events broadcast hub
│   └── export/               # Streaming CSV exporter
├── tests/                    # Integration tests (with wiremock HTTP mocks)
├── benches/                  # Criterion microbenchmarks
├── templates/                # Askama compile-time checked HTML templates
├── web/static/               # CSS, JS, icons (embedded into binary)
└── Dockerfile                # Multi-stage static musl + distroless container build
```

---

## 📚 Primary Reference: *The Rust Programming Language* (TRPL)

Every user story maps directly to chapters in [***The Rust Programming Language***](https://doc.rust-lang.org/book/):

- **Ch 1: Getting Started** — `rustup`, `rustc`, Cargo, `Cargo.toml`, `cargo check` / `build` / `run`
- **Ch 4: Understanding Ownership** — Ownership, borrowing (`&T`, `&mut T`), slices (`&str`, `&[T]`)
- **Ch 5: Using Structs to Structure Related Data** — Structs, `impl` blocks, `&self` methods
- **Ch 6: Enums and Pattern Matching** — Algebraic enums, `Option<T>`, `match`, `if let` / `let else`
- **Ch 7: Packages, Crates, and Modules** — `lib.rs`, `src/bin/`, `pub` visibility, module trees
- **Ch 8: Common Collections** — `Vec<T>`, UTF-8 `String`, `HashMap<K, V>`
- **Ch 9: Error Handling** — `panic!` vs `Result<T, E>`, `?` propagation, custom `Error` types
- **Ch 10: Generic Types, Traits, and Lifetimes** — Generics, `trait` bounds, `Display`, `FromStr`, lifetimes
- **Ch 11: Writing Automated Tests** — `#[cfg(test)]`, `tests/` integration tests, `assert_eq!`, `#[should_panic]`
- **Ch 12: An I/O Project (CLI Program)** — `std::env::args`, `std::fs`, `std::env::var`, `eprintln!`
- **Ch 13: Functional Features: Iterators and Closures** — `move` closures, iterator chains, zero-cost abstractions
- **Ch 14: More About Cargo and Crates.io** — `[profile.release]`, Cargo Workspaces, feature flags
- **Ch 15: Smart Pointers** — `Box<T>`, `Drop` trait cleanup, `Rc<T>` / `Arc<T>`, interior mutability
- **Ch 16: Fearless Concurrency** — Threads, `mpsc` channels, `Mutex<T>` / `RwLock<T>`, `Send` & `Sync`, atomics
- **Ch 17: Async Programming** — `async` / `await`, `Future`, `Stream`, racing & joining futures
- **Ch 18: OOP Features of Rust** — Trait objects (`Arc<dyn StockProvider>`) & dynamic dispatch
- **Ch 19: Patterns and Matching** — Exhaustive destructuring, match guards, `matches!`
- **Ch 20: Advanced Features** — `unsafe` boundaries, advanced traits, Newtype pattern, `macro_rules!` & proc macros
- **Ch 21: Final Project: Multithreaded Web Server** — `TcpListener`, HTTP framing, graceful shutdown & `Drop`

---

## 🗺️ Roadmap & User Stories

The learning journey is divided into 7 sequential phases containing 22 focused user stories. Track your implementation progress in the table below:

### 📊 User Stories Status Table

| Story | Title | Phase | TRPL Reference (*The Rust Programming Language*) | Status |
| :---: | :--- | :---: | :--- | :---: |
| [001](stories/001_project_setup_and_cargo_initialization.md) | Project Setup & Cargo Initialization | Phase 1 | Ch 1 & Ch 7.1–7.2 (Toolchain, Cargo, Crates & Modules) | Done |
| [002](stories/002_domain_models_structs_enums_and_serde.md) | Domain Models, Structs, Enums & Serde | Phase 1 | Ch 5, Ch 6 & Ch 10.2 (Structs, Enums, `match`, Traits) | Done |
| [003](stories/003_multi_source_configuration_loader.md) | Multi-Source Configuration Loader | Phase 1 | Ch 4 & Ch 12 (Ownership, Args, Env Vars, Files, `stderr`) | ⏳ Todo |
| [004](stories/004_provider_trait_and_yahoo_client.md) | Provider Trait & Yahoo Finance Client | Phase 2 | Ch 10.2, Ch 17.1 & Ch 18.2 (Traits, `async`/`await`, `reqwest`) | ⏳ Todo |
| [005](stories/005_idiomatic_error_handling_with_result.md) | Idiomatic Error Handling with `Result` & `?` | Phase 2 | Ch 9 & Ch 19 (`Result`, `?`, `Error` trait, Pattern Matching) | ⏳ Todo |
| [006](stories/006_finviz_provider_and_composite_fallback.md) | Finviz Provider & Composite Fallback Engine | Phase 2 | Ch 10.2, Ch 15.1/15.4 & Ch 18.2 (`Arc<dyn StockProvider>`) | ⏳ Todo |
| [007](stories/007_concurrent_multi_symbol_fetcher.md) | Concurrent Multi-Symbol Fetcher | Phase 3 | Ch 16.1/16.4 & Ch 17.3 (`Send`/`Sync`, `JoinSet`, Threads) | ⏳ Todo |
| [008](stories/008_worker_pool_with_rate_limiting.md) | Worker Pool with Rate Limiting | Phase 3 | Ch 13.1, Ch 16.2 & Ch 17.2 (`mpsc`, `Semaphore`, `select!`) | ⏳ Todo |
| [009](stories/009_thread_safe_in_memory_cache.md) | Thread-Safe In-Memory Cache with TTL | Phase 3 | Ch 8.3, Ch 10.1/10.3 & Ch 16.3 (`HashMap`, Generics, `RwLock`) | ⏳ Todo |
| [010](stories/010_structured_logging_with_tracing.md) | Structured Logging with `tracing` | Phase 4 | Ch 7.4, Ch 12.6 & Ch 14 (Visibility, `stderr`, Crates) | ⏳ Todo |
| [011](stories/011_unit_integration_tests_and_http_mocks.md) | Unit, Integration Tests & HTTP Mocks | Phase 4 | Ch 11 (`#[cfg(test)]`, `tests/`, `wiremock` HTTP Mocks) | ⏳ Todo |
| [012](stories/012_property_fuzz_testing_and_benchmarking.md) | Property/Fuzz Testing & Benchmarking | Phase 4 | Ch 11, Ch 13.2/13.4 & Ch 14.1 (Iterators, `criterion`, Release Profiles) | ⏳ Todo |
| [013](stories/013_rest_api_with_axum_and_tcp_foundations.md) | REST API with Axum & TCP Foundations | Phase 5 | Ch 17 & Ch 21.1–21.2 (`TcpListener`, `axum`, `IntoResponse`) | ⏳ Todo |
| [014](stories/014_composable_middleware_with_tower.md) | Composable Middleware Pipeline with Tower | Phase 5 | Ch 9.1, Ch 10.2 & Ch 13.1 (`tower::Layer`, Closures, Panic Catching) | ⏳ Todo |
| [015](stories/015_server_configuration_and_graceful_shutdown.md) | Server Configuration & Graceful Shutdown | Phase 5 | Ch 15.3 & Ch 21.3 (`Drop` Trait, OS Signals, Draining) | ⏳ Todo |
| [016](stories/016_server_rendered_ui_with_askama.md) | Server-Rendered UI with Askama Templates | Phase 6 | Ch 5, Ch 6 & Ch 10 (Type-Safe Compile-Time HTML Templates) | ⏳ Todo |
| [017](stories/017_single_binary_static_file_embedding.md) | Single-Binary Static File Embedding | Phase 6 | Ch 14 & Ch 20.5 (`include_bytes!`, `rust-embed` Macros) | ⏳ Todo |
| [018](stories/018_real_time_streaming_with_sse.md) | Real-Time Price Streaming with SSE | Phase 6 | Ch 16.2 & Ch 17.4 (`broadcast` Channels, Async `Stream`, SSE) | ⏳ Todo |
| [019](stories/019_historical_data_export_to_csv.md) | Historical Data Export to CSV | Phase 6 | Ch 8, Ch 12 & Ch 13.2 (`std::io::Write`, Iterators, CSV) | ⏳ Todo |
| [020](stories/020_cloud_health_probes_and_metrics.md) | Cloud Health Probes & Runtime Metrics | Phase 7 | Ch 8.3 & Ch 16.3 (`/healthz`, `/readyz`, `AtomicU64`) | ⏳ Todo |
| [021](stories/021_minimal_distroless_dockerization.md) | Minimal Distroless Dockerization | Phase 7 | Ch 14.1 (Release Profiles, Static `musl`, `rustls`, Distroless) | ⏳ Todo |
| [022](stories/022_workspaces_custom_macros_and_unsafe.md) | Cargo Workspaces, Custom Macros & Advanced Rust | Phase 7 | Ch 14.3 & Ch 20 (Workspaces, Newtype, `macro_rules!`, Proc Macros) | ⏳ Todo |

---

## 📚 Book Mapping Matrix

| *The Rust Programming Language* Chapter | Key Techniques Covered | Mapped User Stories |
| :--- | :--- | :--- |
| **Ch 1: Getting Started** | `rustup`, Cargo, `Cargo.toml`, `cargo check/run` | [001](stories/001_project_setup_and_cargo_initialization.md) |
| **Ch 4: Understanding Ownership** | Ownership, borrowing, `&str` vs `String`, slices | [003](stories/003_multi_source_configuration_loader.md) |
| **Ch 5: Structs & Methods** | Structs, `impl`, `&self`, view models | [002](stories/002_domain_models_structs_enums_and_serde.md), [016](stories/016_server_rendered_ui_with_askama.md) |
| **Ch 6: Enums & Pattern Matching** | Algebraic enums, `Option<T>`, `match`, `if let` | [002](stories/002_domain_models_structs_enums_and_serde.md), [016](stories/016_server_rendered_ui_with_askama.md) |
| **Ch 7: Packages, Crates & Modules** | `lib.rs`, `src/bin/`, visibility (`pub`), `use` | [001](stories/001_project_setup_and_cargo_initialization.md), [010](stories/010_structured_logging_with_tracing.md) |
| **Ch 8: Common Collections** | `Vec<T>`, `String`, `HashMap<K, V>` | [009](stories/009_thread_safe_in_memory_cache.md), [019](stories/019_historical_data_export_to_csv.md), [020](stories/020_cloud_health_probes_and_metrics.md) |
| **Ch 9: Error Handling** | `panic!` vs `Result<T, E>`, `?`, custom `Error` | [005](stories/005_idiomatic_error_handling_with_result.md), [014](stories/014_composable_middleware_with_tower.md) |
| **Ch 10: Generics, Traits & Lifetimes** | Generics, traits, `Display`, `FromStr`, lifetimes | [002](stories/002_domain_models_structs_enums_and_serde.md), [004](stories/004_provider_trait_and_yahoo_client.md), [006](stories/006_finviz_provider_and_composite_fallback.md), [009](stories/009_thread_safe_in_memory_cache.md), [014](stories/014_composable_middleware_with_tower.md), [016](stories/016_server_rendered_ui_with_askama.md) |
| **Ch 11: Writing Automated Tests** | `#[cfg(test)]`, `tests/`, HTTP mocks, property tests | [011](stories/011_unit_integration_tests_and_http_mocks.md), [012](stories/012_property_fuzz_testing_and_benchmarking.md) |
| **Ch 12: CLI I/O Project** | CLI args, env vars, files, `stderr` errors | [003](stories/003_multi_source_configuration_loader.md), [010](stories/010_structured_logging_with_tracing.md), [019](stories/019_historical_data_export_to_csv.md) |
| **Ch 13: Iterators & Closures** | `move` closures, iterator pipelines, benchmarks | [008](stories/008_worker_pool_with_rate_limiting.md), [012](stories/012_property_fuzz_testing_and_benchmarking.md), [014](stories/014_composable_middleware_with_tower.md), [019](stories/019_historical_data_export_to_csv.md) |
| **Ch 14: More About Cargo** | Release profiles, workspaces, crates.io ecosystem | [010](stories/010_structured_logging_with_tracing.md), [012](stories/012_property_fuzz_testing_and_benchmarking.md), [017](stories/017_single_binary_static_file_embedding.md), [021](stories/021_minimal_distroless_dockerization.md), [022](stories/022_workspaces_custom_macros_and_unsafe.md) |
| **Ch 15: Smart Pointers** | `Box<T>`, `Drop`, `Arc<T>`, interior mutability | [006](stories/006_finviz_provider_and_composite_fallback.md), [009](stories/009_thread_safe_in_memory_cache.md), [015](stories/015_server_configuration_and_graceful_shutdown.md) |
| **Ch 16: Fearless Concurrency** | Threads, `mpsc`, `RwLock`, `Send`/`Sync`, atomics | [007](stories/007_concurrent_multi_symbol_fetcher.md), [008](stories/008_worker_pool_with_rate_limiting.md), [009](stories/009_thread_safe_in_memory_cache.md), [018](stories/018_real_time_streaming_with_sse.md), [020](stories/020_cloud_health_probes_and_metrics.md) |
| **Ch 17: Async Programming** | `async`/`await`, futures, `JoinSet`, `Stream` | [004](stories/004_provider_trait_and_yahoo_client.md), [007](stories/007_concurrent_multi_symbol_fetcher.md), [008](stories/008_worker_pool_with_rate_limiting.md), [013](stories/013_rest_api_with_axum_and_tcp_foundations.md), [018](stories/018_real_time_streaming_with_sse.md) |
| **Ch 18: OOP Features** | Trait objects (`Arc<dyn StockProvider>`), dispatch | [004](stories/004_provider_trait_and_yahoo_client.md), [006](stories/006_finviz_provider_and_composite_fallback.md) |
| **Ch 19: Patterns & Matching** | Exhaustive `match`, destructuring, `matches!` | [005](stories/005_idiomatic_error_handling_with_result.md) |
| **Ch 20: Advanced Features** | Newtype pattern, `macro_rules!`, proc macros, `unsafe` | [017](stories/017_single_binary_static_file_embedding.md), [022](stories/022_workspaces_custom_macros_and_unsafe.md) |
| **Ch 21: Multithreaded Web Server** | `TcpListener`, HTTP framing, graceful shutdown | [013](stories/013_rest_api_with_axum_and_tcp_foundations.md), [015](stories/015_server_configuration_and_graceful_shutdown.md) |

---

## 🚀 How to Work Through This Project

1. Install the Rust toolchain if needed (`rustup` — see [Story 001](stories/001_project_setup_and_cargo_initialization.md)).
2. Verify the existing starter code from Stories 001 & 002:
   ```bash
   cargo test
   cargo clippy --all-targets
   cargo run --bin rustock-cli
   ```
3. Continue with [Story 003: Multi-Source Configuration Loader](stories/003_multi_source_configuration_loader.md).
4. For each story:
   - Read the corresponding chapter(s) in [*The Rust Programming Language*](https://doc.rust-lang.org/book/).
   - Implement the acceptance criteria in `src/` and `tests/`.
   - Run `cargo fmt --check`, `cargo clippy --all-targets`, and `cargo test`.
   - Mark the acceptance criteria as completed (`[X]`).
