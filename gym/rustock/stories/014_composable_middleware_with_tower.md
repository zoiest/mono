# Story 014: Composable Middleware Pipeline with Tower

## User Story
**As a** backend engineer,
**I want to** apply cross-cutting concerns (request tracing, timeouts, panic catching, and CORS headers) using composable Tower layers,
**So that** business handlers remain focused while requests stay observable and resilient.

---

## 📖 Book Alignment
* **Reference:** *The Rust Programming Language* (TRPL — [doc.rust-lang.org/book](https://doc.rust-lang.org/book/))
* **Chapters:**
  - Chapter 9: *Error Handling*
    - 9.1 *Unrecoverable Errors with `panic!`* (and `catch_unwind` at service boundaries)
  - Chapter 10: *Generic Types, Traits, and Lifetimes*
    - 10.2 *Traits: Defining Shared Behavior* (`tower::Service` and `tower::Layer`)
  - Chapter 13: *Functional Language Features: Iterators and Closures*
    - 13.1 *Closures* (`axum::middleware::from_fn`)

---

## 🎯 What You Will Learn
1. How `tower::Service` and `tower::Layer` model composable async middleware as wrapped types.
2. Applying `tower-http` middleware layers: `TraceLayer`, `CorsLayer`, `TimeoutLayer`, and `CatchPanicLayer`.
3. Writing a custom middleware function with `axum::middleware::from_fn` to attach request IDs or measure latency.
4. Understanding layer ordering (outermost vs innermost execution order).

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Add `tower` and `tower-http` to `Cargo.toml`
```toml
tower = "0.5"
tower-http = { version = "0.6", features = ["trace", "cors", "timeout", "catch-panic"] }
```

### 2. Compose the Middleware Stack
In `src/server/middleware.rs`:
```rust
use std::time::Duration;

use axum::{
    extract::Request,
    middleware::{self, Next},
    response::Response,
    Router,
};
use tower_http::{
    catch_panic::CatchPanicLayer,
    cors::{Any, CorsLayer},
    timeout::TimeoutLayer,
    trace::TraceLayer,
};

pub fn apply_middleware(router: Router) -> Router {
    let cors = CorsLayer::new()
        .allow_origin(Any)
        .allow_methods(Any)
        .allow_headers(Any);

    router
        .layer(middleware::from_fn(request_timing))
        .layer(TimeoutLayer::new(Duration::from_secs(10)))
        .layer(CatchPanicLayer::new())
        .layer(cors)
        .layer(TraceLayer::new_for_http())
}

async fn request_timing(req: Request, next: Next) -> Response {
    let start = std::time::Instant::now();
    let method = req.method().clone();
    let uri = req.uri().clone();

    let mut response = next.run(req).await;
    let elapsed_ms = start.elapsed().as_millis();

    response.headers_mut().insert(
        "x-response-time-ms",
        elapsed_ms.to_string().parse().unwrap(),
    );
    tracing::debug!(%method, %uri, status = %response.status(), elapsed_ms, "handled request");
    response
}
```

---

## ✅ Acceptance Criteria
- [ ] `TraceLayer`, `CorsLayer`, `TimeoutLayer`, and `CatchPanicLayer` wrap the Axum router.
- [ ] Custom `request_timing` middleware adds `x-response-time-ms` to HTTP responses.
- [ ] A deliberate panic inside a test route is caught by `CatchPanicLayer` (returning HTTP 500) without crashing the server.
- [ ] Integration tests verify CORS headers and timing headers on responses.
