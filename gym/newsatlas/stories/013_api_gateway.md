# Story 013: API Gateway

## User Story
**As a** edge infrastructure engineer,  
**I want to** build an API gateway with JWT/OIDC validation, path-based reverse proxying, and IP rate limiting,  
**So that** external clients have a single, secure front door protecting internal microservices.

---

## 📖 Book Alignment
📖 **Go in Practice (2nd Ed) Alignment:**
- [Chapter 08: Building an HTTP Server](../writings/go_in_practice_notes.md#chapter-08-building-an-http-server) — §8.2 Reverse proxy construction with `net/http/httputil.ReverseProxy`, §8.3 Composable middleware pipelines (JWT authentication, rate limiting, request tracing, CORS, security headers).
- [Chapter 12: Cloud-Ready Applications](../writings/go_in_practice_notes.md#chapter-12-cloud-ready-applications-and-communications) — §12.3 API Gateway edge patterns and TLS termination.
- [The Ten Cardinal Rules](../writings/go_in_practice_notes.md#the-ten-cardinal-rules-of-idiomatic-go) — Rule 7: *Design composable HTTP middleware* (`func(http.Handler) http.Handler`).

---

## 🎯 What You Will Learn
- **Core Objective:** The only door into the system: authenticated, authorised, documented, and fast.
- **Architectural Concepts:** OpenAPI-first design, code generation, middleware chains (request-id, logging,
CORS, rate limit, auth, recovery), JWT validation (JWKS caching), RBAC,
REST<->gRPC mapping, pagination, problem+json errors, SSE, aggregation,
timeouts and deadline propagation, mock clients for tests.

---

## 🛠️ Step-by-Step Implementation Guide

### Implementation Tasks
1. Write `api/openapi.yaml` first. Generate server stubs + TS client.
2. Handler packages per area: `sources/`, `adapters/`, `headlines/`, `map/`,
   `views/`, `bookmarks/`, `alerts/`, and (added later) `instruments/`,
   `quotes/`, `watchlists/`, `moves/`, `briefing/`. Each has `handler.go`,
   `mapper.go`, `handler_test.go`.
3. **Mappers** convert REST DTO <-> gRPC messages (table-driven tests; add a
   "parity" test that every field is mapped).
4. Auth middleware: verify JWT via JWKS (cache keys, handle rotation); extract
   user id + roles; permission map `{route -> required permission}`.
5. gRPC client wrappers behind **interfaces** (so handlers are tested with
   mocks, not real services). Apply per-call deadlines & retries only for
   idempotent calls.
6. **SSE endpoint** `/api/v1/stream`: each gateway instance has a *broadcast*
   consumer on `story.events`, `alert.raised` (and later `quote.live`,
   `market.event`, `insight.created`); fan-out to connected clients; support
   `Last-Event-ID` resume (short ring buffer), heartbeat comments, per-client
   filter (bbox/category/**instrument ids**) and slow-client eviction.
   **Quote traffic is high-volume**: coalesce (keep only the latest quote per
   instrument per client per 250-500 ms) instead of queueing every tick - decide
   and test what "slow client" means for a price stream vs a news stream.
7. Rate limiting per user/IP; request size limits; CORS allowlist.
8. Aggregation examples with `errgroup` and partial-failure semantics:
   - `/headlines/{id}` = headline (story-service) + bookmark flag (ui-backend).
   - `/instruments/{id}/overview` = snapshot (market-service) + latest linked
     headlines (story-service) + recent moves (insight-service) + watchlist
     membership (ui-backend). If `insight-service` is down, the page still
     renders, flagged `X-Partial: true`.

---

## 📦 Deliverables
Swagger UI served from the gateway in dev; Postman/Bruno collection in repo.

---

## 🧪 Deep-Dive Exercises
Add ETag/If-None-Match to read endpoints; add an OpenAPI-vs-implementation
contract test (e.g. `schemathesis`).

---

## 🤔 Reflection & Architectural Questions
What is the cost of letting the browser talk to backends directly? Where
should *business* validation live: gateway or service?
