# Story 013: REST API with Enhanced ServeMux

## User Story
**As a** client application or web frontend,  
**I want** clean RESTful endpoints to query quotes, batch quotes, and historical metrics,  
**So that** I can retrieve JSON data using modern Go HTTP routing without heavy external routing dependencies.

---

## 📖 Book Alignment
* **Book:** *Go in Practice, Second Edition*
* **Chapters:**
  - Chapter 8: *Building an HTTP server* (8.1 Routing requests and accepting data: routing via HTTP verbs, routing path values; 8.2 Query parameters, JSON encoding)
  - Chapter 11: *Working with external services* (11.4 Versioning REST APIs)

---

## 🎯 What You Will Learn
1. Using the enhanced `http.ServeMux` features in modern Go (HTTP method matching like `"GET /..."` and path parameter wildcards like `"/stocks/{symbol}"`).
2. Extracting path parameters using `r.PathValue("symbol")`.
3. Reading URL query parameters with `r.URL.Query()`.
4. Writing helper functions for consistent JSON responses and HTTP status codes.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Build the HTTP Handlers
In `internal/server/handlers.go`:
```go
package server

import (
	"encoding/json"
	"errors"
	"net/http"
	"strings"

	"github.com/zoiest/mono/gym/gostock/internal/domain"
	"github.com/zoiest/mono/gym/gostock/internal/service"
)

type Server struct {
	aggregator *service.Aggregator
	mux        *http.ServeMux
}

func (s *Server) routes() {
	s.mux.HandleFunc("GET /api/v1/stocks/{symbol}", s.handleGetStock)
	s.mux.HandleFunc("GET /api/v1/stocks", s.handleBatchStocks)
}

func (s *Server) handleGetStock(w http.ResponseWriter, r *http.Request) {
	symbol := strings.ToUpper(r.PathValue("symbol"))
	if symbol == "" {
		s.respondJSON(w, http.StatusBadRequest, map[string]string{"error": "symbol required"})
		return
	}

	quote, err := s.aggregator.GetQuote(r.Context(), symbol)
	if err != nil {
		if errors.Is(err, domain.ErrSymbolNotFound) {
			s.respondJSON(w, http.StatusNotFound, map[string]string{"error": "symbol not found"})
			return
		}
		s.respondJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
		return
	}

	s.respondJSON(w, http.StatusOK, quote)
}

func (s *Server) respondJSON(w http.ResponseWriter, status int, payload any) {
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(payload)
}
```

---

## ✅ Acceptance Criteria
- [ ] Routes use modern `ServeMux` pattern matching (`GET /api/v1/...`).
- [ ] `GET /api/v1/stocks/AAPL` returns HTTP 200 with the quote JSON payload.
- [ ] Invalid symbols return HTTP 404 with structured error JSON.
- [ ] `GET /api/v1/stocks?symbols=AAPL,GOOG` returns array of quotes.
