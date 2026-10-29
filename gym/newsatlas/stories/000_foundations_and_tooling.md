# Story 000: Foundations and Tooling

## User Story
**As a** platform engineer,  
**I want to** establish a clean monorepo workspace with Docker Compose, Taskfile, and strict CI linters,  
**So that** all subsequent microservices build reliably from a unified, reproducible foundation with zero manual environment configuration.

---

## 📖 Book Alignment
📖 **Go in Practice (2nd Ed) Alignment:**
- [Chapter 01: Getting Started with Go](../writings/go_in_practice_notes.md#chapter-01-getting-started-with-go) — §1.2 Understanding the Go toolchain (`go mod`, `go work`), §1.4 Workspace layout and GOPATH/module boundary, §1.5 Code hygiene (`go fmt`, `go vet`, `golangci-lint`).
- [Chapter 06: Formatting, Testing, Debugging, and Benchmarking](../writings/go_in_practice_notes.md#chapter-06-formatting-testing-debugging-and-benchmarking) — §6.1 Code formatting conventions and vetting.
- [The Ten Cardinal Rules](../writings/go_in_practice_notes.md#the-ten-cardinal-rules-of-idiomatic-go) — Rule 1: *Let the compiler & toolchain enforce boundaries* (monorepo root `go.mod` with strict `internal/` package encapsulation).

---

## 🎯 What You Will Learn
- **Core Objective:** A reproducible dev environment and an empty-but-green pipeline.
- **Architectural Concepts:** Go workspaces/modules, `internal/` visibility rule, Docker Compose, Taskfile,
linting (`golangci-lint`), pre-commit hooks, conventional commits.

---

## 🛠️ Step-by-Step Implementation Guide

### Implementation Tasks
1. Create the repo, `go mod init example.com/newsatlas`, add `Taskfile.yml`.
2. Compose file with `postgres (postgis)`, `redis`, optional `keycloak`.
3. Add `golangci-lint`, `buf`, `gofumpt` to a `tools.go` or `mise`/`asdf` file.
4. GitHub Actions: lint + `go test ./...` + `go build ./...`.
5. Write ADR-0001: "Monorepo, one Go module".

---

## 📦 Deliverables
`task up` starts infra; `task test` is green with a trivial test.

---

## ✅ Acceptance Criteria ("Done When")
- [ ] A fresh clone reaches green CI with **zero manual steps** other than
- [ ] `task up`.

---

## 🧪 Deep-Dive Exercises
Prove the `internal/` rule: create a second module that tries to import
`internal/common/boot` and observe the compiler error. (You will rely on this
property in Phase 11.)

---

## 🤔 Reflection & Architectural Questions
Why one module instead of one module per service? What do you give up?
