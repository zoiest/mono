# Story 009: Market Service & TimescaleDB

## User Story
**As a** time-series engineer,  
**I want to** build the Market service with TimescaleDB hypertables, continuous aggregates, and real-time in-memory 1m OHLCV candle aggregation,  
**So that** high-frequency ticks are rolled up into queryable historical bars and streaming candles.

---

## 📖 Book Alignment
📖 **Go in Practice (2nd Ed) Alignment:**
- [Chapter 03: Structs, Interfaces, and Generics](../writings/go_in_practice_notes.md#chapter-03-structs-interfaces-and-generics) — §3.1 Precision decimal modeling (`shopspring/decimal` or fixed-point integer cents), preventing IEEE 754 float rounding inaccuracies.
- [Chapter 05: Concurrency in Go](../writings/go_in_practice_notes.md#chapter-05-concurrency-in-go) — §5.2 State synchronization for in-flight candle builders using `sync.RWMutex`, timer-driven tumbling window flushes.
- [Chapter 06: Formatting, Testing, Debugging, and Benchmarking](../writings/go_in_practice_notes.md#chapter-06-formatting-testing-debugging-and-benchmarking) — §6.5 Benchmarking aggregation throughput and profiling zero-allocation bar builders (`testing.B`).

---

## 🎯 What You Will Learn
- **Core Objective:** Turn raw quotes into trustworthy OHLCV bars at several resolutions, store
them efficiently, and serve fast range queries.
- **Architectural Concepts:** TimescaleDB (hypertables, chunking, compression, continuous aggregates,
retention policies), event time vs processing time, **watermarks and allowed
lateness**, out-of-order data, idempotent upserts with revisions, trading
calendars and sessions, time zones/DST, corporate actions and **adjusted
prices**, exact decimals, downsampling for charts, caching.

---

## 🛠️ Step-by-Step Implementation Guide

### Implementation Tasks
1. Schema (raw SQL migrations for Timescale parts, ent for the rest):
   - `bar_1m(instrument_id, ts_open, o, h, l, c, v, trades, is_final, revision)`
     as a hypertable; `PRIMARY KEY (instrument_id, ts_open)`.
   - 5m / 1h via **continuous aggregates**; 1D computed per **exchange
     session** (not UTC midnight) by a rollup task using the calendar.
   - `corporate_action` table; adjusted view/materialisation for splits.
   - Compression policy for chunks older than N days; retention policy for 1m.
2. **Aggregator** (in-memory, per instrument): fold ticks into the open bar;
   watermark = max event time seen - allowed lateness (e.g. 5 s); close bars
   when the watermark passes their end; late ticks after close produce a
   **revision** (upsert + `bar.closed` with `revision+1`) up to a hard limit,
   then are counted and dropped.
3. **Validation** rules: reject non-positive prices; flag a jump > X% vs last
   price for review instead of silently accepting; reject ticks from the
   far future; de-duplicate by `(source, seq)` or hash.
4. **Latest-quote cache** (Redis or in-memory + broadcast) + throttled
   `quote.live` (e.g. max 2/s per instrument) to protect the UI.
5. **Trading calendar** package: given MIC + instant -> is the market open,
   session start/end, previous/next session; handle holidays, half days and
   DST changes. Test around DST switches and Lunar New Year closures.
6. `MarketQueryService` gRPC: `GetBars` (with `adjusted`, `limit`, and server-side
   **downsampling** so a 5-year 1m request cannot return 2M points),
   `GetLatest` (batch), `GetSnapshot` (last, prev close, % change, 52-week
   hi/lo, avg volume).
7. Startup **recovery**: on boot reload open-bar state from the last N minutes
   of ticks/bars so a restart doesn't corrupt the current candle.
8. Backfill ingestion path: `RawBar` from REST/CSV adapters is written through
   the same validation + upsert (and **never overwrites a final bar from a
   better source with a worse one** - define source priority).
9. Metrics: `bars_closed_total`, `late_ticks_total{outcome}`,
   `aggregation_lag_seconds`, `gap_minutes_total`, `rejected_ticks_total{reason}`.

---

## 📦 Deliverables
`GET /bars?interval=5m` for a symbol returns correct candles that match what
a reference chart (from your data provider) shows, within documented rounding.

---

## 🤔 Reflection & Architectural Questions
Why do tick processing and bar *finalisation* need an event-time watermark
rather than "close the bar when the wall clock hits :00"? What is the cost of a
longer allowed lateness for the chart, and for downstream event detection?
