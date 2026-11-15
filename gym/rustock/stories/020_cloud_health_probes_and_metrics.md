# Story 020: Cloud Health Probes & Runtime Metrics

## User Story
**As a** Kubernetes or Docker platform engineer,
**I want** explicit `/healthz` (liveness) and `/readyz` (readiness) endpoints reporting lock-free application metrics,
**So that** orchestrators know when the service is alive, ready for traffic, and how cache/provider requests are performing.

---

## 📖 Book Alignment
* **Reference:** *The Rust Programming Language* (TRPL — [doc.rust-lang.org/book](https://doc.rust-lang.org/book/))
* **Chapters:**
  - Chapter 8: *Common Collections*
  - Chapter 16: *Fearless Concurrency*
    - 16.3 *Shared-State Concurrency* (Lock-free atomic counters `AtomicU64` + `Ordering::Relaxed`)

---

## 🎯 What You Will Learn
1. Designing Kubernetes-compatible liveness (`/healthz`) vs readiness (`/readyz`) probes.
2. Tracking high-throughput metrics (total requests, cache hits, cache misses, upstream errors) without mutex contention using `std::sync::atomic::AtomicU64`.
3. Exposing JSON diagnostics (`/metrics`) containing uptime, atomic counters, and cache size.
4. Checking upstream provider reachability or shutdown state inside `/readyz` (returning HTTP 503 during graceful drain).

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Define Lock-Free `AppMetrics`
In `src/telemetry/metrics.rs`:
```rust
use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};
use std::time::Instant;

use serde::Serialize;

pub struct AppMetrics {
    started_at: Instant,
    ready: AtomicBool,
    requests_total: AtomicU64,
    cache_hits: AtomicU64,
    cache_misses: AtomicU64,
    provider_errors: AtomicU64,
}

#[derive(Serialize)]
pub struct MetricsSnapshot {
    pub uptime_secs: u64,
    pub ready: bool,
    pub requests_total: u64,
    pub cache_hits: u64,
    pub cache_misses: u64,
    pub provider_errors: u64,
}

impl AppMetrics {
    pub fn new() -> Self {
        Self {
            started_at: Instant::now(),
            ready: AtomicBool::new(true),
            requests_total: AtomicU64::new(0),
            cache_hits: AtomicU64::new(0),
            cache_misses: AtomicU64::new(0),
            provider_errors: AtomicU64::new(0),
        }
    }

    pub fn inc_requests(&self) { self.requests_total.fetch_add(1, Ordering::Relaxed); }
    pub fn inc_cache_hit(&self) { self.cache_hits.fetch_add(1, Ordering::Relaxed); }
    pub fn inc_cache_miss(&self) { self.cache_misses.fetch_add(1, Ordering::Relaxed); }
    pub fn inc_provider_error(&self) { self.provider_errors.fetch_add(1, Ordering::Relaxed); }
    pub fn set_ready(&self, ready: bool) { self.ready.store(ready, Ordering::SeqCst); }
    pub fn is_ready(&self) -> bool { self.ready.load(Ordering::SeqCst) }

    pub fn snapshot(&self) -> MetricsSnapshot {
        MetricsSnapshot {
            uptime_secs: self.started_at.elapsed().as_secs(),
            ready: self.is_ready(),
            requests_total: self.requests_total.load(Ordering::Relaxed),
            cache_hits: self.cache_hits.load(Ordering::Relaxed),
            cache_misses: self.cache_misses.load(Ordering::Relaxed),
            provider_errors: self.provider_errors.load(Ordering::Relaxed),
        }
    }
}
```

---

## ✅ Acceptance Criteria
- [ ] `GET /healthz` always returns HTTP 200 when the process event loop is responsive.
- [ ] `GET /readyz` returns HTTP 200 when ready and HTTP 503 once shutdown begins or dependencies fail.
- [ ] `GET /metrics` exposes `MetricsSnapshot` JSON backed by lock-free atomics.
- [ ] Unit tests verify atomic increment behavior and readiness toggling.
