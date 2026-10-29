# Story 004: Adapter Framework & RSS Adapter

## User Story
**As a** ingestion engineer,  
**I want to** build a reusable adapter framework and an RSS feed poller with HTTP conditional caching (ETag/If-Modified-Since) and token bucket rate limiting,  
**So that** external news headlines are collected continuously and published to raw streams without spamming providers.

---

## 📖 Book Alignment
📖 **Go in Practice (2nd Ed) Alignment:**
- [Chapter 03: Structs, Interfaces, and Generics](../writings/go_in_practice_notes.md#chapter-03-structs-interfaces-and-generics) — §3.1 XML and JSON struct tags for feed parsing (`encoding/xml`), struct embedding for common adapter fields.
- [Chapter 05: Concurrency in Go](../writings/go_in_practice_notes.md#chapter-05-concurrency-in-go) — §5.3 Timers and tickers (`time.NewTicker`), periodic polling loops with context cancellation, rate limiting with token buckets.
- [Chapter 07: File Access and Basic Networking](../writings/go_in_practice_notes.md#chapter-07-file-access-and-basic-networking) — §7.1 Streaming I/O with `io.Reader` and `bufio.Reader` to parse incoming feed payloads efficiently.
- [Chapter 11: Working with External Services](../writings/go_in_practice_notes.md#chapter-11-working-with-external-services) — §11.1 Resilient HTTP client configuration (`http.Client` timeouts, transport connection pooling, custom headers for `ETag` and `If-Modified-Since`), §11.2 Graceful fault tolerance.

Adapter kit responsibilities (the *framework*, written once):

- Consume `assignment.events` for its `adapter_id` -> maintain a **source cache**.
- For each assigned source, run a **SourceRunner** goroutine that calls
  `Adapter.Fetch(ctx, source)` on its interval (with jitter).
- Publish `RawHeadline` -> `headline.raw` (batch + key by `source_id`).
- Publish heartbeats/status -> `adapter.status` every *N* s (state, #sources,
  last errors, version).
- Provide a uniform **error taxonomy** (`Transient`, `Permanent`, `RateLimited`,
  `AuthFailed`, `ParseError`) and map it to backoff behaviour.
- Per-source **circuit breaker** and **per-host token bucket**.
- Graceful drain on shutdown (stop pollers, flush publishes).

Adapter author responsibilities (the *plug-in point*):

```go
type Adapter interface {
    Type() string                                           // "rss"
    Validate(src Source) error                              // config check
    Fetch(ctx context.Context, src Source, st *State) (Result, error)
}

type Result struct {
    Items []RawHeadline
    State *State        // opaque cursor: etag, last-modified, last-seen ids
}
```

---

## 🎯 What You Will Learn
- **Core Objective:** A reusable **adapter kit** and one concrete adapter built on it.
- **Architectural Concepts:** Adapter pattern, template-method vs interface composition, schedulers,
HTTP conditional GET (ETag / Last-Modified), timeouts, retries with jitter,
circuit breaker, rate limiting per host, parsing untrusted input, SSRF defence,
bounded memory.

---

## 🛠️ Step-by-Step Implementation Guide

### Implementation Tasks
1. Write `internal/adapterkit/core` with the runner/scheduler and a fake adapter.
2. Write `rss-adapter` (use a battle-tested feed parser).
3. Implement conditional GET and an `external_id` strategy (`guid` else hash of URL).
4. Persist the adapter `State` (etag/cursor) in Redis so restarts don't re-emit
   everything (or accept duplicates and rely on dedupe - decide and document in an ADR).
5. Reject private IP ranges / non-http(s) schemes / huge bodies (>5 MB), cap
   redirects.
6. Tests with `httptest.Server` serving fixture feeds, including malformed XML,
   slow responses, 304s, 429 with `Retry-After`.

---

## 📦 Deliverables
`rss-adapter` running locally, polling a hard-coded assignment, emitting
`headline.raw`.

---

## 🤔 Reflection & Architectural Questions
What belongs in the *framework* vs the *adapter*? How would you design the kit
so a new adapter is < 150 lines of code?
