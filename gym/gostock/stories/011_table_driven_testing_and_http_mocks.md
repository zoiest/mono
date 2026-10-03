# Story 011: Table-Driven Testing & HTTP Mocks

## User Story
**As a** quality-focused developer,  
**I want to** write comprehensive unit tests using table-driven test patterns and mock HTTP servers (`net/http/httptest`),  
**So that** all business logic, error paths, and response decoders are tested fast, deterministically, and without making real internet calls.

---

## 📖 Book Alignment
* **Book:** *Go in Practice, Second Edition*
* **Chapter:** Chapter 6: *Formatting, testing, debugging, and benchmarking*
* **Sections:**
  - 6.3 *Unit testing in Go (Creating a test suite with table-driven tests, Annotating tests with names, Checking test coverage with `go cover`)*

---

## 🎯 What You Will Learn
1. The canonical Go table-driven testing pattern using slices of anonymous structs.
2. Running isolated subtests with `t.Run(tt.name, func(t *testing.T) { ... })`.
3. Using `httptest.NewServer` to mock external API responses, HTTP headers, and error codes.
4. Analyzing test coverage with `go test -cover` and viewing HTML coverage profiles.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Build Table-Driven Tests with `httptest.Server`
In `internal/provider/yahoo/client_test.go`:
```go
package yahoo

import (
	"context"
	"errors"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	"github.com/zoiest/mono/gym/gostock/internal/domain"
)

func TestClient_FetchQuote(t *testing.T) {
	tests := []struct {
		name         string
		symbol       string
		serverStatus int
		serverResponse string
		wantPrice    float64
		wantErr      error
	}{
		{
			name:         "successful quote parse",
			symbol:       "AAPL",
			serverStatus: http.StatusOK,
			serverResponse: `{
				"chart": {
					"result": [{
						"meta": {
							"symbol": "AAPL",
							"regularMarketPrice": 185.50,
							"previousClose": 182.00
						}
					}]
				}
			}`,
			wantPrice: 185.50,
			wantErr:   nil,
		},
		{
			name:           "symbol not found",
			symbol:         "UNKNOWN",
			serverStatus:   http.StatusNotFound,
			serverResponse: `{"chart":{"error":{"code":"Not Found","description":"No data found"}}}`,
			wantErr:        domain.ErrSymbolNotFound,
		},
		{
			name:           "rate limit exceeded",
			symbol:         "MSFT",
			serverStatus:   http.StatusTooManyRequests,
			serverResponse: `Too Many Requests`,
			wantErr:        domain.ErrRateLimited,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				w.WriteHeader(tt.serverStatus)
				w.Write([]byte(tt.serverResponse))
			}))
			defer server.Close()

			client := New(2 * time.Second)
			client.baseURL = server.URL // Override for test

			quote, err := client.FetchQuote(context.Background(), tt.symbol)

			if tt.wantErr != nil {
				if !errors.Is(err, tt.wantErr) {
					t.Fatalf("expected error wrapping %v, got %v", tt.wantErr, err)
				}
				return
			}

			if err != nil {
				t.Fatalf("unexpected error: %v", err)
			}
			if quote.Price != tt.wantPrice {
				t.Errorf("got price %f, want %f", quote.Price, tt.wantPrice)
			}
		})
	}
}
```

---

## ✅ Acceptance Criteria
- [ ] Table-driven tests implemented for domain math, config loading, and Yahoo client.
- [ ] Tests run without requiring an active internet connection.
- [ ] Running `go test -cover ./...` demonstrates > 80% coverage across business packages.
