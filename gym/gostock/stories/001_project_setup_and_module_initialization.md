# Story 001: Project Setup & Module Initialization

## User Story
**As a** Go developer,  
**I want to** initialize a Go module and configure the project workspace,  
**So that** I have a reproducible dependency workspace adhering to standard Go directory conventions.

---

## 📖 Book Alignment
* **Book:** *Go in Practice, Second Edition*
* **Chapter:** Chapter 1: *Getting started with Go*
* **Sections:**
  - 1.2 *Noteworthy aspects of Go (Go the toolchain: More than a language)*
  - 1.4 *Getting up and running in Go (Working with Git, exploring the workspace, working with environment variables)*
  - 1.5 *Hello, Go*

---

## 🎯 What You Will Learn
1. How Go manages dependencies with `go.mod` and `go.sum`.
2. The standard Go directory structure (`cmd/` for entrypoints, `internal/` for private application packages).
3. Using the core Go toolchain commands: `go mod init`, `go run`, `go build`, `go vet`, and `go fmt`.
4. How Go enforces package boundary encapsulation with the `internal/` directory.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Initialize the Module
Create the module with a clear namespace path:
```bash
go mod init github.com/zoiest/mono/gym/gostock
```

### 2. Scaffold the Project Directory Layout
Create the recommended directories:
```bash
mkdir -p cmd/gostock-cli cmd/gostock-server internal/domain internal/config internal/provider
```

### 3. Create the Initial CLI Entrypoint
Create `cmd/gostock-cli/main.go`:
```go
package main

import (
	"fmt"
)

func main() {
	fmt.Println("gostock: Financial data aggregator v0.1.0")
}
```

### 4. Verify Toolchain Formatting and Vetting
Run standard Go hygiene tools:
```bash
go fmt ./...
go vet ./...
go run ./cmd/gostock-cli
```

---

## ✅ Acceptance Criteria
- [ ] `go.mod` is generated at the project root targeting Go 1.22+.
- [ ] The `cmd/gostock-cli` directory contains a functioning `main.go`.
- [ ] Running `go run ./cmd/gostock-cli` prints the version message cleanly.
- [ ] `go vet ./...` reports zero issues.
