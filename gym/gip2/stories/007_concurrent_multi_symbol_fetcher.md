# Story 007: Concurrent Multi-Symbol Fetcher

## User Story
**As a** portfolio investor,  
**I want to** query quotes for a batch of 20+ stock tickers simultaneously,  
**So that** my query response time is bounded by the slowest single request rather than the sum of all sequential requests.

---

## 📖 Book Alignment
* **Book:** *Go in Practice, Second Edition*
* **Chapter:** Chapter 5: *Concurrency in Go*
* **Sections:**
  - 5.1 *Understanding Go’s concurrency model (CSP)*
  - 5.2 *Working with goroutines (Waiting for goroutines with `sync.WaitGroup`, Locking with a mutex)*

---

## 🎯 What You Will Learn
1. Spawning goroutines with the `go` keyword.
2. Avoiding closure variable capture bugs in loops.
3. Coordinating multiple goroutines using `sync.WaitGroup`.
4. Safely aggregating concurrent results using a mutex or result channel.
5. Detecting and debugging race conditions with `go test -race` and `go run -race`.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Concurrent Fetch using `sync.WaitGroup`
In `internal/service/fetcher.go`:
```go
package service

import (
	"context"
	"sync"

	"github.com/tofunth/gostock/internal/domain"
	"github.com/tofunth/gostock/internal/provider"
)

type BatchResult struct {
	Symbol string
	Quote  *domain.Quote
	Err    error
}

func FetchBatch(ctx context.Context, p provider.StockProvider, symbols []string) []BatchResult {
	var wg sync.WaitGroup
	results := make([]BatchResult, len(symbols))

	for i, sym := range symbols {
		wg.Add(1)
		go func(idx int, s string) {
			defer wg.Done()
			q, err := p.FetchQuote(ctx, s)
			results[idx] = BatchResult{
				Symbol: s,
				Quote:  q,
				Err:    err,
			}
		}(i, sym)
	}

	wg.Wait()
	return results
}
```

### 2. Connect to CLI
In `cmd/gostock-cli/main.go`:
```bash
# Allow syntax like:
gostock-cli fetch AAPL MSFT GOOG AMZN NVDA
```

---

## ✅ Acceptance Criteria
- [ ] Querying 10 symbols completes concurrently.
- [ ] Running `go test -race ./internal/service/...` passes with zero race warnings.
- [ ] Partial failures (e.g. 1 invalid symbol out of 10) do not abort the entire batch; valid quotes are still returned.
