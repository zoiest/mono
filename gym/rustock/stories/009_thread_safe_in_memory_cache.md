# Story 009: Thread-Safe In-Memory Cache with TTL

## User Story
**As an** API consumer,
**I want** recent stock quotes to be cached in memory with a configurable Time-To-Live (TTL),
**So that** redundant external network queries are eliminated and frequent reads remain sub-millisecond.

---

## 📖 Book Alignment
* **Reference:** *The Rust Programming Language* (TRPL — [doc.rust-lang.org/book](https://doc.rust-lang.org/book/))
* **Chapters:**
  - Chapter 8: *Common Collections*
    - 8.3 *Storing Keys with Associated Values in Hash Maps* (`HashMap`)
  - Chapter 10: *Generic Types, Traits, and Lifetimes*
    - 10.1 *Generic Data Types* (`Cache<K, V>`)
    - 10.3 *Validating References with Lifetimes*
  - Chapter 15: *Smart Pointers*
    - 15.5 *Interior Mutability Pattern*
  - Chapter 16: *Fearless Concurrency*
    - 16.3 *Shared-State Concurrency* (`Mutex<T>`, `RwLock<T>`, `Arc<T>`)

---

## 🎯 What You Will Learn
1. Designing a generic struct `TtlCache<K, V>` with trait bounds (`K: Eq + Hash + Clone`, `V: Clone`).
2. Why Rust's `RwLock<T>` wraps the protected *data* (not just a lock flag), preventing unlocked access at compile time.
3. Choosing `std::sync::RwLock` (for short, non-`.await` critical sections) vs `tokio::sync::RwLock`.
4. Passive TTL expiration on read plus active `purge_expired()` cleanup.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Implement Generic `TtlCache<K, V>`
In `src/cache/mod.rs`:
```rust
use std::collections::HashMap;
use std::hash::Hash;
use std::sync::RwLock;
use std::time::{Duration, Instant};

#[derive(Debug, Clone)]
struct CacheEntry<V> {
    value: V,
    expires_at: Instant,
}

pub struct TtlCache<K, V> {
    ttl: Duration,
    store: RwLock<HashMap<K, CacheEntry<V>>>,
}

impl<K, V> TtlCache<K, V>
where
    K: Eq + Hash + Clone,
    V: Clone,
{
    pub fn new(ttl: Duration) -> Self {
        Self {
            ttl,
            store: RwLock::new(HashMap::new()),
        }
    }

    pub fn get(&self, key: &K) -> Option<V> {
        let guard = self.store.read().expect("cache lock poisoned");
        guard.get(key).and_then(|entry| {
            if Instant::now() < entry.expires_at {
                Some(entry.value.clone())
            } else {
                None
            }
        })
    }

    pub fn insert(&self, key: K, value: V) {
        let mut guard = self.store.write().expect("cache lock poisoned");
        guard.insert(
            key,
            CacheEntry {
                value,
                expires_at: Instant::now() + self.ttl,
            },
        );
    }

    pub fn purge_expired(&self) -> usize {
        let now = Instant::now();
        let mut guard = self.store.write().expect("cache lock poisoned");
        let before = guard.len();
        guard.retain(|_, entry| now < entry.expires_at);
        before - guard.len()
    }
}
```

### 2. Wrap `StockService` with Cache-Aside Lookup
Check `cache.get(&symbol)` before calling `provider.fetch_quote(&symbol)`, and call `cache.insert(symbol, quote.clone())` on cache miss.

---

## ✅ Acceptance Criteria
- [ ] `TtlCache<K, V>` is generic over `K: Eq + Hash + Clone` and `V: Clone`.
- [ ] Concurrent reads share access via `RwLock::read()`, while writes acquire `RwLock::write()`.
- [ ] Expired entries are ignored on `get` and removed by `purge_expired`.
- [ ] Unit tests verify hits, misses, TTL expiration, and concurrent multi-thread safety.
