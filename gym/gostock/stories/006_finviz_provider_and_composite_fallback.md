# Story 006: Finviz Provider & Composite Fallback Engine

## User Story
**As a** stock trader using `gostock`,  
**I want to** fetch stock data from Finviz or fall back to Finviz automatically if Yahoo Finance is rate-limited or unavailable,  
**So that** my application exhibits high availability and resilience across independent financial sources.

---

## 📖 Book Alignment
* **Book:** *Go in Practice, Second Edition*
* **Chapters:**
  - Chapter 3: *Structs, interfaces, and generics* (3.3 Extending functionality with interfaces, composition over inheritance)
  - Chapter 11: *Working with external services* (11.2 When faults happen, passing and handling errors over HTTP)
  - Chapter 12: *Cloud-ready applications and communications* (12.2 Microservices and high availability)

---

## 🎯 What You Will Learn
1. Implementing multiple concrete types satisfying the same interface.
2. Web scraping / HTML extraction or parsing Finviz quote endpoints.
3. Implementing the Composite / Fallback pattern in Go using composition.
4. Selective error inspection to decide when to failover vs when to fail immediately (e.g. don't failover if symbol is invalid; do failover if rate-limited or 5xx).

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Implement Finviz Provider
In `internal/provider/finviz/client.go`:
```go
package finviz

import (
	"context"
	"fmt"
	"net/http"
	"time"

	"github.com/zoiest/mono/gym/gostock/internal/domain"
)

type Client struct {
	httpClient *http.Client
	baseURL    string
}

func New(timeout time.Duration) *Client {
	return &Client{
		httpClient: &http.Client{Timeout: timeout},
		baseURL:    "https://finviz.com/quote.ashx",
	}
}

func (c *Client) Name() string { return "finviz" }

func (c *Client) FetchQuote(ctx context.Context, symbol string) (*domain.Quote, error) {
	// Query Finviz and extract metrics (e.g. Price, Previous Close, Volume)
	// Return mapped *domain.Quote with Provider: domain.ProviderFinviz
    ...
}
```

### 2. Implement the Composite Fallback Provider
In `internal/provider/fallback.go`:
```go
type CompositeProvider struct {
	primary   StockProvider
	secondary StockProvider
}

func NewComposite(primary, secondary StockProvider) *CompositeProvider {
	return &CompositeProvider{
		primary:   primary,
		secondary: secondary,
	}
}

func (cp *CompositeProvider) Name() string {
	return fmt.Sprintf("%s-with-%s-fallback", cp.primary.Name(), cp.secondary.Name())
}

func (cp *CompositeProvider) FetchQuote(ctx context.Context, symbol string) (*domain.Quote, error) {
	quote, err := cp.primary.FetchQuote(ctx, symbol)
	if err == nil {
		return quote, nil
	}

	// If symbol simply does not exist, do not waste secondary provider budget
	if errors.Is(err, domain.ErrSymbolNotFound) {
		return nil, err
	}

	// Otherwise, fallback to secondary
	return cp.secondary.FetchQuote(ctx, symbol)
}
```

---

## ✅ Acceptance Criteria
- [ ] `finviz.Client` satisfies `StockProvider`.
- [ ] `CompositeProvider` satisfies `StockProvider` using Go composition.
- [ ] If primary succeeds, secondary is never invoked.
- [ ] If primary returns `ErrRateLimited` or a network timeout, secondary is automatically queried.
- [ ] If primary returns `ErrSymbolNotFound`, secondary is skipped.
