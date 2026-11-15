# Story 008: Worker Pool with Rate Limiting

## User Story
**As a** system architect,
**I want to** bound the maximum number of concurrent outbound requests and throttle outgoing traffic with a rate limiter,
**So that** external financial APIs are never overwhelmed and the application degrades gracefully under load or timeouts.

---

## 📖 Book Alignment
* **Reference:** *The Rust Programming Language* (TRPL — [doc.rust-lang.org/book](https://doc.rust-lang.org/book/))
* **Chapters:**
  - Chapter 13: *Functional Language Features: Iterators and Closures*
    - 13.1 *Closures: Anonymous Functions that Capture Their Environment*
  - Chapter 16: *Fearless Concurrency*
    - 16.2 *Using Message Passing to Transfer Data Between Threads* (`mpsc` channels, dropping senders to close channels)
  - Chapter 17: *Fundamentals of Asynchronous Programming: Async, Await, Futures, and Streams*
    - 17.2 *Applying Concurrency with Async* (Channels, racing futures)

---

## 🎯 What You Will Learn
1. Bounded message passing with `tokio::sync::mpsc::channel` (and `std::sync::mpsc::sync_channel`).
2. Enforcing a concurrency cap using `tokio::sync::Semaphore` and RAII `OwnedSemaphorePermit`.
3. Building a token-bucket / interval rate limiter using `tokio::time::interval`.
4. Racing futures with `tokio::select!` and `tokio::time::timeout` for cancellation and deadlines.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Define a Bounded Worker Pool / Rate-Limited Dispatcher
In `src/service/pool.rs`:
```rust
use std::sync::Arc;
use std::time::Duration;

use tokio::sync::{mpsc, Semaphore};
use tokio::time::{interval, timeout};

use crate::domain::{ProviderType, Quote, StockError};
use crate::provider::StockProvider;

pub struct RateLimitedFetcher {
    provider: Arc<dyn StockProvider>,
    semaphore: Arc<Semaphore>,
    tick_interval: Duration,
    task_timeout: Duration,
}

impl RateLimitedFetcher {
    pub fn new(
        provider: Arc<dyn StockProvider>,
        max_concurrent: usize,
        requests_per_sec: u32,
        task_timeout: Duration,
    ) -> Self {
        let tick_ms = (1000 / requests_per_sec.max(1)) as u64;
        Self {
            provider,
            semaphore: Arc::new(Semaphore::new(max_concurrent.max(1))),
            tick_interval: Duration::from_millis(tick_ms),
            task_timeout,
        }
    }

    pub async fn fetch_many(
        &self,
        symbols: Vec<String>,
    ) -> Vec<(String, Result<Quote, StockError>)> {
        let (tx, mut rx) = mpsc::channel(symbols.len().max(1));
        let mut limiter = interval(self.tick_interval);

        for symbol in symbols {
            limiter.tick().await;
            let permit = Arc::clone(&self.semaphore)
                .acquire_owned()
                .await
                .expect("semaphore not closed");
            let provider = Arc::clone(&self.provider);
            let tx = tx.clone();
            let limit = self.task_timeout;

            tokio::spawn(async move {
                let _permit = permit; // Released automatically on drop
                let res = match timeout(limit, provider.fetch_quote(&symbol)).await {
                    Ok(inner) => inner,
                    Err(_) => Err(StockError::NetworkTimeout {
                        provider: ProviderType::Unknown,
                    }),
                };
                let _ = tx.send((symbol, res)).await;
            });
        }

        // Drop the original sender so `rx.recv()` finishes when all workers complete!
        drop(tx);

        let mut out = Vec::new();
        while let Some(item) = rx.recv().await {
            out.push(item);
        }
        out
    }
}
```

---

## ✅ Acceptance Criteria
- [ ] In-flight concurrent requests never exceed `max_concurrent` (enforced via `Semaphore`).
- [ ] Outbound request rate is paced by `tokio::time::interval`.
- [ ] Dropping the original `mpsc::Sender` closes the channel cleanly once all spawned tasks complete.
- [ ] Slow provider responses trigger `StockError::NetworkTimeout` via `tokio::time::timeout`.
