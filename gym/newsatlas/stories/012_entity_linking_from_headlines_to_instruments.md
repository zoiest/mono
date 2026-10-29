# Story 012: Entity Linking (Headlines to Instruments)

## User Story
**As a** data engineer,  
**I want to** build an entity linking engine using Aho-Corasick / Trie matching and disambiguation heuristics,  
**So that** enriched headlines are accurately linked to tradable instruments with calibrated confidence scores.

---

## 📖 Book Alignment
📖 **Go in Practice (2nd Ed) Alignment:**
- [Chapter 03: Structs, Interfaces, and Generics](../writings/go_in_practice_notes.md#chapter-03-structs-interfaces-and-generics) — §3.4 Generic trie / prefix tree implementations (`Trie[T any]`) for high-throughput string matching.
- [Chapter 06: Formatting, Testing, Debugging, and Benchmarking](../writings/go_in_practice_notes.md#chapter-06-formatting-testing-debugging-and-benchmarking) — §6.4 Fuzz testing string normalizers and alias extractors (`testing.F`) to discover edge cases in UTF-8 text.

---

## 🎯 What You Will Learn
- **Core Objective:** For each headline, decide *which instruments it is about*, with a calibrated
confidence and a human-readable reason.
- **Architectural Concepts:** Named-entity recognition (rule-based first), alias dictionaries, Aho-Corasick
/ trie matching, tokenisation, case/diacritics normalisation, disambiguation
(ambiguous names: "Apple", "Meta", "Shell", "Target", "Tesla" the car vs the
person), context scoring, precision/recall/F1, evaluation sets, rebuild/reprocess
pipelines, schema evolution with a new consumer.

---

## 🛠️ Step-by-Step Implementation Guide

### Implementation Tasks
1. Build an **alias index** from the instrument master: ticker symbols,
   legal names, short names ("Alphabet", "Google"), brands, CEO names (weak
   signal), and exclusions. Rebuild on `instrument.events` (broadcast
   consumer; keep an atomic swap of the index).
2. **Matcher**: multi-pattern search over the title + summary (Aho-Corasick or
   a token trie). Distinguish:
   - `$TSLA` / `(NASDAQ: TSLA)` cashtag-style mentions -> high confidence.
   - Bare uppercase tickers (`AI`, `ON`, `ALL`, `A`) -> **very** low confidence
     unless context supports it. Maintain a stop-list of ambiguous tickers.
   - Company names -> medium; with legal suffix ("Apple Inc.") -> higher.
3. **Disambiguation** features: category (business/tech vs sports), co-mentioned
   entities ("iPhone", "Cupertino"), source type (a finance outlet vs general),
   capitalisation, surrounding words ("shares of", "stock", "earnings").
   Start with hand-tuned weights; then fit a tiny logistic regression on your
   labelled data.
4. Output `headline.linked {headline_id, links:[{instrument_id, score, method,
   why}], linker_version}` as a **new consumer of `headline.enriched`** - note
   that no producer changed.
5. `story-service`: new consumer stores `HeadlineLink`
   (`UNIQUE(headline_id, instrument_id, linker_version)`), exposes
   `GetHeadlinesForInstrument(instrument, from, to, min_score)` and
   `GetInstrumentsForHeadline`.
6. **Reprocessing**: `busctl replay headline.enriched --since ...` or a
   `backfill` task re-runs the linker over history when you improve it; old
   links with an older `linker_version` are superseded, not duplicated.
7. **Evaluation harness** (`tools/labeling`): a tiny CLI/web page to label ~300
   headlines (headline, expected instruments or "none"); a Go test that reports
   precision/recall per method and fails CI if F1 drops by more than 2 points.
8. Also link **sector/country/commodity** concepts (e.g. "oil", "OPEC", "ECB",
   "chip shortage") to *groups* of instruments via a small taxonomy. These
   become the "macro" candidates in Phase 16.

---

## 📦 Deliverables
A headline "Apple unveils new iPhone as shares rise" links to `AAPL` with a
score and `why = ["name: Apple", "context: iPhone, shares"]`; "Apple harvest
season begins" does not.

---

## 🤔 Reflection & Architectural Questions
Why is a *wrong* link worse than a *missing* link for the "why did it move?"
feature? How would you expose uncertainty in the UI honestly?
