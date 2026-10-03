# Story 012: Fuzz Testing & Allocation Benchmarking

## User Story
**As a** systems performance engineer,  
**I want to** fuzz-test JSON and HTML response parsing and benchmark cache lookups,  
**So that** unpredictable remote responses never crash the service and high-frequency cache reads achieve zero heap allocations.

---

## 📖 Book Alignment
* **Book:** *Go in Practice, Second Edition*
* **Chapter:** Chapter 6: *Formatting, testing, debugging, and benchmarking*
* **Sections:**
  - 6.3 *Fuzzing test input (`testing.F`, `f.Add`, `f.Fuzz`)*
  - 6.4 *Benchmarking and performance tuning (`testing.B`, `b.ReportAllocs()`)*

---

## 🎯 What You Will Learn
1. Setting up Go native fuzz tests (`testing.F`) to test resilience against corrupted payloads.
2. Writing benchmark functions (`func BenchmarkX(b *testing.B)`).
3. Analyzing memory allocations with `b.ReportAllocs()` and `-benchmem`.
4. Using compiler escape analysis (`go build -gcflags="-m"`) to eliminate unnecessary heap escapes.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Fuzz Testing the Response Parser
In `internal/provider/yahoo/parser_test.go`:
```go
package yahoo

import (
	"testing"
)

func FuzzParseResponse(f *testing.F) {
	// Seed corpus with valid sample JSON
	f.Add([]byte(`{"chart":{"result":[{"meta":{"symbol":"AAPL","regularMarketPrice":150.0}}]}}`))
	f.Add([]byte(`{"chart":{"error":{"code":"Not Found"}}}`))
	f.Add([]byte(`{}`))
	f.Add([]byte(`null`))

	f.Fuzz(func(t *testing.T, payload []byte) {
		// The parser must gracefully handle malformed data without panicking
		_, _ = ParseChartJSON(payload, "AAPL")
	})
}
```

### 2. Benchmarking Cache Lookups
In `internal/cache/cache_test.go`:
```go
package cache

import (
	"testing"
	"time"
)

func BenchmarkCache_Get(b *testing.B) {
	c := New[string, float64](5 * time.Minute)
	c.Set("AAPL", 185.50)

	b.ResetTimer()
	b.ReportAllocs()

	b.RunParallel(func(pb *testing.PB) {
		for pb.Next() {
			val, found := c.Get("AAPL")
			if !found || val != 185.50 {
				b.Fatal("unexpected cache miss")
			}
		}
	})
}
```

---

## ✅ Acceptance Criteria
- [ ] Running `go test -fuzz=FuzzParseResponse -fuzztime=10s ./...` produces no crashes or panics.
- [ ] Running `go test -bench=BenchmarkCache -benchmem ./...` shows 0 allocs/op during cache read hits.
