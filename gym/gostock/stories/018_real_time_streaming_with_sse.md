# Story 018: Real-Time Streaming with Server-Sent Events (SSE)

## User Story
**As a** trader watching volatile stock prices,  
**I want** stock prices on the dashboard to update automatically in real-time,  
**So that** I see price changes immediately without manually refreshing the browser.

---

## 📖 Book Alignment
* **Book:** *Go in Practice, Second Edition*
* **Chapters:**
  - Chapter 5: *Concurrency in Go* (5.3 Channels and fan-out broadcasting)
  - Chapter 7: *File access and basic networking* (7.4 Websockets and server-sent events: Server-sent events)

---

## 🎯 What You Will Learn
1. Understanding Server-Sent Events (SSE) over HTTP compared to WebSockets.
2. Using Go's `http.Flusher` interface to stream chunks immediately to the client.
3. Building an SSE Broker/Hub using Go channels for client registration, unregistration, and broadcasting.
4. Clean channel cleanup upon client browser disconnect using `r.Context().Done()`.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Build the SSE Broker
In `internal/sse/broker.go`:
```go
package sse

import (
	"encoding/json"
	"fmt"
	"net/http"
	"sync"

	"github.com/zoiest/mono/gym/gostock/internal/domain"
)

type Broker struct {
	mu      sync.Mutex
	clients map[chan []byte]bool
}

func NewBroker() *Broker {
	return &Broker{
		clients: make(map[chan []byte]bool),
	}
}

func (b *Broker) BroadcastQuote(q *domain.Quote) {
	data, err := json.Marshal(q)
	if err != nil {
		return
	}
	msg := []byte(fmt.Sprintf("data: %s\n\n", data))

	b.mu.Lock()
	defer b.mu.Unlock()

	for clientChan := range b.clients {
		select {
		case clientChan <- msg:
		default:
			// Non-blocking drop if client buffer is full
		}
	}
}

func (b *Broker) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	flusher, ok := w.(http.Flusher)
	if !ok {
		http.Error(w, "streaming unsupported", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "text/event-stream")
	w.Header().Set("Cache-Control", "no-cache")
	w.Header().Set("Connection", "keep-alive")

	clientChan := make(chan []byte, 10)

	b.mu.Lock()
	b.clients[clientChan] = true
	b.mu.Unlock()

	defer func() {
		b.mu.Lock()
		delete(b.clients, clientChan)
		close(clientChan)
		b.mu.Unlock()
	}()

	notify := r.Context().Done()

	for {
		select {
		case <-notify:
			return
		case msg := <-clientChan:
			w.Write(msg)
			flusher.Flush()
		}
	}
}
```

### 2. Frontend SSE Listener
In `web/static/app.js`:
```javascript
const evtSource = new EventSource("/api/v1/stream");
evtSource.onmessage = function(event) {
    const quote = JSON.parse(event.data);
    updateRow(quote);
};
```

---

## ✅ Acceptance Criteria
- [ ] Clients receive price ticks via `text/event-stream`.
- [ ] Closing the browser tab disconnects the client and frees the channel.
- [ ] Web dashboard updates cells dynamically without page reload.
