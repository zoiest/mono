# Story 010: Structured Logging with Tracing

## User Story
**As a** DevOps engineer and backend developer,
**I want** the application to emit structured logs and spans with contextual fields using `tracing`,
**So that** logs can be read cleanly in local terminals or parsed as JSON by observability platforms (Datadog, Grafana Loki).

---

## 📖 Book Alignment
* **Reference:** *The Rust Programming Language* (TRPL — [doc.rust-lang.org/book](https://doc.rust-lang.org/book/))
* **Chapters:**
  - Chapter 7: *Managing Growing Projects with Packages, Crates, and Modules*
    - 7.4 *Bringing Paths into Scope with the `use` Keyword*
  - Chapter 12: *An I/O Project: Building a Command Line Program*
    - 12.6 *Writing Error Messages to Standard Error Instead of Standard Output*
  - Chapter 14: *More About Cargo and Crates.io*
    - Feature flags and optional crate configuration

---

## 🎯 What You Will Learn
1. Instrumenting async and sync functions with `#[tracing::instrument]`.
2. Emitting structured fields (`symbol = %sym`, `provider = %p`, `latency_ms = ...`) via `tracing::info!`, `warn!`, and `error!`.
3. Configuring `tracing-subscriber` with `EnvFilter` (`RUST_LOG=rustock=debug,info`) and switching between human-readable vs JSON formatters.
4. Directing diagnostic logs to `stderr` so `stdout` stays clean for CLI JSON/CSV piping.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Add Dependencies to `Cargo.toml`
```toml
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter", "json"] }
```

### 2. Initialize the Subscriber
In `src/telemetry.rs`:
```rust
use tracing_subscriber::{fmt, EnvFilter};

pub fn init_tracing(json_output: bool) {
    let filter = EnvFilter::try_from_default_env()
        .unwrap_or_else(|_| EnvFilter::new("rustock=info,warn"));

    if json_output {
        fmt()
            .with_env_filter(filter)
            .with_writer(std::io::stderr)
            .json()
            .init();
    } else {
        fmt()
            .with_env_filter(filter)
            .with_writer(std::io::stderr)
            .compact()
            .init();
    }
}
```

### 3. Instrument Provider & Service Methods
```rust
#[tracing::instrument(skip(self), fields(provider = %self.name()))]
async fn fetch_quote(&self, symbol: &str) -> Result<Quote, StockError> {
    let start = std::time::Instant::now();
    // ... fetch logic ...
    tracing::info!(symbol = %symbol, elapsed_ms = start.elapsed().as_millis(), "fetched quote");
    Ok(quote)
}
```

---

## ✅ Acceptance Criteria
- [ ] `init_tracing` supports both compact terminal output and structured JSON output.
- [ ] `RUST_LOG` controls log verbosity dynamically without recompiling.
- [ ] Logs write to `stderr` (keeping `stdout` clean for CLI data output).
- [ ] Key operations emit structured spans with `symbol`, `provider`, and latency fields.
