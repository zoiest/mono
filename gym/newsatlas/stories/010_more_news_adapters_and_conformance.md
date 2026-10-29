# Story 010: More News Adapters & Conformance Suite

## User Story
**As a** QA / platform engineer,  
**I want to** expand news coverage with REST API and bulk-file adapters and build an automated adapter conformance test suite,  
**So that** any new adapter implementation can be certified in hours with zero goroutine leaks.

---

## 📖 Book Alignment
📖 **Go in Practice (2nd Ed) Alignment:**
- [Chapter 06: Formatting, Testing, Debugging, and Benchmarking](../writings/go_in_practice_notes.md#chapter-06-formatting-testing-debugging-and-benchmarking) — §6.3 Table-driven conformance suites, testing interfaces against mocks, detecting goroutine leaks using `goleak`.
- [Chapter 07: File Access and Basic Networking](../writings/go_in_practice_notes.md#chapter-07-file-access-and-basic-networking) — §7.1 Decompressing and streaming large archive payloads (`compress/gzip`, `archive/tar`), `io.Copy` buffer recycling.
- [Chapter 11: Working with External Services](../writings/go_in_practice_notes.md#chapter-11-working-with-external-services) — §11.3 Testing external network dependencies using `net/http/httptest` mock servers.

---

## 🎯 What You Will Learn
- **Core Objective:** Prove the adapter kit is genuinely reusable, and test adapters uniformly.
- **Architectural Concepts:** Pagination cursors, JSON APIs, bulk file feeds (CSV/TSV zips), time-window
polling, deterministic simulators, contract testing.

---

## 🛠️ Step-by-Step Implementation Guide

### Implementation Tasks
1. `api-adapter`: JSON API source (e.g. top stories list + item lookup). Practice
   bounded concurrency for N+1 calls.
2. `bulk-adapter`: pulls a periodic bulk event file (feed that includes
   coordinates), streams & parses without loading it all in memory.
3. `replay-adapter` (news mode; the market mode was added in Phase 8): a
   **simulator** - reads a fixture file and emits headlines at a configurable
   rate, with knobs for duplicates, bursts, malformed items, late arrivals. You
   will use this for load, chaos and UI demos. Add a **shared scenario file**
   that drives news *and* quotes on one timeline (e.g. "at 10:02 a company
   headline appears, at 10:04 the price drops 3%") - this is the test bed for
   Phase 16.
4. **Conformance suite** (`internal/adapterkit/conformance`): a Go test package
   any adapter can import and run: `Validate` rejects bad input, `Fetch`
   respects `ctx` cancel, state cursors advance, errors are typed, no goroutine
   leaks (`goleak`). Run it against the Phase 4 and Phase 8 adapters as well
   (news *and* market, polling *and* streaming).

---

## 📦 Deliverables
Four adapters, all passing the same suite.

---

## ✅ Acceptance Criteria ("Done When")
- [ ] Adding a *new* adapter type takes you < 2 hours and < 200 LOC.

---

## 🧪 Deep-Dive Exercises
Make the replay adapter deterministic with a seed so UI tests are repeatable.

---

## 🤔 Reflection & Architectural Questions
Which parts of the kit felt awkward once you wrote the 2nd and 3rd adapter?
Refactor the kit now (ADR it).
