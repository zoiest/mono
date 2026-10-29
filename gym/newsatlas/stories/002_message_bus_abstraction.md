# Story 002: Message Bus Abstraction

## User Story
**As a** event-driven systems engineer,  
**I want to** build a message bus abstraction hiding Redis Streams behind generic Go interfaces with in-memory test doubles,  
**So that** microservices can publish and consume typed event streams reliably with automatic backoff retry and DLQ routing.

---

## 📖 Book Alignment
📖 **Go in Practice (2nd Ed) Alignment:**
- [Chapter 03: Structs, Interfaces, and Generics](../writings/go_in_practice_notes.md#chapter-03-structs-interfaces-and-generics) — §3.2 Interface-driven architecture (defining consumer-side `Producer`, `Subscriber`, `Delivery` interfaces), §3.4 Generics for type-safe message envelopes (`Envelope[T any]`).
- [Chapter 04: Handling Errors and Panics](../writings/go_in_practice_notes.md#chapter-04-handling-errors-and-panics) — §4.2 Contextual error wrapping (`fmt.Errorf("%w")`), custom transient/permanent error classifiers for backoff retry and DLQ routing.
- [Chapter 05: Concurrency in Go](../writings/go_in_practice_notes.md#chapter-05-concurrency-in-go) — §5.2 Unbuffered/buffered channels, worker dispatch loops, and channel-based test mocks without external dependencies.
- [The Ten Cardinal Rules](../writings/go_in_practice_notes.md#the-ten-cardinal-rules-of-idiomatic-go) — Rule 3: *Accept interfaces, return structs* & Rule 6: *Wrap errors with context (%w)*.

Interface (starting point):

```go
type Message struct {
    ID      string            // bus-assigned
    Key     string            // ordering key
    Headers map[string]string // trace id, schema, content-type
    Data    []byte
}

type Producer interface {
    Produce(ctx context.Context, m Message) (id string, err error)
    Close() error
}

type Consumer interface {                // broadcast: every instance sees all
    Messages() <-chan Delivery
    Close() error
}

type GroupConsumer interface {           // work-sharing
    Messages() <-chan Delivery
    Close() error
}

type Delivery struct {
    Message
    Ack() error
    Nack(requeue bool) error             // or Retry(after time.Duration)
}
```

---

## 🎯 What You Will Learn
- **Core Objective:** A small, well-tested library that hides Redis Streams (and later NATS/Kafka)
behind three types: **Producer, Consumer, ConsumerGroup**.
- **Architectural Concepts:** Streams vs queues vs pub/sub, `XADD/XREADGROUP/XACK/XPENDING/XCLAIM`,
at-least-once delivery, idempotency, back-pressure, poison messages, DLQ,
ordering per key, retention (`MAXLEN`), connection health, backoff.

---

## 🛠️ Step-by-Step Implementation Guide

### Implementation Tasks
1. In-memory implementation first (fast unit tests for everything else).
2. Redis Streams implementation with consumer groups, auto-create group, `MKSTREAM`.
3. Reclaim stuck messages (`XAUTOCLAIM`) after a visibility timeout.
4. Retry policy: N attempts with backoff, then publish to `<stream>.dlq` with the
   error attached.
5. Typed helpers: `events.Publish[T]`, `events.Subscribe[T]` `(handler)`; JSON codec
   with schema/version header.
6. Connection resilience: bounded ping loop at boot, per-command retry on
   connection errors, background health check, exposed as a readiness probe.
7. Environment-selected backend (`MB_SERVICE=redis|memory|nats`).

---

## 📦 Deliverables
`internal/common/mbus` + a README with usage and failure behaviour.

---

## 🤔 Reflection & Architectural Questions
What does "exactly-once" really mean, and why do you design for
**at-least-once + idempotent consumers** instead? Where would an ordering
guarantee break if you scale a group to 5 consumers?
