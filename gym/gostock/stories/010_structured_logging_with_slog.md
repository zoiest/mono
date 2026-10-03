# Story 010: Structured Logging with slog

## User Story
**As a** DevOps engineer and backend developer,  
**I want** the application to emit structured logs with contextual attributes using the standard `log/slog` package,  
**So that** log streams can be parsed by aggregation tools (e.g. Datadog, Grafana Loki) and searched by ticker symbol, provider, or latency.

---

## 📖 Book Alignment
* **Book:** *Go in Practice, Second Edition*
* **Chapter:** Chapter 6: *Formatting, testing, debugging, and benchmarking*
* **Sections:**
  - 6.1 *Keeping your code and projects clean*
  - 6.2 *Logging (Logging data to different outputs, Going deeper with structured logging, Accessing and capturing stack traces)*

---

## 🎯 What You Will Learn
1. Using the Go standard library `log/slog` package.
2. Configuring `slog.TextHandler` (for clean local terminal output) vs `slog.JSONHandler` (for machine-readable production output).
3. Adding contextual key-value pairs using strongly-typed attributes (`slog.String`, `slog.Float64`, `slog.Duration`).
4. Attaching custom loggers to request contexts.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Initialize Logger
In `internal/config/logger.go`:
```go
package config

import (
	"log/slog"
	"os"
)

func InitLogger(format string, level slog.Level) *slog.Logger {
	var handler slog.Handler
	opts := &slog.HandlerOptions{
		Level: level,
	}

	if format == "json" {
		handler = slog.NewJSONHandler(os.Stdout, opts)
	} else {
		handler = slog.NewTextHandler(os.Stdout, opts)
	}

	logger := slog.New(handler)
	slog.SetDefault(logger)
	return logger
}
```

### 2. Log Ingestion Events with Context
In `internal/service/fetcher.go`:
```go
start := time.Now()
quote, err := p.FetchQuote(ctx, symbol)
elapsed := time.Since(start)

if err != nil {
	slog.Error("failed to fetch stock quote",
		slog.String("symbol", symbol),
		slog.String("provider", p.Name()),
		slog.Duration("latency", elapsed),
		slog.String("error", err.Error()),
	)
	return nil, err
}

slog.Info("successfully fetched stock quote",
	slog.String("symbol", quote.Symbol),
	slog.Float64("price", quote.Price),
	slog.String("provider", p.Name()),
	slog.Duration("latency", elapsed),
)
```

---

## ✅ Acceptance Criteria
- [ ] Format switches between text and JSON via configuration (`--log-format=json`).
- [ ] Log levels (`DEBUG`, `INFO`, `WARN`, `ERROR`) filter output correctly.
- [ ] HTTP requests and provider fetch events produce structured log attributes.
