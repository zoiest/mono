# Story 006: Enrichment Pipeline

## User Story
**As a** pipeline developer,  
**I want to** build an enrichment pipeline that deduplicates, detects language, and geotags headlines using PostGIS spatial points,  
**So that** raw text headlines are transformed into enriched, structured events with geographic coordinates.

---

## 📖 Book Alignment
📖 **Go in Practice (2nd Ed) Alignment:**
- [Chapter 03: Structs, Interfaces, and Generics](../writings/go_in_practice_notes.md#chapter-03-structs-interfaces-and-generics) — §3.3 Immutable domain value objects (`Location`, `GeoPoint`, `EnrichedHeadline`) and composition.
- [Chapter 05: Concurrency in Go](../writings/go_in_practice_notes.md#chapter-05-concurrency-in-go) — §5.4 Bounded worker pool pattern for concurrent CPU-bound tasks (tokenization, language detection, hash computation) avoiding goroutine proliferation.
- [Chapter 06: Formatting, Testing, Debugging, and Benchmarking](../writings/go_in_practice_notes.md#chapter-06-formatting-testing-debugging-and-benchmarking) — §6.5 Performance benchmarking and memory allocation profiling for deduplication algorithms.

---

## 🎯 What You Will Learn
- **Core Objective:** Turn `RawHeadline` into a located, classified, de-duplicated `Headline`.
- **Architectural Concepts:** Stream processing, idempotency keys, stateless vs stateful consumers, text
normalisation, gazetteer lookups, inverted index / trie, simhash or MinHash,
backpressure, worker pools, DLQ handling, metrics per stage.

---

## 🛠️ Step-by-Step Implementation Guide

### Implementation Tasks
1. **Normalise**: canonical URL (strip tracking params, lowercase host,
   resolve `amp`), trim/clean title, language detection.
2. **Geocode** (three strategies, try in order):
   a. Source-provided coordinates/country.
   b. Gazetteer match: import GeoNames "cities 1000" into Postgres/in-memory
      trie; extract capitalised n-grams from the title; score by population and
      context (country hints from the source's `default_country`).
   c. Fallback to the source's home location, with low `confidence`.
3. **Dedupe**: `dedupe_key = hash(canonical_url)` for exact; simhash on normalised
   title for near-duplicates within a rolling window (store recent simhashes in
   Redis with TTL).
4. **Classify**: keyword/rule-based category (world, politics, business, tech,
   sports, science, health, disaster). Make it an interface so you can plug in
   a model later.
5. Publish `headline.enriched` with `confidence` and `geocode_method`.
6. Bad input -> DLQ, never a crash loop.

---

## 📦 Deliverables
`enrichment-service` consuming/producing; metrics:
`enrich_latency_seconds`, `enrich_geocode_method_total{method}`,
`enrich_duplicates_total`.

---

## 🧪 Deep-Dive Exercises
Add "ambiguous place" handling (Paris, TX vs Paris, FR) with a confidence
penalty and an explainability field (`why`) returned to the UI.

---

## 🤔 Reflection & Architectural Questions
Where is the line between "enrichment" and "business rules"? What's the cost
of doing dedupe in the enrichment service vs in the store?
