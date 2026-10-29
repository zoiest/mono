# Story 016: Event Detection & "Why Did It Move?"

## User Story
**As a** quantitative systems developer,  
**I want to** implement abnormal price/volume move detection using rolling Welford z-scores and rank candidate news stories,  
**So that** market anomalies are automatically paired with explanatory headlines answering 'Why did this stock move?'.

---

## 📖 Book Alignment
📖 **Go in Practice (2nd Ed) Alignment:**
- [Chapter 03: Structs, Interfaces, and Generics](../writings/go_in_practice_notes.md#chapter-03-structs-interfaces-and-generics) — §3.4 Type-safe streaming statistics engine (Welford's algorithm) implemented as a reusable generic struct.
- [Chapter 05: Concurrency in Go](../writings/go_in_practice_notes.md#chapter-05-concurrency-in-go) — §5.4 Parallel candidate news scoring using worker pools or `errgroup` for zero latency spikes.
- [Chapter 06: Formatting, Testing, Debugging, and Benchmarking](../writings/go_in_practice_notes.md#chapter-06-formatting-testing-debugging-and-benchmarking) — §6.5 Performance benchmarking and zero-allocation math routines for high-frequency tick analysis.

**Part A - Event detector (`event-detector`)**

1. Consume `bar.closed` (final bars only, plus revisions). Maintain per-instrument
   rolling state: mean/variance of returns over a window **per time-of-day
   bucket** (so 09:30 isn't compared with 13:00), average volume per bucket.
2. Detectors implemented as an interface, run side by side:
   - `return_spike`: |return over 1/5/15/60 min| / rolling σ > threshold.
   - `volume_spike`: volume / rolling average > ratio.
   - `gap`: open vs previous close beyond k·σ.
   - `volatility_regime`: realised vol vs 30-day baseline.
3. Suppress noise: minimum liquidity filter, cooldown per instrument+kind,
   merge adjacent events into one (an event has a start and an end).
4. Warm-up: on boot, rebuild rolling state from the last N days of bars (do
   **not** emit events during warm-up).
5. Publish `market.event` with all the numbers (`ret`, `zscore`, `volume_ratio`,
   `window`, `detector_version`) so the UI can explain *why it was flagged*.
6. Calibrate thresholds: choose them so that a typical liquid stock yields only
   a handful of events a day; write the calibration notebook/script and commit
   the resulting config + date.

**Part B - Insight service (`insight-service`)**

1. On `market.event`, build the **candidate window**:
   `[event.start - Δbefore, event.end + Δafter]` (e.g. 6 h before, 30 min after;
   make them configurable per asset class and market session).
2. Fetch candidates from `story-service`: headlines linked to the instrument
   with `score >= t`; plus **group-level** candidates (sector, country, macro
   taxonomy) with a penalty.
3. **Rank** with an explainable linear score, e.g.
   `rank = w1*link_score + w2*time_proximity + w3*source_weight +
   w4*story_size + w5*category_prior + w6*novelty` where *novelty* penalises
   re-reports of an old story. Store each feature in the result.
4. Persist `Insight{event_id, candidates[], method_version}`; publish
   `insight.created`. **Never overwrite**; a new `method_version` creates a new
   record so you can compare rankers offline.
5. Handle late news: headlines arriving after the insight was created (e.g. the
   RSS feed polled 10 min later) trigger an **insight refresh** within the
   candidate window. Decide and document: refresh in place, or append a new
   revision?
6. API: `ListMoves(watchlist, from, to, min_z)` and `GetInsight`.
7. UI contract: for each candidate return `published_at` relative to the event
   (`-37m`), `link.why`, `rank_features`, and whether it was published **before
   or after** the move started.

**Part C - Honest statistics (v4 groundwork)**

1. Implement a basic **event study**: for headlines of category *C* linked to
   instrument *I*, compute average cumulative abnormal return at +15m, +1h,
   +1d, using a market/sector index as the benchmark; report `n`, mean, std
   error, 95% CI.
2. Refuse to display results when `n < 30` (configurable) and show "not enough
   data" - make the **UI** honour that rule, too.
3. Write a test that proves your pipeline cannot use information that was not
   available at time *t* (**no look-ahead**): feed a fixture where the label
   leaks from the future and assert the feature builder ignores it.
4. In `docs/notes/phase-16.md`, list 5 ways this feature can mislead a user
   (confounding events, news after the fact, thin liquidity, multiple
   instruments moving together, survivorship in the instrument universe) and
   how the UI mitigates each.

---

## 🎯 What You Will Learn
- **Core Objective:** Detect abnormal price/volume behaviour, attach ranked candidate news, and
present it honestly in the UI.
- **Architectural Concepts:** Returns (log vs simple), rolling mean/variance (Welford), volatility
estimators, z-scores and their limits (fat tails), intraday seasonality
(volume at the open is always high), market-hours awareness, time-window joins
between two streams, ranking with explainable features, **event-study
methodology** (event window, estimation window, abnormal return), small-sample
statistics and confidence intervals, **look-ahead bias**, multiple-comparison
pitfalls, "correlation is not causation".

---

## 🛠️ Step-by-Step Implementation Guide

---

## 📦 Deliverables
The portal's **Moves** page lists today's abnormal moves in your watchlist,
each with the top 3 candidate headlines, a mini price chart with news flags, and
a mini-map of where the news occurred.

---

## 🤔 Reflection & Architectural Questions
Suppose your ranker puts the right headline first 70% of the time. How should
the UI present a 70% hypothesis so users don't treat it as a fact? What would
you need to measure to know whether the feature actually helps you?
