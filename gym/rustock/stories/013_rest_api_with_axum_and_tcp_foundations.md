# Story 013: REST API with Axum & TCP Foundations

## User Story
**As a** client application or web frontend,
**I want** clean RESTful endpoints to query quotes, batch quotes, and historical prices,
**So that** consumers can retrieve JSON data using type-safe HTTP extractors and unified error responses.

---

## 📖 Book Alignment
* **Reference:** *The Rust Programming Language* (TRPL — [doc.rust-lang.org/book](https://doc.rust-lang.org/book/))
* **Chapters:**
  - Chapter 21: *Final Project: Building a Multithreaded Web Server*
    - 21.1 *Building a Single-Threaded Web Server* (`std::net::TcpListener`, HTTP request/response anatomy)
    - 21.2 *Turning Our Single-Threaded Server into a Multithreaded Server* (`ThreadPool`)
  - Chapter 17: *Fundamentals of Asynchronous Programming: Async, Await, Futures, and Streams*

---

## 🎯 What You Will Learn
1. How HTTP servers work under the hood in Rust (`TcpListener`, reading request lines, writing `HTTP/1.1 200 OK` responses — TRPL Ch 21).
2. Building a production REST API on top of `axum` and `tokio`.
3. Using typed Axum extractors: `Path<String>`, `Query<HistoryParams>`, `State<AppState>`, and `Json<T>`.
4. Implementing `axum::response::IntoResponse` on `StockError` so domain errors automatically map to proper HTTP status codes (`404`, `429`, `502`, `504`).

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Warm-Up: Raw `TcpListener` Echo/Health Prototype (TRPL Ch 21)
Before wiring Axum, build a small `scratch` or unit example using `std::net::TcpListener` following TRPL Ch 21.1 to inspect raw HTTP headers and status lines firsthand.

### 2. Add `axum` to `Cargo.toml` and Build the Router
In `src/server/mod.rs`:
```rust
use std::sync::Arc;

use axum::{
    extract::{Path, Query, State},
    http::StatusCode,
    response::{IntoResponse, Response},
    routing::get,
    Json, Router,
};
use serde::Deserialize;

use crate::domain::{Quote, StockError};
use crate::service::StockService;

#[derive(Clone)]
pub struct AppState {
    pub service: Arc<StockService>,
}

#[derive(Deserialize)]
pub struct BatchQuery {
    pub symbols: String,
}

#[derive(Deserialize)]
pub struct HistoryQuery {
    #[serde(default = "default_range")]
    pub range: String,
    #[serde(default = "default_interval")]
    pub interval: String,
}

fn default_range() -> String { "1mo".to_string() }
fn default_interval() -> String { "1d".to_string() }

impl IntoResponse for StockError {
    fn into_response(self) -> Response {
        let status = match &self {
            StockError::SymbolNotFound { .. } => StatusCode::NOT_FOUND,
            StockError::RateLimited { .. } => StatusCode::TOO_MANY_REQUESTS,
            StockError::NetworkTimeout { .. } => StatusCode::GATEWAY_TIMEOUT,
            _ => StatusCode::BAD_GATEWAY,
        };
        (status, Json(serde_json::json!({ "error": self.to_string() }))).into_response()
    }
}

pub fn router(state: AppState) -> Router {
    Router::new()
        .route("/api/v1/stocks/{symbol}", get(get_quote))
        .route("/api/v1/stocks", get(get_batch_quotes))
        .route("/api/v1/stocks/{symbol}/history", get(get_history))
        .with_state(state)
}
```

---

## ✅ Acceptance Criteria
- [ ] `GET /api/v1/stocks/{symbol}` returns a JSON `Quote`.
- [ ] `GET /api/v1/stocks?symbols=AAPL,MSFT,GOOG` returns concurrent batch quotes.
- [ ] `GET /api/v1/stocks/{symbol}/history?range=1mo&interval=1d` returns historical OHLCV bars.
- [ ] `IntoResponse` maps `StockError` variants cleanly to semantic HTTP status codes.
