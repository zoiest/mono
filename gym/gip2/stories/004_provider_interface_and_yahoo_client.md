# Story 004: Provider Interface & Yahoo Finance Client

## User Story
**As an** application service,  
**I want to** define a unified `StockProvider` interface and implement a Yahoo Finance client,  
**So that** the application can consume real-world stock quotes and historical OHLC data with proper HTTP client timeouts.

---

## 📖 Book Alignment
* **Book:** *Go in Practice, Second Edition*
* **Chapters:**
  - Chapter 3: *Structs, interfaces, and generics* (3.3 Extending functionality with interfaces)
  - Chapter 11: *Working with external services* (11.1 Consuming REST APIs as a full-featured client, 11.3 Parsing and mapping JSON)

---

## 🎯 What You Will Learn
1. Designing focused Go interfaces (duck typing / implicit interface satisfaction).
2. Configuring production-grade `http.Client` (avoiding `http.DefaultClient` pitfalls with missing timeouts).
3. Using `context.Context` with `http.NewRequestWithContext` for deadline and cancellation propagation.
4. Parsing complex/nested JSON responses into clean domain structs.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Define the Provider Interface
In `internal/provider/provider.go`:
```go
package provider

import (
	"context"
	"github.com/tofunth/gostock/internal/domain"
)

type StockProvider interface {
	Name() string
	FetchQuote(ctx context.Context, symbol string) (*domain.Quote, error)
	FetchHistorical(ctx context.Context, symbol string, interval string) ([]domain.HistoricalPrice, error)
}
```

### 2. Implement the Yahoo Client
In `internal/provider/yahoo/client.go`:
```go
package yahoo

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"time"

	"github.com/tofunth/gostock/internal/domain"
)

type Client struct {
	httpClient *http.Client
	baseURL    string
}

func New(timeout time.Duration) *Client {
	return &Client{
		httpClient: &http.Client{
			Timeout: timeout,
		},
		baseURL: "https://query1.finance.yahoo.com/v8/finance/chart",
	}
}

func (c *Client) Name() string {
	return "yahoo"
}

func (c *Client) FetchQuote(ctx context.Context, symbol string) (*domain.Quote, error) {
	url := fmt.Sprintf("%s/%s?interval=1d&range=1d", c.baseURL, symbol)
	req, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
	if err != nil {
		return nil, fmt.Errorf("creating request: %w", err)
	}

	req.Header.Set("User-Agent", "Mozilla/5.0 (compatible; gostock/1.0)")

	resp, err := c.httpClient.Do(req)
	if err != nil {
		return nil, fmt.Errorf("executing yahoo request: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("yahoo returned status %d", resp.StatusCode)
	}

	var payload YahooChartResponse
	if err := json.NewDecoder(resp.Body).Decode(&payload); err != nil {
		return nil, fmt.Errorf("decoding response: %w", err)
	}

	return payload.ToQuote(symbol)
}
```

---

## ✅ Acceptance Criteria
- [ ] `StockProvider` interface is defined in `internal/provider/provider.go`.
- [ ] Yahoo client satisfies the `StockProvider` interface.
- [ ] HTTP requests pass `ctx` and include customized User-Agent headers.
- [ ] `FetchQuote` maps remote Yahoo JSON into `domain.Quote`.
