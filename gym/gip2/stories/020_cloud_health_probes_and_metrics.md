# Story 020: Cloud Health Probes & Runtime Metrics

## User Story
**As a** Kubernetes or Docker platform engineer,  
**I want** explicit `/healthz` (liveness) and `/readyz` (readiness) endpoints reporting memory and runtime metrics,  
**So that** orchestrators know when the service is healthy, ready to receive traffic, or needs restarting.

---

## 📖 Book Alignment
* **Book:** *Go in Practice, Second Edition*
* **Chapter:** Chapter 12: *Cloud-ready applications and communications*
* **Sections:**
  - 12.1 *Cloud computing overview & cloud-native applications*
  - 12.4 *Running on cloud servers (Performing runtime detection, Performing runtime monitoring)*

---

## 🎯 What You Will Learn
1. Designing Kubernetes-compatible liveness and readiness probe semantics.
2. Inspecting the Go runtime: `runtime.ReadMemStats(&m)` and `runtime.NumGoroutine()`.
3. Verifying downstream dependency readiness before marking traffic-ready.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Build Health & Readiness Handlers
In `internal/server/health.go`:
```go
package server

import (
	"encoding/json"
	"net/http"
	"runtime"
	"time"
)

type RuntimeMetrics struct {
	Status        string `json:"status"`
	Uptime        string `json:"uptime"`
	NumGoroutines int    `json:"num_goroutines"`
	AllocMB       uint64 `json:"alloc_mb"`
	TotalAllocMB  uint64 `json:"total_alloc_mb"`
	SysMB         uint64 `json:"sys_mb"`
	NumGC         uint32 `json:"num_gc"`
}

var startTime = time.Now()

func (s *Server) handleHealthz(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	_, _ = w.Write([]byte(`{"status":"alive"}`))
}

func (s *Server) handleReadyz(w http.ResponseWriter, r *http.Request) {
	var m runtime.MemStats
	runtime.ReadMemStats(&m)

	stats := RuntimeMetrics{
		Status:        "ready",
		Uptime:        time.Since(startTime).Truncate(time.Second).String(),
		NumGoroutines: runtime.NumGoroutine(),
		AllocMB:       m.Alloc / 1024 / 1024,
		TotalAllocMB:  m.TotalAlloc / 1024 / 1024,
		SysMB:         m.Sys / 1024 / 1024,
		NumGC:         m.NumGC,
	}

	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(stats)
}
```

---

## ✅ Acceptance Criteria
- [ ] `GET /healthz` returns 200 OK immediately.
- [ ] `GET /readyz` outputs Go memory stats and goroutine count in JSON.
