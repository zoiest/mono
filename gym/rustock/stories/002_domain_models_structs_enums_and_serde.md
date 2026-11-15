# Story 002: Domain Models, Structs, Enums & Serde

## User Story
**As a** financial application developer,
**I want to** define core domain models (`Quote`, `HistoricalPrice`, `ProviderType`),
**So that** stock data can be serialized to and from JSON with compile-time type safety, `Option<T>` nullability, and business methods.

---

## 📖 Book Alignment
* **Reference:** *The Rust Programming Language* (TRPL — [doc.rust-lang.org/book](https://doc.rust-lang.org/book/))
* **Chapters:**
  - Chapter 5: *Using Structs to Structure Related Data*
    - 5.1 *Defining and Instantiating Structs*
    - 5.3 *Method Syntax* (`impl` blocks, `&self` borrowing)
  - Chapter 6: *Enums and Pattern Matching*
    - 6.1 *Defining an Enum* & `Option<T>`
    - 6.2 *The `match` Control Flow Construct*
    - 6.3 *Concise Control Flow with `if let` and `let else`*
  - Chapter 10: *Generic Types, Traits, and Lifetimes*
    - 10.2 *Traits: Defining Shared Behavior* (`Display`, `FromStr`, `Default`, `Serialize`, `Deserialize`)

---

## 🎯 What You Will Learn
1. Defining algebraic enums (`ProviderType`) and deriving standard traits (`Debug`, `Clone`, `Copy`, `PartialEq`, `Eq`, `Default`).
2. Implementing `std::fmt::Display` and `std::str::FromStr` on custom types.
3. Modeling optional fields safely with `Option<T>` instead of sentinel zero values.
4. Using `#[derive(Serialize, Deserialize)]` and `#[serde(...)]` attributes for clean JSON encoding.
5. Writing `impl` methods with `&self` and unit tests inside `#[cfg(test)] mod tests`.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Define `ProviderType` Enum
In `src/domain/provider.rs`:
```rust
use std::fmt;
use std::str::FromStr;

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Default, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum ProviderType {
    #[default]
    Unknown,
    Yahoo,
    Finviz,
    Mock,
}

impl fmt::Display for ProviderType {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let name = match self {
            ProviderType::Yahoo => "yahoo",
            ProviderType::Finviz => "finviz",
            ProviderType::Mock => "mock",
            ProviderType::Unknown => "unknown",
        };
        write!(f, "{name}")
    }
}
```

### 2. Define `Quote` Struct and Methods
In `src/domain/quote.rs`:
```rust
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

use super::provider::ProviderType;

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Quote {
    pub symbol: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub company_name: Option<String>,
    pub price: f64,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub previous_close: Option<f64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub open: Option<f64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub day_high: Option<f64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub day_low: Option<f64>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub volume: Option<u64>,
    pub provider: ProviderType,
    #[serde(default = "Utc::now")]
    pub updated_at: DateTime<Utc>,
}

impl Quote {
    pub fn change(&self) -> f64 {
        match self.previous_close {
            Some(prev) if prev != 0.0 => self.price - prev,
            _ => 0.0,
        }
    }

    pub fn change_percent(&self) -> f64 {
        match self.previous_close {
            Some(prev) if prev != 0.0 => (self.change() / prev) * 100.0,
            _ => 0.0,
        }
    }
}
```

### 3. Add Historical Data Model
In `src/domain/historical.rs`:
```rust
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct HistoricalPrice {
    pub date: DateTime<Utc>,
    pub open: f64,
    pub high: f64,
    pub low: f64,
    pub close: f64,
    pub volume: u64,
}
```

---

## ✅ Acceptance Criteria
- [X] `ProviderType` implements `Display`, `FromStr`, `Default`, and `serde` JSON serialization.
- [X] `Quote` uses `Option<T>` for optional fields, omits `None` on serialization, and provides `change()` and `change_percent()`.
- [X] `HistoricalPrice` models OHLCV bars cleanly.
- [X] Unit tests in `src/domain/provider.rs` and `src/domain/quote.rs` verify math calculations, parsing, and JSON serialization.
