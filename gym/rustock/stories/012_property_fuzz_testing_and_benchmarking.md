# Story 012: Property/Fuzz Testing & Benchmarking

## User Story
**As a** systems performance engineer,
**I want to** property-test and fuzz-test JSON/HTML response parsers and benchmark cache lookups,
**So that** malformed payloads never panic in production and hot paths benefit from zero-cost iterator optimizations.

---

## 📖 Book Alignment
* **Reference:** *The Rust Programming Language* (TRPL — [doc.rust-lang.org/book](https://doc.rust-lang.org/book/))
* **Chapters:**
  - Chapter 11: *Writing Automated Tests*
  - Chapter 13: *Functional Language Features: Iterators and Closures*
    - 13.2 *Processing a Series of Items with Iterators*
    - 13.4 *Comparing Performance: Loops vs. Iterators*
  - Chapter 14: *More About Cargo and Crates.io*
    - 14.1 *Customizing Builds with Release Profiles* (`[profile.release]`, `opt-level`, `lto`)

---

## 🎯 What You Will Learn
1. Why Rust iterators compile down to the same (or faster) machine code as hand-written loops ("zero-cost abstractions").
2. Writing statistical microbenchmarks with `criterion` (`cargo bench`).
3. Writing property-based tests with `proptest` (and optional fuzz targets with `cargo-fuzz`) to verify parsers never panic on arbitrary input.
4. Tuning `[profile.release]` in `Cargo.toml` for throughput vs binary size.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Add `criterion` and `proptest` to `[dev-dependencies]`
```toml
[dev-dependencies]
criterion = "0.5"
proptest = "1"

[[bench]]
name = "cache_and_parse"
harness = false
```

### 2. Write Criterion Benchmarks in `benches/cache_and_parse.rs`
```rust
use std::time::Duration;
use criterion::{black_box, criterion_group, criterion_main, Criterion};
use chrono::Utc;
use rustock::cache::TtlCache;
use rustock::domain::{ProviderType, Quote};

fn bench_cache_get(c: &mut Criterion) {
    let cache = TtlCache::new(Duration::from_secs(60));
    cache.insert(
        "AAPL".to_string(),
        Quote {
            symbol: "AAPL".to_string(),
            company_name: None,
            price: 185.0,
            previous_close: Some(180.0),
            open: None,
            day_high: None,
            day_low: None,
            volume: None,
            provider: ProviderType::Mock,
            updated_at: Utc::now(),
        },
    );

    c.bench_function("ttl_cache_hit", |b| {
        b.iter(|| black_box(cache.get(&"AAPL".to_string())))
    });
}

criterion_group!(benches, bench_cache_get);
criterion_main!(benches);
```

### 3. Add Property Tests for Parsers
Use `proptest!` to feed arbitrary strings into `ProviderType::from_str` and Yahoo/Finviz JSON decoders, asserting they always return `Ok` or `Err` gracefully without panicking.

### 4. Tune Release Profile
Add `[profile.release]` in `Cargo.toml`:
```toml
[profile.release]
opt-level = 3
lto = "thin"
codegen-units = 1
```

---

## ✅ Acceptance Criteria
- [ ] `cargo bench` runs Criterion benchmarks for `TtlCache::get` and quote JSON deserialization.
- [ ] Property tests (`proptest!`) verify parsers never panic on arbitrary/malformed inputs.
- [ ] Iterator-based OHLC aggregation pipelines replace manual index loops cleanly.
- [ ] `[profile.release]` is configured and verified with `cargo build --release`.
