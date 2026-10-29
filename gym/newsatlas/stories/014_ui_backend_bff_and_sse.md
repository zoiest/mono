# Story 014: UI Backend (BFF & SSE)

## User Story
**As a** frontend platform engineer,  
**I want to** build a Backend-For-Frontend (BFF) service that maintains Redis read-model projections and multiplexes real-time Server-Sent Events (SSE),  
**So that** the React web portal receives perfectly tailored data models and live UI updates over a single connection.

---

## 📖 Book Alignment
📖 **Go in Practice (2nd Ed) Alignment:**
- [Chapter 05: Concurrency in Go](../writings/go_in_practice_notes.md#chapter-05-concurrency-in-go) — §5.2 Fan-out broadcast channels, thread-safe SSE client connection registry guarded by `sync.RWMutex`.
- [Chapter 07: File Access and Basic Networking](../writings/go_in_practice_notes.md#chapter-07-file-access-and-basic-networking) — §7.4 Implementing real-time streaming with Server-Sent Events (SSE) using `http.Flusher`.
- [Chapter 10: Sending and Receiving Data](../writings/go_in_practice_notes.md#chapter-10-sending-and-receiving-data) — §10.2 Streaming JSON encoders for real-time market updates.

---

## 🎯 What You Will Learn
- **Core Objective:** Own everything that is "about the user's experience" and not "about the news".
- **Architectural Concepts:** CQRS read models, event-sourced projections (light), idempotent consumers,
lazy-load/search with cursors, clustering algorithms for maps (grid / geohash /
`ST_ClusterDBSCAN` / Supercluster), transactions (`committx` pattern), settings
synchronisation across instances.

---

## 🛠️ Step-by-Step Implementation Guide

### Implementation Tasks
1. ent schemas: `SavedView`, `Bookmark`, `UserPref`, `Watchlist` (+ items, ordering,
   notes, per-user alert preferences), `MapCell` (read model).
2. Projection consumer: from `story.events` build **geohash-bucketed counts**
   per (cell, hour, category) for fast cluster queries at any zoom.
3. `GetClusters(bbox, zoom, filters)`: choose geohash precision from zoom; return
   `{lat, lon, count, top_category, sample_headline_ids}`.
4. Lazy-load search: full-text (Postgres `tsvector`) + filters + keyset
   pagination; return a `next_cursor`.
5. Per-user data with authorisation checks in the service layer (a user can
   never read another user's bookmarks - write a test that tries).
6. A tiny **transaction helper** (`WithTx(ctx, func(tx) error)`) that commits or
   rolls back and publishes domain events after commit.
7. Synchronise preferences across instances via a broadcast event + cache
   invalidation.
8. **Watchlist read model**: a projection of the latest quote + day change for
   every instrument that appears in at least one watchlist (fed by `quote.live`
   / `bar.closed`), so loading a 50-instrument watchlist is one cheap query
   rather than 50 calls to `market-service`. Also store per-user "last seen"
   markers so the portal can badge *new* moves/headlines since the last visit.

---

## 📦 Deliverables
`GET /map/clusters` returns in < 100 ms for the whole world at zoom 2 and for
a city at zoom 12 with 1M headlines.

---

## 🧪 Deep-Dive Exercises
Compare three clustering strategies on latency and visual quality; write an ADR.

---

## 🤔 Reflection & Architectural Questions
When is a projection better than a live query? What staleness is acceptable
for the map and for bookmarks?
