# Story 005: Idiomatic Error Handling with Result & `?`

## User Story
**As a** software engineer debugging failed network queries,
**I want** errors to clearly distinguish between missing symbols, network timeouts, rate limiting, and upstream server errors,
**So that** calling layers can match on `StockError` variants exhaustively and propagate context cleanly with `?`.

---

## 📖 Book Alignment
* **Reference:** *The Rust Programming Language* (TRPL — [doc.rust-lang.org/book](https://doc.rust-lang.org/book/))
* **Chapters:**
  - Chapter 9: *Error Handling*
    - 9.1 *Unrecoverable Errors with `panic!`*
    - 9.2 *Recoverable Errors with `Result`* (Matching on errors, shortcuts `unwrap`/`expect`, propagating errors with `?`)
    - 9.3 *To `panic!` or Not to `panic!`* (Guidelines for error handling, custom types for validation)
  - Chapter 19: *Patterns and Matching*
    - 19.3 *Pattern Syntax* (Destructuring enums in `match` arms)

---

## 🎯 What You Will Learn
1. Why Rust separates recoverable errors (`Result<T, E>`) from unrecoverable bugs (`panic!`).
2. Designing a domain-specific `StockError` enum covering all failure modes.
3. Implementing `std::fmt::Display`, `std::error::Error` (with `source()`), and `From<E>` conversions (first manually, then cleanly with `thiserror`).
4. Using the `?` operator for concise, zero-boilerplate error propagation.
5. Exhaustive `match` handling in callers (e.g., deciding whether to fail over or abort).

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Define `StockError`
In `src/domain/error.rs`:
```rust
use std::fmt;

use super::ProviderType;

#[derive(Debug)]
pub enum StockError {
    SymbolNotFound {
        symbol: String,
        provider: ProviderType,
    },
    RateLimited {
        provider: ProviderType,
        retry_after_secs: Option<u64>,
    },
    NetworkTimeout {
        provider: ProviderType,
    },
    Upstream {
        provider: ProviderType,
        status: u16,
        message: String,
    },
    Http(reqwest::Error),
    Parse(String),
    AllProvidersFailed(Vec<StockError>),
}
```

### 2. Implement `Display`, `Error`, and `From`
Write `Display` and `std::error::Error` (returning `Some(err)` in `fn source(&self)` for wrapped errors like `StockError::Http(err)`), plus `impl From<reqwest::Error> for StockError`:
```rust
impl From<reqwest::Error> for StockError {
    fn from(err: reqwest::Error) -> Self {
        if err.is_timeout() {
            StockError::NetworkTimeout {
                provider: ProviderType::Unknown,
            }
        } else {
            StockError::Http(err)
        }
    }
}
```
*(Optional upgrade: compare your manual impl with `#[derive(thiserror::Error)]`.)*

### 3. Add Semantic Helpers and Propagate with `?`
Add a helper `pub fn is_retryable(&self) -> bool` using `match self`:
```rust
impl StockError {
    pub fn is_retryable(&self) -> bool {
        matches!(
            self,
            StockError::RateLimited { .. }
                | StockError::NetworkTimeout { .. }
                | StockError::Upstream { status, .. } if *status >= 500
        )
    }
}
```
Update `StockProvider` methods to return `Result<Quote, StockError>` and `Result<Vec<HistoricalPrice>, StockError>`.

---

## ✅ Acceptance Criteria
- [ ] `StockError` implements `Debug`, `Display`, and `std::error::Error` (preserving `source()`).
- [ ] `From<reqwest::Error>` converts HTTP/timeout errors automatically when using `?`.
- [ ] `StockProvider` and `YahooProvider` return `Result<_, StockError>` with zero `.unwrap()` calls in library code.
- [ ] Unit tests verify `Display` messages, `is_retryable()`, and exhaustive pattern matching on variants.
