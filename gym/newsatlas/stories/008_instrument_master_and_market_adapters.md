# Story 008: Instrument Master & Market Adapters

## User Story
**As a** market data engineer,  
**I want to** extend the registry with tradable instrument aggregates and build streaming market data adapters (REST daily bars and WebSocket live ticks),  
**So that** financial market pricing is ingested through the same modular adapter architecture as news.

---

## 📖 Book Alignment
📖 **Go in Practice (2nd Ed) Alignment:**
- [Chapter 05: Concurrency in Go](../writings/go_in_practice_notes.md#chapter-05-concurrency-in-go) — §5.3 Worker pools with rate limiters, concurrent WebSocket read/write loops with dedicated ping/pong goroutines.
- [Chapter 07: File Access and Basic Networking](../writings/go_in_practice_notes.md#chapter-07-file-access-and-basic-networking) — §7.4 Network socket lifecycle management (heartbeats, reconnect backoff, and socket read deadlines).
- [Chapter 11: Working with External Services](../writings/go_in_practice_notes.md#chapter-11-working-with-external-services) — §11.1 Handling rate limits with `Retry-After`, §11.2 Managing external financial REST/WebSocket client connections.
- [The Ten Cardinal Rules](../writings/go_in_practice_notes.md#the-ten-cardinal-rules-of-idiomatic-go) — Rule 2: *Never communicate by sharing memory; share memory by communicating* (use channels for quote stream demuxing).

---

## 🎯 What You Will Learn
- **Core Objective:** Teach the platform what a "tradable thing" is, and ingest quotes/bars through
the **same adapter kit** you built for news.
- **Architectural Concepts:** Reference data management, symbol mapping across providers, REST rate limits
(token bucket, `Retry-After`), long-lived WebSocket connections (reconnect,
resubscribe, heartbeat/ping, sequence gaps), snapshot-then-delta patterns,
decimal parsing, clock skew, idempotent backfills, provider terms of use.

---

## 🛠️ Step-by-Step Implementation Guide

### Implementation Tasks
1. **Extend `registry-service`** with an `Instrument` aggregate
   (symbol, exchange MIC, asset class, currency, aliases) + per-source
   `provider_symbol` mappings. Publish `instrument.events`. Add
   `tools/instrument-import` (e.g. US ticker list, a few crypto pairs, major
   FX pairs, 2-3 indices).
2. Extend `Source.kind` with `market`; source `settings` carry the instrument
   subscription list (or a watchlist reference).
3. Extend the **adapter kit** with a second runner type next to the polling
   `SourceRunner`: a **`StreamRunner`** that owns one long-lived connection per
   assigned source (or per shard of instruments), with: connect/backoff,
   resubscribe on reconnect, ping/pong deadlines, bounded in-memory buffer with
   a **drop policy** (what do you do when the bus is slow?), and graceful close.
4. `market-rest-adapter`: daily/intraday bars from a REST API.
   - Respect provider limits with a **per-provider token bucket** shared by all
     sources of that provider (e.g. 5 req/min).
   - Backfill mode: walk a date range in chunks; resumable via adapter `State`.
5. `market-stream-adapter`: WebSocket live quotes/trades (crypto streams are
   free and 24/7 - ideal for learning). Normalise into `RawQuote`; parse prices
   as **strings -> decimal** (never via `float64`).
6. `market-csv-adapter`: end-of-day CSV (download, checksum/ETag, stream-parse,
   handle encoding/locale decimals).
7. Extend `replay-adapter` with a **market mode**: replays a fixture of ticks
   at a configurable speed, with knobs for out-of-order ticks, duplicates,
   gaps, bad prices, and a "flash crash" scenario. You will lean on this
   heavily in Phases 9 and 16.
8. Publish `quote.raw` keyed by `instrument_id` (so a group preserves
   per-instrument order). Include `ts_exchange` (event time) **and**
   `ts_received` (processing time).
9. Extend the **conformance suite** with market-specific checks: no float
   parsing, monotonic seq handling, reconnect resubscribes, context
   cancellation closes the socket.

---

## 📦 Deliverables
With `docker compose up`, a stream adapter produces live crypto quotes and a
REST adapter backfills 1 year of daily bars for 10 symbols; `busctl tail
quote.raw` shows them.

---

## 🤔 Reflection & Architectural Questions
What changed when the adapter went from *pull on a schedule* to *hold a
connection*? Which parts of the kit were still reusable, and which assumptions
(one `Fetch` call = one batch) had to be removed?
