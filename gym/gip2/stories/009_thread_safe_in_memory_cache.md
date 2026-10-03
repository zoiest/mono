# Story 009: Thread-Safe In-Memory Cache with TTL

## User Story
**As an** API consumer,  
**I want** recent stock quotes to be cached in memory with a configurable Time-To-Live (TTL),  
**So that** redundant external network queries are eliminated and response times for frequent queries remain sub-millisecond.

---

## 📖 Book Alignment
* **Book:** *Go in Practice, Second Edition*
* **Chapters:**
  - Chapter 3: *Structs, interfaces, and generics* (3.4 Simplifying code with generics, using constraints and type approximations)
  - Chapter 5: *Concurrency in Go* (5.2 Locking with a mutex, `sync.RWMutex`)

---

## 🎯 What You Will Learn
1. When to choose `sync.RWMutex` over `sync.Mutex` (read-heavy vs write-heavy workloads).
2. Implementing a generic key-value cache using Go generics (`[K comparable, V any]`).
3. TTL expiration logic (passive check on read vs active background cleanup worker).
4. Preventing cache stampedes and race conditions.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Build Generic In-Memory Cache
In `internal/cache/cache.go`:
```go
package cache

import (
	"sync"
	"time"
)

type item[V any] struct {
	value     V
	expiresAt time.Time
}

func (i item[V]) isExpired() bool {
	return time.Now().After(i.expiresAt)
}

type MemoryCache[K comparable, V any] struct {
	mu    sync.RWMutex
	items map[K]item[V]
	ttl   time.Duration
}

func New[K comparable, V any](ttl time.Duration) *MemoryCache[K, V] {
	return &MemoryCache[K, V]{
		items: make(map[K]item[V]),
		ttl:   ttl,
	}
}

func (c *MemoryCache[K, V]) Get(key K) (V, bool) {
	c.mu.RLock()
	defer c.mu.RUnlock()

	it, found := c.items[key]
	if !found || it.isExpired() {
		var zero V
		return zero, false
	}
	return it.value, true
}

func (c *MemoryCache[K, V]) Set(key K, value V) {
	c.mu.Lock()
	defer c.mu.Unlock()

	c.items[key] = item[V]{
		value:     value,
		expiresAt: time.Now().Add(c.ttl),
	}
}

func (c *MemoryCache[K, V]) EvictExpired() {
	c.mu.Lock()
	defer c.mu.Unlock()

	now := time.Now()
	for k, it := range c.items {
		if now.After(it.expiresAt) {
			delete(c.items, k)
		}
	}
}
```

---

## ✅ Acceptance Criteria
- [ ] Generic cache supports any comparable key and any value type.
- [ ] Concurrent reads and writes tested with `go test -race` without deadlocks or data races.
- [ ] Items older than TTL return `false` on `Get()`.
- [ ] Background cleanup runs periodically without blocking concurrent readers.
