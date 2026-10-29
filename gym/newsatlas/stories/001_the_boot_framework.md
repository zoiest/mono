# Story 001: The Boot Framework

## User Story
**As a** backend engineer,  
**I want to** implement a unified boot framework with deterministic startup order, health probes, and graceful shutdown,  
**So that** every service initializes and terminates predictably under Kubernetes with zero orphaned tasks or race conditions.

---

## 📖 Book Alignment
📖 **Go in Practice (2nd Ed) Alignment:**
- [Chapter 02: Building CLI Applications](../writings/go_in_practice_notes.md#chapter-02-building-cli-applications) — §2.3 Handling OS signals (`os/signal`, `syscall.SIGTERM`, `SIGINT`), coordinated process exits, and configuration cascades.
- [Chapter 05: Concurrency in Go](../writings/go_in_practice_notes.md#chapter-05-concurrency-in-go) — §5.1 Goroutine lifecycle management, §5.2 Synchronization with `sync.WaitGroup`, `errgroup`, and `context.Context` cancellation hierarchies.
- [Chapter 12: Cloud-Ready Applications](../writings/go_in_practice_notes.md#chapter-12-cloud-ready-applications-and-communications) — §12.4 Cloud health probes (standardized `/livez`, `/readyz`, and `/metrics` endpoints), graceful drain before SIGKILL.
- [The Ten Cardinal Rules](../writings/go_in_practice_notes.md#the-ten-cardinal-rules-of-idiomatic-go) — Rule 4: *Always propagate Context & handle OS signals* (every background worker accepts a `context.Context` and cancels cleanly within the exit deadline).

---

## 🎯 What You Will Learn
- **Core Objective:** Every service starts, becomes ready, and stops **the same way**.
- **Architectural Concepts:** `context`, signals, `sync.WaitGroup`, `errgroup`, init-order, readiness vs
liveness, K8s probes, graceful shutdown, Go `init()` registration pattern.

---

## 🛠️ Step-by-Step Implementation Guide

### Architecture & Design Considerations
Design (implement it yourself - see skeleton in the appendix):

- `main()` contains **only** `boot.StartApp()`.
- Packages register what they need in their own `init()`:
  - **Init methods** (sync, priority-ordered): load config, open DB pool.
  - **Init jobs** (parallel, may wait for dependencies): wait for DB, wait for bus.
  - **Init job chains** (sequential inside, parallel between chains).
  - **Background tasks** (HTTP server, consumers). Some start *early* (HTTP
    server so probes work) and some *after* init jobs.
  - **Shutdown methods** run in reverse order.
- Startup sequence: register readiness probe `DOWN` -> init methods -> early
  background tasks -> init jobs -> remaining tasks -> readiness `UP`.
- On `SIGTERM` during init: log once, exit non-zero (so the orchestrator
  retries). On `SIGTERM` after startup: cancel the app context, wait up to
  `BOOT_MAX_EXIT_SECONDS`.
- Expose `/livez`, `/readyz`, `/metrics` automatically.

### Implementation Tasks
1. Implement `internal/common/boot` with unit tests for ordering and shutdown.
2. Implement `internal/common/health` (registry of named probes, lazy probes).
3. Implement `internal/common/config` (env + optional file, typed, validated).
4. Implement `internal/common/logger` (slog JSON, correlation id, secret redaction).
5. Build `tools/new-service` that generates the standard per-service layout with
   `*_init.go` files that register with boot.

---

## 📦 Deliverables
A `hello-service` that starts, serves `/readyz`, and stops cleanly in < 3 s.

---

## 🤔 Reflection & Architectural Questions
Why is it valuable that `main.go` is identical in every service? What would
break if two packages registered init methods with the same priority and one
depended on the other?
