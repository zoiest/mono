# Story 008: Worker Pool with Rate Limiting

## User Story
**As a** system architect,  
**I want to** bound the maximum number of concurrent outbound requests and throttle outgoing traffic with a token bucket,  
**So that** external financial APIs are never overwhelmed and the application operates predictably under heavy load.

---

## 📖 Book Alignment
* **Book:** *Go in Practice, Second Edition*
* **Chapter:** Chapter 5: *Concurrency in Go*
* **Sections:**
  - 5.3 *Working with channels (Using channels, Closing channels, Locking with buffered channels)*
  - 5.3 *Select statements, timeouts, and channel directionality*

---

## 🎯 What You Will Learn
1. Creating bounded worker pools using buffered job and result channels.
2. Channel ownership idioms: only the sender should close a channel.
3. Implementing rate limiting using `time.Ticker` or a token bucket pattern.
4. Using `select` to handle timeouts, context cancellation, and channel operations simultaneously.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Build the Worker Pool
In `internal/service/pool.go`:
```go
package service

import (
	"context"
	"time"

	"github.com/tofunth/gostock/internal/domain"
	"github.com/tofunth/gostock/internal/provider"
)

type WorkerPool struct {
	provider   provider.StockProvider
	numWorkers int
	limiter    *time.Ticker
}

func NewWorkerPool(p provider.StockProvider, numWorkers int, rps int) *WorkerPool {
	interval := time.Second / time.Duration(rps)
	return &WorkerPool{
		provider:   p,
		numWorkers: numWorkers,
		limiter:    time.NewTicker(interval),
	}
}

func (wp *WorkerPool) FetchAll(ctx context.Context, symbols []string) ([]BatchResult, error) {
	jobs := make(chan string, len(symbols))
	results := make(chan BatchResult, len(symbols))

	// Launch fixed number of workers
	for w := 0; w < wp.numWorkers; w++ {
		go func() {
			for sym := range jobs {
				// Throttle by waiting for rate limiter tick
				select {
				case <-ctx.Done():
					results <- BatchResult{Symbol: sym, Err: ctx.Err()}
					return
				case <-wp.limiter.C:
				}

				q, err := wp.provider.FetchQuote(ctx, sym)
				results <- BatchResult{Symbol: sym, Quote: q, Err: err}
			}
		}()
	}

	// Send jobs
	for _, s := range symbols {
		jobs <- s
	}
	close(jobs)

	// Collect results
	out := make([]BatchResult, 0, len(symbols))
	for i := 0; i < len(symbols); i++ {
		select {
		case <-ctx.Done():
			return out, ctx.Err()
		case r := <-results:
			out = append(out, r)
		}
	}

	return out, nil
}
```

---

## ✅ Acceptance Criteria
- [ ] Concurrency is strictly capped at `numWorkers` (e.g. 5 concurrent requests max).
- [ ] Requests are metered according to the configured requests-per-second (RPS).
- [ ] Canceling `ctx` halts pending workers without leaking goroutines.
