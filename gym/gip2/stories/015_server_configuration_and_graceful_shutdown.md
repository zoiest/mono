# Story 015: Server Configuration & Graceful Shutdown

## User Story
**As a** system administrator,  
**I want** the HTTP server to configure explicit network timeouts and perform graceful shutdown on OS signals (`SIGINT`, `SIGTERM`),  
**So that** pending client connections finish cleanly without truncated downloads or dropped transactions during updates.

---

## 📖 Book Alignment
* **Book:** *Go in Practice, Second Edition*
* **Chapters:**
  - Chapter 2: *A solid foundation: Building a command-line application* (2.3 Working with real-world web servers: Starting up and shutting down a server, Graceful shutdowns using OS signals)
  - Chapter 8: *Building an HTTP server* (8.2 More control over our server)

---

## 🎯 What You Will Learn
1. Configuring explicit timeouts on `http.Server` (`ReadHeaderTimeout`, `ReadTimeout`, `WriteTimeout`, `IdleTimeout`) to protect against Slowloris attacks.
2. Intercepting OS termination signals using `signal.Notify` or `signal.NotifyContext`.
3. Invoking `server.Shutdown(ctx)` with a deadline to drain in-flight requests.
4. Closing background workers and flushers before application exit.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Configure the Server and Graceful Signal Listener
In `cmd/gostock-server/main.go`:
```go
package main

import (
	"context"
	"errors"
	"fmt"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/tofunth/gostock/internal/config"
	"github.com/tofunth/gostock/internal/server"
)

func main() {
	cfg, err := config.Load(os.Args[1:])
	if err != nil {
		slog.Error("configuration error", slog.String("error", err.Error()))
		os.Exit(1)
	}

	appServer := server.New(cfg)

	httpServer := &http.Server{
		Addr:              fmt.Sprintf(":%d", cfg.Port),
		Handler:           appServer.Handler(),
		ReadHeaderTimeout: 3 * time.Second,
		ReadTimeout:       10 * time.Second,
		WriteTimeout:      15 * time.Second,
		IdleTimeout:       60 * time.Second,
	}

	// Trap termination signals
	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer stop()

	// Run server in goroutine
	go func() {
		slog.Info("gostock server listening", slog.String("addr", httpServer.Addr))
		if err := httpServer.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) {
			slog.Error("server error", slog.String("error", err.Error()))
			os.Exit(1)
		}
	}()

	// Block until signal is received
	<-ctx.Done()
	slog.Info("shutting down server gracefully...")

	shutdownCtx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	if err := httpServer.Shutdown(shutdownCtx); err != nil {
		slog.Error("server forced to shutdown", slog.String("error", err.Error()))
	}

	slog.Info("server exited cleanly")
}
```

---

## ✅ Acceptance Criteria
- [ ] Server initiates shutdown upon receiving `SIGINT` (Ctrl+C) or `SIGTERM`.
- [ ] In-flight requests are given up to 10 seconds to finish.
- [ ] Server exits with return code 0 when shut down gracefully.
