# Story 020: Capstone and Architecture Review

## User Story
**As a** lead architect,  
**I want to** perform end-to-end chaos engineering tests, disaster recovery drills, and complete an architectural retrospective,  
**So that** the entire distributed event-driven platform is proven resilient, performant, and ready for continuous production usage.

---

## 📖 Book Alignment
📖 **Go in Practice (2nd Ed) Alignment:**
- [The Ten Cardinal Rules of Idiomatic Go](../writings/go_in_practice_notes.md#the-ten-cardinal-rules-of-idiomatic-go) — Complete synthesis of all 10 Cardinal Rules in production operations and fault recovery.
- [All 13 Chapters](../writings/go_in_practice_notes.md) — Comprehensive validation of Go engineering best practices across CLI, networking, concurrency, error handling, templates, and cloud architecture.

1. Add one **brand-new feature end-to-end** without help from this document -
   pick one:
   - "follow a place": subscribe to a city, get an alert when its headline rate
     spikes;
   - **sentiment layer**: score each linked headline (lexicon first, small model
     later), colour chart flags by sentiment, and measure whether sentiment adds
     any information beyond the category prior in your ranker;
   - **earnings calendar**: ingest earnings dates, show them on the chart, and
     mark moves around earnings as "scheduled event" rather than "surprise";
   - **correlated instruments**: when AAPL moves, show peers' moves and the
     sector index in the same card.
   Touch: proto, registry or ui-backend, bus event, alert rule, gateway
   endpoint, portal screen, tests, Helm values.
2. Write a 2-page architecture overview for a new teammate.
3. Hold a (self-recorded) 20-minute walkthrough: boot sequence, a message's
   life, a failure and how the system heals.
4. Re-read your ADRs. Which three decisions would you change now, and why?
5. **Use it for a month.** Keep a log: which "Why did it move?" cards were right,
   wrong, or "no news"? Compute your own top-3 accuracy. Feed the labelled
   cases back into Phase 12/16 as a regression test set.

---

---

## 🎯 What You Will Learn
- **Core Objective:** Consolidate. Prove you can explain and extend the system.
- **Architectural Concepts:** 

---

## 🛠️ Step-by-Step Implementation Guide

### Capstone Directives
🎯 Consolidate. Prove you can explain and extend the system.

📖 **Go in Practice (2nd Ed) Alignment:**
- [The Ten Cardinal Rules of Idiomatic Go](../writings/go_in_practice_notes.md#the-ten-cardinal-rules-of-idiomatic-go) — Complete synthesis of all 10 Cardinal Rules in production operations and fault recovery.
- [All 13 Chapters](../writings/go_in_practice_notes.md) — Comprehensive validation of Go engineering best practices across CLI, networking, concurrency, error handling, templates, and cloud architecture.

1. Add one **brand-new feature end-to-end** without help from this document -
   pick one:
   - "follow a place": subscribe to a city, get an alert when its headline rate
     spikes;
   - **sentiment layer**: score each linked headline (lexicon first, small model
     later), colour chart flags by sentiment, and measure whether sentiment adds
     any information beyond the category prior in your ranker;
   - **earnings calendar**: ingest earnings dates, show them on the chart, and
     mark moves around earnings as "scheduled event" rather than "surprise";
   - **correlated instruments**: when AAPL moves, show peers' moves and the
     sector index in the same card.
   Touch: proto, registry or ui-backend, bus event, alert rule, gateway
   endpoint, portal screen, tests, Helm values.
2. Write a 2-page architecture overview for a new teammate.
3. Hold a (self-recorded) 20-minute walkthrough: boot sequence, a message's
   life, a failure and how the system heals.
4. Re-read your ADRs. Which three decisions would you change now, and why?
5. **Use it for a month.** Keep a log: which "Why did it move?" cards were right,
   wrong, or "no news"? Compute your own top-3 accuracy. Feed the labelled
   cases back into Phase 12/16 as a regression test set.

---
