# Story 004: Provider Trait & Yahoo Finance Client

## User Story
**As an** application service,
**I want to** define a unified `StockProvider` trait and implement an async Yahoo Finance HTTP client,
**So that** the application can fetch real-world stock quotes and historical OHLC data with explicit client timeouts.

---

## 📖 Book Alignment
* **Reference:** *The Rust Programming Language* (TRPL — [doc.rust-lang.org/book](https://doc.rust-lang.org/book/))
* **Chapters:**
  - Chapter 10: *Generic Types, Traits, and Lifetimes*
    - 10.2 *Traits: Defining Shared Behavior* (Trait definitions, default implementations, trait bounds)
  - Chapter 17: *Fundamentals of Asynchronous Programming: Async, Await, Futures, and Streams*
    - 17.1 *Futures and the Async Syntax*
  - Chapter 18: *Object-Oriented Programming Features of Rust*
    - 18.2 *Using Trait Objects That Allow for Values of Different Types* (`dyn StockProvider`)

---

## 🎯 What You Will Learn
1. Defining shared behavior in Rust via `trait StockProvider`.
2. Understanding async traits (`async-trait` or `Pin<Box<dyn Future>>`) when using trait objects (`Arc<dyn StockProvider>`).
3. Configuring a production-grade `reqwest::Client` with `connect_timeout` and `timeout`.
4. Deserializing deeply nested third-party JSON payloads into clean domain structs (`Quote`, `HistoricalPrice`).

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Add Async & HTTP Crates to `Cargo.toml`
```toml
tokio = { version = "1", features = ["full"] }
reqwest = { version = "0.12", default-features = false, features = ["json", "rustls-tls"] }
async-trait = "0.1"
```

### 2. Define the `StockProvider` Trait
In `src/provider/mod.rs`:
```rust
use async_trait::async_trait;

use crate::domain::{HistoricalPrice, ProviderType, Quote};

pub mod yahoo;

#[async_trait]
pub trait StockProvider: Send + Sync {
    fn name(&self) -> ProviderType;
    async fn fetch_quote(&self, symbol: &str) -> Result<Quote, String>;
    async fn fetch_history(
        &self,
        symbol: &str,
        range: &str,
        interval: &str,
    ) -> Result<Vec<HistoricalPrice>, String>;
}
```
*(Note: In Story 005, you will replace `String` with a rich `StockError` enum!)*

### 3. Implement `YahooProvider`
In `src/provider/yahoo.rs`:
```rust
use std::time::Duration;

use async_trait::async_trait;
use chrono::{TimeZone, Utc};
use reqwest::Client;
use serde::Deserialize;

use crate::domain::{HistoricalPrice, ProviderType, Quote};
use super::StockProvider;

pub struct YahooProvider {
    client: Client,
    base_url: String,
}

impl YahooProvider {
    pub fn new(timeout: Duration) -> Result<Self, reqwest::Error> {
        let client = Client::builder()
            .connect_timeout(Duration::from_secs(3))
            .timeout(timeout)
            .user_agent("rustock/0.1")
            .build()?;

        Ok(Self {
            client,
            base_url: "https://query1.finance.yahoo.com".to_string(),
        })
    }

    /// Useful for injecting a mock HTTP server URL in tests.
    pub fn with_base_url(mut self, base_url: impl Into<String>) -> Self {
        self.base_url = base_url.into();
        self
    }
}
```

### 4. Map Nested Yahoo Finance Chart JSON
Define private `#[derive(Deserialize)]` structs matching Yahoo's `chart.result[0]` schema so external API quirks stay encapsulated inside `src/provider/yahoo.rs` and never leak into `crate::domain`.

---

## ✅ Acceptance Criteria
- [ ] `StockProvider` trait requires `Send + Sync` so providers can be shared safely across async tasks.
- [ ] `YahooProvider` configures explicit connection and request timeouts via `reqwest::Client::builder()`.
- [ ] Yahoo Finance chart JSON is parsed cleanly into `Quote` and `Vec<HistoricalPrice>`.
- [ ] `with_base_url` allows pointing `YahooProvider` at a local mock server during tests.
