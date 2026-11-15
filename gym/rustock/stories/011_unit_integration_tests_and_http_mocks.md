# Story 011: Unit, Integration Tests & HTTP Mocks

## User Story
**As a** quality-focused developer,
**I want to** write comprehensive unit tests, integration tests, and local HTTP mocks,
**So that** all business logic, error paths, and response decoders are verified deterministically without making real network calls.

---

## 📖 Book Alignment
* **Reference:** *The Rust Programming Language* (TRPL — [doc.rust-lang.org/book](https://doc.rust-lang.org/book/))
* **Chapters:**
  - Chapter 11: *Writing Automated Tests*
    - 11.1 *How to Write Tests* (`#[test]`, `assert!`, `assert_eq!`, `#[should_panic]`, `Result<(), E>` tests)
    - 11.2 *Controlling How Tests Are Run* (`cargo test -- --test-threads=1`, `--nocapture`, filtering)
    - 11.3 *Test Organization* (`#[cfg(test)]` unit tests vs `tests/` integration tests)

---

## 🎯 What You Will Learn
1. Organizing unit tests (`#[cfg(test)] mod tests`) alongside source modules vs integration tests in `tests/`.
2. Writing `Result`-returning tests (`fn it_works() -> Result<(), Box<dyn Error>>`) and `#[should_panic(expected = "...")]`.
3. Mocking external HTTP APIs deterministically using `wiremock` (or `httpmock`) in `[dev-dependencies]`.
4. Testing HTTP status codes (200, 404, 429, 500), malformed JSON, and timeouts offline.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Add `[dev-dependencies]` in `Cargo.toml`
```toml
[dev-dependencies]
wiremock = "0.6"
```

### 2. Create Integration Tests in `tests/yahoo_provider_test.rs`
```rust
use std::time::Duration;

use wiremock::matchers::{method, path};
use wiremock::{Mock, MockServer, ResponseTemplate};

use rustock::domain::StockError;
use rustock::provider::yahoo::YahooProvider;
use rustock::provider::StockProvider;

#[tokio::test]
async fn yahoo_provider_parses_valid_quote() {
    let server = MockServer::start().await;
    let body = r#"{
        "chart": {
            "result": [{
                "meta": {
                    "symbol": "AAPL",
                    "regularMarketPrice": 182.50,
                    "chartPreviousClose": 180.00
                }
            }]
        }
    }"#;

    Mock::given(method("GET"))
        .and(path("/v8/finance/chart/AAPL"))
        .respond_with(ResponseTemplate::new(200).set_body_string(body))
        .mount(&server)
        .await;

    let provider = YahooProvider::new(Duration::from_secs(2))
        .unwrap()
        .with_base_url(server.uri());

    let quote = provider.fetch_quote("AAPL").await.unwrap();
    assert_eq!(quote.symbol, "AAPL");
    assert_eq!(quote.price, 182.50);
}

#[tokio::test]
async fn yahoo_provider_maps_429_to_rate_limited() {
    let server = MockServer::start().await;

    Mock::given(method("GET"))
        .respond_with(ResponseTemplate::new(429))
        .mount(&server)
        .await;

    let provider = YahooProvider::new(Duration::from_secs(2))
        .unwrap()
        .with_base_url(server.uri());

    let err = provider.fetch_quote("AAPL").await.unwrap_err();
    assert!(matches!(err, StockError::RateLimited { .. }));
}
```

### 3. Run Unit and Integration Tests
```bash
cargo test
cargo test --test yahoo_provider_test -- --nocapture
```

---

## ✅ Acceptance Criteria
- [ ] Unit tests in `src/` test private helpers and edge cases inside `#[cfg(test)]`.
- [ ] Integration tests in `tests/` exercise the public `rustock` library API against `wiremock`.
- [ ] HTTP 200, 404, 429, 500, and timeout scenarios are all tested offline.
- [ ] `cargo test` passes 100% deterministically with zero external network calls.
