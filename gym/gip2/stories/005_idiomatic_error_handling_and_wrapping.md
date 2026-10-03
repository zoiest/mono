# Story 005: Idiomatic Error Handling & Error Wrapping

## User Story
**As a** software engineer debugging failed network queries,  
**I want** errors to clearly distinguish between missing symbols, network timeouts, rate limiting, and upstream server errors,  
**So that** calling layers can inspect error types with `errors.Is` and `errors.As` and take intelligent actions.

---

## 📖 Book Alignment
* **Book:** *Go in Practice, Second Edition*
* **Chapter:** Chapter 4: *Handling errors and panics*
* **Sections:**
  - 4.1 *Error handling (Nil best practices, Custom error types, Error variables)*
  - 4.2 *Wrapping errors (`fmt.Errorf("%w")`, `errors.Is`, `errors.As`)*
  - 4.3 *The panic system (Differentiating panics from errors, Recovering from panics)*

---

## 🎯 What You Will Learn
1. Defining package-level sentinel errors (`errors.New`).
2. Creating custom error types that implement the `error` interface.
3. Wrapping errors with `fmt.Errorf("...: %w", err)` to preserve the causal stack.
4. Using Go 1.13+ `errors.Is()` for value equality and `errors.As()` for type assertions.
5. Best practices on when to return an error versus when to panic.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Define Sentinel Errors
In `internal/domain/errors.go`:
```go
package domain

import (
	"errors"
	"fmt"
)

var (
	ErrSymbolNotFound = errors.New("symbol not found")
	ErrRateLimited    = errors.New("rate limit exceeded by upstream provider")
	ErrTimeout        = errors.New("request timed out")
	ErrInvalidSymbol  = errors.New("symbol format is invalid")
)
```

### 2. Define Custom Upstream Error Type
```go
type UpstreamError struct {
	Provider   string
	StatusCode int
	Message    string
	Err        error
}

func (e *UpstreamError) Error() string {
	return fmt.Sprintf("provider [%s] returned status %d: %s", e.Provider, e.StatusCode, e.Message)
}

func (e *UpstreamError) Unwrap() error {
	return e.Err
}
```

### 3. Handle Status Codes in Provider
In `internal/provider/yahoo/client.go`:
```go
switch resp.StatusCode {
case http.StatusOK:
	// proceed
case http.StatusNotFound:
	return nil, fmt.Errorf("%w: %s", domain.ErrSymbolNotFound, symbol)
case http.StatusTooManyRequests:
	return nil, fmt.Errorf("%w from yahoo: %s", domain.ErrRateLimited, symbol)
default:
	return nil, &domain.UpstreamError{
		Provider:   "yahoo",
		StatusCode: resp.StatusCode,
		Message:    resp.Status,
	}
}
```

---

## ✅ Acceptance Criteria
- [ ] Sentinel errors defined in `internal/domain/errors.go`.
- [ ] `UpstreamError` implements `Error()` and `Unwrap() error`.
- [ ] Tests verify that `errors.Is(err, domain.ErrSymbolNotFound)` returns `true` when a nonexistent ticker like `XYZNONEXISTENT` is queried.
- [ ] Tests verify that `errors.As(err, &upstreamErr)` extracts the HTTP status code.
