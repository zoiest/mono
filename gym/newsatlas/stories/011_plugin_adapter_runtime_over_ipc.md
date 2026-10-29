# Story 011: Plug-in Adapter Runtime (IPC)

## User Story
**As a** ecosystem architect,  
**I want to** build an out-of-tree plug-in runtime over Unix domain sockets with Protobuf / gRPC contracts,  
**So that** external developers can contribute new adapters in any language without modifying core repository internals.

---

## 📖 Book Alignment
📖 **Go in Practice (2nd Ed) Alignment:**
- [Chapter 07: File Access and Basic Networking](../writings/go_in_practice_notes.md#chapter-07-file-access-and-basic-networking) — §7.3 Low-latency IPC via Unix domain sockets (`net.Listen("unix", ...)`).
- [Chapter 13: Reflection, Code Generation, and Advanced Go](../writings/go_in_practice_notes.md#chapter-13-reflection-code-generation-and-advanced-go) — §13.3 Dynamic process loading, code generation with `buf`/`protoc-gen-go`, plugin lifecycle negotiation.
- [The Ten Cardinal Rules](../writings/go_in_practice_notes.md#the-ten-cardinal-rules-of-idiomatic-go) — Rule 1: *Let the compiler & toolchain enforce boundaries* (out-of-tree plugins cannot import internal packages).

---

## 🎯 What You Will Learn
- **Core Objective:** Let someone else write an adapter in any language, in a separate repo, with no
access to your internals.
- **Architectural Concepts:** gRPC over Unix domain sockets, process supervision, sidecar pattern (shared
`emptyDir` volume in Kubernetes), capability-based security, API versioning,
contract-first design, `internal/` import rule as an architectural fence.

---

## 🛠️ Step-by-Step Implementation Guide

### Implementation Tasks
1. Define `plugin.proto` (section 7.5). Keep the plug-in free of any bus/DB code.
2. `adapter-runtime`: runs the standard adapter kit, but its `Fetch` calls the
   plug-in over a Unix socket. Supports multiple plug-ins.
3. Host callbacks (`HttpGet`, `Log`): the host does all network I/O (applies
   SSRF protections, timeouts, size limits, adds credentials from refs).
4. `plugins/example-adapter/` - **separate `go.mod`** with a module path that does
   **not** sit under the main module path (so the `internal/` rule *physically*
   prevents imports). Add a CI check that greps the plug-in dir for forbidden
   import paths.
5. A standalone **conformance CLI** that a plug-in author can run against their
   binary without the rest of your system.
6. Export script: produces a tarball with `proto/`, the example plug-in, and a
   `getting-started.md` - nothing else.

---

## 📦 Deliverables
A plug-in written by you in Go, and a second tiny one in Python (use the same
proto) to prove language independence.

---

## 🧪 Deep-Dive Exercises
Add a version negotiation (`api_version` in `Describe`) and reject
incompatible plug-ins with a clear error.

---

## 🤔 Reflection & Architectural Questions
What would you give up if plug-ins could open their own sockets? How would you
sandbox further (seccomp, gVisor, WASM)?
