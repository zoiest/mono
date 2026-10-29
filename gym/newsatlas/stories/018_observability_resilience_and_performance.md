# Story 018: Observability, Resilience & Performance

## User Story
**As a** SRE / performance engineer,  
**I want to** instrument all services with OpenTelemetry distributed tracing, Prometheus metrics, structured logs, and pprof profiling,  
**So that** system latency, bottlenecks, and error cascades are visible and debuggable across the distributed topology.

---

## 📖 Book Alignment
📖 **Go in Practice (2nd Ed) Alignment:**
- [Chapter 06: Formatting, Testing, Debugging, and Benchmarking](../writings/go_in_practice_notes.md#chapter-06-formatting-testing-debugging-and-benchmarking) — §6.2 Structured logging with `log/slog` handlers and trace correlation, §6.5 Profiling CPU, memory, and lock contention with `net/http/pprof`.
- [Chapter 12: Cloud-Ready Applications](../writings/go_in_practice_notes.md#chapter-12-cloud-ready-applications-and-communications) — §12.2 Production readiness, metrics instrumentation (`/metrics`), OpenTelemetry span propagation.
- [The Ten Cardinal Rules](../writings/go_in_practice_notes.md#the-ten-cardinal-rules-of-idiomatic-go) — Rule 5: *Use log/slog for structured, contextual logging* & Rule 10: *Profile before optimizing*.

---

## 🎯 What You Will Learn
- **Core Objective:** Be able to *see* the system and *prove* it survives failure.
- **Architectural Concepts:** RED/USE metrics, cardinality, histograms, distributed tracing across async
boundaries, structured logs, SLOs, chaos engineering, load testing, pprof.

---

## 🛠️ Step-by-Step Implementation Guide

### Implementation Tasks
1. Prometheus metrics in the shared libs: gRPC/HTTP server+client, bus
   (published, consumed, lag, retries, DLQ), DB pool, cache hit rate, adapter
   fetch results.
2. OpenTelemetry tracing: propagate `trace_id` through **bus headers** so one
   trace spans adapter -> enrichment -> story -> gateway SSE.
3. Grafana dashboards (committed as JSON): pipeline throughput & lag, adapter
   health, API latency, error budget.
4. Alerts on: consumer lag > X, DLQ non-empty, no heartbeats, error rate.
5. Chaos scenarios (scripted): kill Redis; kill Postgres; kill an adapter; slow
   network (use `toxiproxy`); duplicate/burst events from the replay adapter.
6. `k6` load tests; profile with `pprof`; fix the top 3 hot spots.
7. Define 3-5 SLOs and measure them, e.g. "95% of headlines visible on map
   < 60 s after publication", "95% of live quotes reach the browser < 2 s after
   the exchange timestamp", "API p95 < 300 ms", "99.5% gateway availability",
   "no unexplained gap > 5 min in 1m bars for liquid instruments during
   market hours".
8. **Data-quality metrics** as first-class citizens: bar gaps, stale quote age
   per instrument, late-tick ratio, link coverage (% of business headlines with
   >= 1 link), duplicate ratio, detector event rate per day (a sudden jump means
   a bug or a bad feed). Graph *end-to-end freshness* (event time -> UI time).
9. Chaos for the market path: drop the stream connection for 60 s then
   reconnect; replay a burst of 100k ticks; deliver ticks out of order; restart
   `market-service` mid-minute; feed a bad price (x1000) and verify it never
   becomes a final bar or triggers a false "flash crash" alert.

---

## ✅ Acceptance Criteria ("Done When")
- [ ] A written **post-mortem** (`docs/notes/chaos-1.md`) for each chaos scenario:
- [ ] what broke, how you noticed, what you changed.

---

## 🤔 Reflection & Architectural Questions
Which metric label could explode your Prometheus cardinality in this system?
