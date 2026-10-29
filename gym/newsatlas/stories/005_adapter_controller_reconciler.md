# Story 005: Adapter Controller (Reconciler)

## User Story
**As a** distributed systems engineer,  
**I want to** implement a reconciler-based adapter controller with leader election, leases, and heartbeats,  
**So that** every active news source is polled by exactly one adapter worker with automatic failover during worker crashes.

---

## 📖 Book Alignment
📖 **Go in Practice (2nd Ed) Alignment:**
- [Chapter 04: Handling Errors and Panics](../writings/go_in_practice_notes.md#chapter-04-handling-errors-and-panics) — §4.3 Safe worker recovery via `recover()` in worker supervisors, converting panics into logged errors to keep the controller running.
- [Chapter 05: Concurrency in Go](../writings/go_in_practice_notes.md#chapter-05-concurrency-in-go) — §5.2 Coordination loops with `select`, channels, and mutexes (`sync.Mutex`, `sync.RWMutex`) guarding assignment state, non-blocking channel heartbeats.
- [Chapter 06: Formatting, Testing, Debugging, and Benchmarking](../writings/go_in_practice_notes.md#chapter-06-formatting-testing-debugging-and-benchmarking) — §6.4 Table-driven tests simulating split-brain, crashed workers, and network partition recovery.

---

## 🎯 What You Will Learn
- **Core Objective:** Automatic assignment of sources to adapter instances, with failure handling.
- **Architectural Concepts:** Controller/reconciler loop, desired vs actual state, level-triggered vs
edge-triggered design, heartbeats and failure detection, leases, distributed
locks, fencing tokens/epochs, rebalancing, consistent hashing / rendezvous
hashing, backoff on reconcile errors.

---

## 🛠️ Step-by-Step Implementation Guide

### Implementation Tasks
1. Maintain in-memory caches: `sources` (from `source.events` + initial gRPC
   list), `adapters` (from `adapter.status`), `assignments`.
2. Reconcile loop (every few seconds *and* on events): compute desired
   assignments (rendezvous hashing over live adapters of matching `type`),
   diff against actual, publish `assignment.events` for changes only.
3. Failure detection: adapter missing `K` heartbeats -> `dead`; its sources get
   reassigned.
4. Use a Redis **lease lock** so only one controller replica acts (leader
   election); include an **epoch** in every assignment so adapters ignore stale
   commands.
5. `ControllerService` gRPC for the admin UI (`ListAdapters`, `ListAssignments`).
6. Handle: new adapter joins (minimal movement), adapter leaves, source
   disabled/deleted, type mismatch (no adapter for type -> `Unassigned` with reason).

---

## 📦 Deliverables
Run 3 `rss-adapter` containers; sources spread across them.

---

## 🧪 Deep-Dive Exercises
Add weights/capacity per adapter and a "drain" admin command.

---

## 🤔 Reflection & Architectural Questions
What happens in a network partition where the old leader still believes it
holds the lock? How do fencing tokens help?
