# Story 014: Composable Middleware Pipeline

## User Story
**As a** backend engineer,  
**I want to** apply cross-cutting concerns (request logging, panic recovery, and CORS headers) using composable middlewares,  
**So that** business handlers remain clean, requests are observable, and panics never crash the server.

---

## 📖 Book Alignment
* **Book:** *Go in Practice, Second Edition*
* **Chapters:**
  - Chapter 4: *Handling errors and panics* (4.3 Capturing panics with `defer` and `recover`)
  - Chapter 8: *Building an HTTP server* (8.2 Reading and writing cookies, headers, and request context)

---

## 🎯 What You Will Learn
1. The standard Go HTTP middleware pattern: `func(http.Handler) http.Handler`.
2. Wrapping `http.ResponseWriter` to record status codes and response sizes.
3. Catching runtime panics safely using `defer` and `recover()`.
4. Composing multiple middleware layers cleanly into an execution chain.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Define Middleware Chain
In `internal/server/middleware.go`:
```go
package server

import (
	"log/slog"
	"net/http"
	"runtime/debug"
	"time"
)

type Middleware func(http.Handler) http.Handler

func Chain(h http.Handler, middlewares ...Middleware) http.Handler {
	for i := len(middlewares) - 1; i >= 0; i-- {
		h = middlewares[i](h)
	}
	return h
}
```

### 2. Implement Recovery and Logging Middlewares
```go
func Recoverer(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		defer func() {
			if rec := recover(); rec != nil {
				slog.Error("panic recovered in HTTP handler",
					slog.Any("error", rec),
					slog.String("stack", string(debug.Stack())),
				)
				http.Error(w, http.StatusText(http.StatusInternalServerError), http.StatusInternalServerError)
			}
		}()
		next.ServeHTTP(w, r)
	})
}

type statusRecorder struct {
	http.ResponseWriter
	statusCode int
}

func (rec *statusRecorder) WriteHeader(code int) {
	rec.statusCode = code
	rec.ResponseWriter.WriteHeader(code)
}

func RequestLogger(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()
		rec := &statusRecorder{ResponseWriter: w, statusCode: http.StatusOK}

		next.ServeHTTP(rec, r)

		slog.Info("http request",
			slog.String("method", r.Method),
			slog.String("path", r.URL.Path),
			slog.Int("status", rec.statusCode),
			slog.Duration("duration", time.Since(start)),
			slog.String("remote_addr", r.RemoteAddr),
		)
	})
}
```

---

## ✅ Acceptance Criteria
- [ ] Panicking in any handler returns HTTP 500 without stopping the HTTP process.
- [ ] Stack trace is logged at ERROR level.
- [ ] Every request logs method, path, status, and duration in `slog`.
