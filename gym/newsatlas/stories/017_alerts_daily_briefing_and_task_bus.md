# Story 017: Alerts, Daily Briefing & Task Bus

## User Story
**As a** product engineer,  
**I want to** build a rule engine for threshold alerts, an asynchronous task bus for heavy operations, and a market-calendar daily briefing email generator,  
**So that** users receive proactive, timely market intelligence and daily digests before market opens.

---

## 📖 Book Alignment
📖 **Go in Practice (2nd Ed) Alignment:**
- [Chapter 02: Building CLI Applications](../writings/go_in_practice_notes.md#chapter-02-building-cli-applications) — §2.3 Scheduled background task runners with clean interrupt signals.
- [Chapter 05: Concurrency in Go](../writings/go_in_practice_notes.md#chapter-05-concurrency-in-go) — §5.2 Task bus consumer queues and bounded worker pools executing long-running backfills.
- [Chapter 09: HTML and Email Template Patterns](../writings/go_in_practice_notes.md#chapter-09-html-and-email-template-patterns) — §9.1 Robust email rendering with `html/template` (template inheritance, custom `FuncMap`, safe data escaping, inline CSS styles).

**Part A - Alert rules**

1. `AlertRule.expr` e.g.
   `count(category == "disaster", window="15m", radius_km=50) >= 5`.
2. Evaluate on each `headline.enriched` using a per-rule sliding window held in
   memory (Redis for HA, as a stretch).
3. Cooldown per rule+area so you don't spam.
4. Publish `alert.raised`; add webhook/email sinks behind an interface (use
   Mailpit locally).
5. Hot-reload rules when changed (event-driven cache refresh).
6. Provide a **dry-run** API: evaluate a rule against the last N hours.
7. **Market-aware rules** over `market.event` / `headline.linked`, e.g.
   - `move(instrument in watchlist, z >= 4)` -> "unusual move".
   - `move(z >= 4) AND NOT linked_news(window="2h", min_score=0.6)` -> "move
     without visible news" (often the most interesting case).
   - `linked_headlines(instrument, category == "earnings", window="1h") >= 3`.
   - `price_cross(instrument, level, direction)` (simple user thresholds).
   Make the rule language a small, typed DSL (CEL or `expr`) with a
   compile-time check against the available fields; reject unknown fields.
8. Respect the **market calendar**: a rule can say `only_when_market_open`;
   queue non-urgent alerts until the next session; never wake yourself at 3 a.m.
   for a low-liquidity instrument (quiet hours per user).

**Part B - Task bus**

1. Task model: `{id, type, params, status, progress, subtasks[], created_by}`.
2. Publisher -> `task.commands`; executors consume in a group; progress to
   `task.status`; state persisted so the UI can show history.
3. Implement tasks: **backfill source** (re-fetch last N days), **re-geocode
   range**, **export CSV**, **purge source**, **backfill bars for instrument
   range**, **re-link headlines** (re-run the entity linker with a new
   `linker_version` over a date range), **recompute events** (new detector
   version).
4. Scheduler: cron-expression tasks aware of **exchange time zones** (e.g. "30
   minutes after the US close", "08:00 local before the European open"):
   - nightly retention report,
   - **daily briefing generator**: for each user watchlist, collect top movers,
     their top candidate news (from `insight-service`), the top news clusters on
     the map, and render a Markdown/HTML digest (email via Mailpit locally);
   - weekly data-quality report (gaps, stale sources, link coverage).
5. Cancellation: `task.cancel` event -> executor checks `ctx`.
6. Hooks: `before`/`after` hooks per task type (e.g. lock the source during purge).

---

## 🎯 What You Will Learn
- **Core Objective:** Two classic backend subsystems: a **rule engine** and a **command/task
system**.
- **Architectural Concepts:** Expression engines (CEL / expr), sliding windows, spatial aggregation,
rate-limited notifications (cooldowns), cron scheduling, long-running tasks
with subtasks, progress reporting, cancellation, idempotent task handlers,
hooks (pre/post).

---

## 🛠️ Step-by-Step Implementation Guide

---

## 🤔 Reflection & Architectural Questions
What's the difference between a *scheduled task*, a *background job*, and a
*stream consumer*? When would you reach for each?
