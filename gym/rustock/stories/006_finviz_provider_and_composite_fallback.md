# Story 006: Finviz Provider & Composite Fallback Engine

## User Story
**As a** stock trader using `rustock`,
**I want to** fetch stock data from Finviz or automatically fail over to secondary providers if Yahoo Finance is rate-limited or unavailable,
**So that** the application delivers high availability across independent financial data sources.

---

## 📖 Book Alignment
* **Reference:** *The Rust Programming Language* (TRPL — [doc.rust-lang.org/book](https://doc.rust-lang.org/book/))
* **Chapters:**
  - Chapter 10: *Generic Types, Traits, and Lifetimes*
    - 10.2 *Traits: Defining Shared Behavior*
  - Chapter 15: *Smart Pointers*
    - 15.1 *Using `Box<T>` to Point to Data on the Heap*
    - 15.4 *`Rc<T>`, the Reference Counted Smart Pointer* (and thread-safe `Arc<T>`)
  - Chapter 18: *Object-Oriented Programming Features of Rust*
    - 18.2 *Using Trait Objects That Allow for Values of Different Types* (`Vec<Arc<dyn StockProvider>>`)

---

## 🎯 What You Will Learn
1. Implementing the same `StockProvider` trait across multiple concrete structs (`YahooProvider`, `FinvizProvider`, `MockProvider`).
2. Storing heterogeneous providers in a `Vec<Arc<dyn StockProvider>>` using trait objects.
3. Implementing the Composite pattern in Rust to provide ordered automatic failover.
4. Aggregating multiple provider errors into `StockError::AllProvidersFailed(Vec<StockError>)`.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Implement `MockProvider` & `FinvizProvider`
- In `src/provider/mock.rs`: create `MockProvider` backed by a `HashMap<String, Quote>` for deterministic offline runs and testing.
- In `src/provider/finviz.rs`: create `FinvizProvider` that fetches quote pages and parses HTML/table metrics (e.g., with `scraper`).

### 2. Build `CompositeProvider`
In `src/provider/composite.rs`:
```rust
use std::sync::Arc;

use async_trait::async_trait;

use crate::domain::{HistoricalPrice, ProviderType, Quote, StockError};
use super::StockProvider;

pub struct CompositeProvider {
    providers: Vec<Arc<dyn StockProvider>>,
}

impl CompositeProvider {
    pub fn new(providers: Vec<Arc<dyn StockProvider>>) -> Self {
        Self { providers }
    }
}

#[async_trait]
impl StockProvider for CompositeProvider {
    fn name(&self) -> ProviderType {
        self.providers
            .first()
            .map(|p| p.name())
            .unwrap_or(ProviderType::Unknown)
    }

    async fn fetch_quote(&self, symbol: &str) -> Result<Quote, StockError> {
        let mut errors = Vec::new();
        for provider in &self.providers {
            match provider.fetch_quote(symbol).await {
                Ok(quote) => return Ok(quote),
                Err(err) => errors.push(err),
            }
        }
        Err(StockError::AllProvidersFailed(errors))
    }

    async fn fetch_history(
        &self,
        symbol: &str,
        range: &str,
        interval: &str,
    ) -> Result<Vec<HistoricalPrice>, StockError> {
        let mut errors = Vec::new();
        for provider in &self.providers {
            match provider.fetch_history(symbol, range, interval).await {
                Ok(history) => return Ok(history),
                Err(err) => errors.push(err),
            }
        }
        Err(StockError::AllProvidersFailed(errors))
    }
}
```

---

## ✅ Acceptance Criteria
- [ ] `MockProvider` and `FinvizProvider` both implement `StockProvider`.
- [ ] `CompositeProvider` accepts `Vec<Arc<dyn StockProvider>>` and tries each provider in order.
- [ ] If the primary provider returns `Err`, `CompositeProvider` falls back to the next provider seamlessly.
- [ ] If all providers fail, `StockError::AllProvidersFailed` preserves every underlying failure.
