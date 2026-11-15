# Story 007: Concurrent Multi-Symbol Fetcher

## User Story
**As a** portfolio investor,
**I want to** query quotes for a batch of 20+ stock tickers simultaneously,
**So that** query latency is bounded by the slowest single request rather than the sum of sequential requests, with compile-time data-race safety.

---

## 📖 Book Alignment
* **Reference:** *The Rust Programming Language* (TRPL — [doc.rust-lang.org/book](https://doc.rust-lang.org/book/))
* **Chapters:**
  - Chapter 16: *Fearless Concurrency*
    - 16.1 *Using Threads to Run Code Simultaneously* (`std::thread::spawn`, `JoinHandle`, `move` closures)
    - 16.4 *Extensible Concurrency with the `Sync` and `Send` Traits*
  - Chapter 17: *Fundamentals of Asynchronous Programming: Async, Await, Futures, and Streams*
    - 17.3 *Working with Any Number of Futures* (`join_all`, `tokio::task::JoinSet`)

---

## 🎯 What You Will Learn
1. How Rust's ownership and `Send` / `Sync` marker traits eliminate data races at compile time ("fearless concurrency").
2. Comparing OS thread concurrency (`std::thread::scope`) vs async task concurrency (`tokio::task::JoinSet`).
3. Using `move` closures and `Arc<dyn StockProvider>` to share a provider safely across concurrent tasks.
4. Aggregating per-symbol `Result<Quote, StockError>` values into a deterministic `HashMap<String, Result<Quote, StockError>>`.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Create `StockService`
In `src/service/mod.rs`:
```rust
use std::collections::HashMap;
use std::sync::Arc;

use tokio::task::JoinSet;

use crate::domain::{Quote, StockError};
use crate::provider::StockProvider;

pub struct StockService {
    provider: Arc<dyn StockProvider>,
}

impl StockService {
    pub fn new(provider: Arc<dyn StockProvider>) -> Self {
        Self { provider }
    }

    pub async fn fetch_quotes_batch(
        &self,
        symbols: &[String],
    ) -> HashMap<String, Result<Quote, StockError>> {
        let mut set = JoinSet::new();

        for symbol in symbols {
            let provider = Arc::clone(&self.provider);
            let sym = symbol.clone();
            set.spawn(async move {
                let res = provider.fetch_quote(&sym).await;
                (sym, res)
            });
        }

        let mut results = HashMap::with_capacity(symbols.len());
        while let Some(joined) = set.join_next().await {
            if let Ok((sym, res)) = joined {
                results.insert(sym, res);
            }
        }
        results
    }
}
```

### 2. Experiment with `std::thread::scope` (Optional Sync Exercise)
Write a small exercise or unit test using `std::thread::scope` to observe how Rust allows borrowing local slices across scoped OS threads without `Arc`!

---

## ✅ Acceptance Criteria
- [ ] `StockService::fetch_quotes_batch` fetches all requested symbols concurrently using `JoinSet` (or `futures::future::join_all`).
- [ ] Partial failures for one symbol do not cancel or fail valid quotes for other symbols.
- [ ] A test with artificial per-symbol delays (e.g., 10 symbols × 50ms) completes in ~50–100ms instead of >500ms.
