# Story 015: Server Configuration & Graceful Shutdown

## User Story
**As a** system administrator,
**I want** the HTTP server to listen for OS signals (`SIGINT`, `SIGTERM`) and drain in-flight requests and background workers cleanly,
**So that** rolling updates and shutdowns never drop active connections or corrupt state.

---

## 📖 Book Alignment
* **Reference:** *The Rust Programming Language* (TRPL — [doc.rust-lang.org/book](https://doc.rust-lang.org/book/))
* **Chapters:**
  - Chapter 15: *Smart Pointers*
    - 15.3 *Running Code on Cleanup with the `Drop` Trait*
  - Chapter 21: *Final Project: Building a Multithreaded Web Server*
    - 21.3 *Graceful Shutdown and Cleanup* (Implementing `Drop` on worker pools / coordinators)

---

## 🎯 What You Will Learn
1. Listening for `Ctrl+C` (`SIGINT`) and `SIGTERM` asynchronously with `tokio::signal`.
2. Wiring `axum::serve(listener, app).with_graceful_shutdown(shutdown_signal())`.
3. Using RAII and the `Drop` trait (TRPL Ch 15.3 & 21.3) plus `tokio_util::sync::CancellationToken` (or `watch` channel) to stop background tasks cleanly.
4. Separating binary startup (`src/bin/rustock_server.rs`) cleanly from library modules.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Implement `shutdown_signal()` and `rustock-server`
In `src/bin/rustock_server.rs`:
```rust
use std::net::SocketAddr;
use std::sync::Arc;

use tokio::net::TcpListener;
use tokio::signal;
use tokio::sync::watch;

use rustock::config::{AppConfig, CliOverrides};
use rustock::provider::yahoo::YahooProvider;
use rustock::server::{apply_middleware, router, AppState};
use rustock::service::StockService;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let cfg = AppConfig::load(CliOverrides::default())?;
    let addr = SocketAddr::from(([0, 0, 0, 0], cfg.port));

    let provider = Arc::new(YahooProvider::new(cfg.request_timeout)?);
    let service = Arc::new(StockService::new(provider));

    let (shutdown_tx, shutdown_rx) = watch::channel(false);
    // Pass `shutdown_rx` to background tasks (cache cleanup, SSE ticker)

    let app = apply_middleware(router(AppState { service }));
    let listener = TcpListener::bind(addr).await?;
    tracing::info!(%addr, "rustock-server listening");

    axum::serve(listener, app)
        .with_graceful_shutdown(shutdown_signal(shutdown_tx))
        .await?;

    drop(shutdown_rx);
    tracing::info!("server shutdown complete");
    Ok(())
}

async fn shutdown_signal(tx: watch::Sender<bool>) {
    let ctrl_c = async {
        signal::ctrl_c().await.expect("install Ctrl+C handler");
    };

    #[cfg(unix)]
    let terminate = async {
        signal::unix::signal(signal::unix::SignalKind::terminate())
            .expect("install SIGTERM handler")
            .recv()
            .await;
    };

    #[cfg(not(unix))]
    let terminate = std::future::pending::<()>();

    tokio::select! {
        _ = ctrl_c => {},
        _ = terminate => {},
    }

    tracing::info!("shutdown signal received, draining connections");
    let _ = tx.send(true);
}
```

---

## ✅ Acceptance Criteria
- [ ] `src/bin/rustock_server.rs` boots the Axum server on the configured port.
- [ ] `SIGINT` (Ctrl+C) and `SIGTERM` trigger graceful connection draining via `with_graceful_shutdown`.
- [ ] Background tasks receive the shutdown signal and finish cleanly before process exit.
- [ ] A `Drop` guard cleans up any background worker handles (aligned with TRPL Ch 21.3).
