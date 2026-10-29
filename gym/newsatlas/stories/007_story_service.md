# Story 007: Story Service (Domain Store & Spatial Queries)

## User Story
**As a** domain engineer,  
**I want to** build the Story service with PostGIS spatiotemporal clustering and bounding-box queries,  
**So that** related headlines are grouped into evolving stories and served to spatial map interfaces.

---

## 📖 Book Alignment
📖 **Go in Practice (2nd Ed) Alignment:**
- [Chapter 03: Structs, Interfaces, and Generics](../writings/go_in_practice_notes.md#chapter-03-structs-interfaces-and-generics) — §3.2 Repository pattern abstraction separating PostGIS spatial query logic from HTTP handlers.
- [Chapter 04: Handling Errors and Panics](../writings/go_in_practice_notes.md#chapter-04-handling-errors-and-panics) — §4.1 Sentinel errors for spatial bounding box boundaries and invalid polygon geometry.
- [Chapter 08: Building an HTTP Server](../writings/go_in_practice_notes.md#chapter-08-building-an-http-server) — §8.2 URL query parameter extraction, bounding-box parsing, and streaming JSON response serialization.

---

## 🎯 What You Will Learn
- **Core Objective:** The system of record for headlines and places, with fast spatial/time queries.
- **Architectural Concepts:** PostGIS (`geography`/`geometry`, GiST indexes, `ST_DWithin`, `ST_MakeEnvelope`,
`ST_ClusterDBSCAN`), partitioning by time, retention janitors, caches kept
fresh by events, cursor pagination, upserts (`ON CONFLICT`), read-your-writes.

---

## 🛠️ Step-by-Step Implementation Guide

### Implementation Tasks
1. ent schemas: `Headline`, `Place`, `Story`, + join tables; migrations create
   GiST + btree indexes.
2. Consumer for `headline.enriched`: **idempotent upsert** by `dedupe_key`.
3. Story clustering: attach to an existing story when title similarity >= t and
   centroid within X km and within 48 h; else create a new story.
4. Query services: `Search`, `GetInBBox`, `GetStory`, with cursor pagination
   (`(published_at, id)` keyset).
5. Publish `story.events` (`headline.added`, `story.updated`).
6. **Janitor**: retention with batch deletes; cache janitor for in-memory place
   cache. Make retention **configurable per kind**: keep plain map headlines
   ~30 days, but keep headlines that later get an instrument link (Phase 12) for
   a year or more - event studies need history. Design the janitor query so this
   change is a config change, not a rewrite.
7. gRPC handlers + mappers + tests.

---

## 📦 Deliverables
You can `grpcurl` a bbox query and get headlines back in < 50 ms for 1M rows
(generate data with a seeder).

---

## 🧪 Deep-Dive Exercises
Partition `headline` by month and compare query plans.

---

## 🤔 Reflection & Architectural Questions
Why keyset pagination instead of `OFFSET`? What breaks if `published_at` ties?
