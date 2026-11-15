# Story 018: Real-Time Streaming with Server-Sent Events (SSE)

## User Story
**As a** trader watching volatile stock prices,
**I want** stock prices on the dashboard to stream automatically in real-time over HTTP,
**So that** price updates appear live in the browser without polling or manual refreshes.

---

## 📖 Book Alignment
* **Reference:** *The Rust Programming Language* (TRPL — [doc.rust-lang.org/book](https://doc.rust-lang.org/book/))
* **Chapters:**
  - Chapter 16: *Fearless Concurrency*
    - 16.2 *Using Message Passing to Transfer Data Between Threads*
  - Chapter 17: *Fundamentals of Asynchronous Programming: Async, Await, Futures, and Streams*
    - 17.4 *Streams: Futures in Sequence* (`tokio_stream`, `Stream` trait)

---

## 🎯 What You Will Learn
1. Fan-out broadcasting to multiple connected browser clients using `tokio::sync::broadcast`.
2. Turning a broadcast receiver into an async `Stream` (`BroadcastStream`) for `axum::response::sse::{Sse, Event}`.
3. Configuring SSE keep-alive heartbeats to keep proxies and browsers connected.
4. Automatic cleanup when a client disconnects (the stream and its receiver are dropped automatically!).

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Add `tokio-stream` to `Cargo.toml`
```toml
tokio-stream = { version = "0.1", features = ["sync"] }
```

### 2. Build the SSE Broadcaster & Handler
In `src/sse/mod.rs`:
```rust
use std::convert::Infallible;
use std::time::Duration;

use axum::response::sse::{Event, KeepAlive, Sse};
use tokio::sync::broadcast;
use tokio_stream::wrappers::BroadcastStream;
use tokio_stream::{Stream, StreamExt};

use crate::domain::Quote;

#[derive(Clone)]
pub struct QuoteBroadcaster {
    tx: broadcast::Sender<Quote>,
}

impl QuoteBroadcaster {
    pub fn new(capacity: usize) -> Self {
        let (tx, _) = broadcast::channel(capacity);
        Self { tx }
    }

    pub fn publish(&self, quote: Quote) {
        let _ = self.tx.send(quote);
    }

    pub fn subscribe_sse(&self) -> Sse<impl Stream<Item = Result<Event, Infallible>>> {
        let rx = self.tx.subscribe();
        let stream = BroadcastStream::new(rx).filter_map(|msg| match msg {
            Ok(quote) => {
                let data = serde_json::to_string(&quote).ok()?;
                Some(Ok(Event::default().event("quote").data(data)))
            }
            Err(_) => None, // Lagged subscriber skipped old messages
        });

        Sse::new(stream).keep_alive(KeepAlive::new().interval(Duration::from_secs(15)))
    }
}
```

### 3. Connect Browser `EventSource` in `web/static/app.js`
Subscribe to `/api/v1/stream` using `new EventSource("/api/v1/stream")` and update matching ticker rows in the DOM on `"quote"` events.

---

## ✅ Acceptance Criteria
- [ ] `QuoteBroadcaster` fans out `Quote` updates to N concurrent subscribers via `tokio::sync::broadcast`.
- [ ] `GET /api/v1/stream` streams `text/event-stream` events with keep-alive pings.
- [ ] Disconnecting a browser tab drops its `BroadcastStream` with zero leaked tasks or channels.
- [ ] Live updates appear on the dashboard automatically when quotes are published.
