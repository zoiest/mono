# Story 015: React Portal (Map & Charts)

## User Story
**As a** full-stack developer,  
**I want to** build a modern React 18 SPA with MapLibre GL spatial map scenes and TradingView price chart scenes,  
**So that** analysts can visualize live global news stories and financial instrument price action in real time.

---

## 📖 Book Alignment
📖 **Go in Practice (2nd Ed) Alignment:**
- [Chapter 09: HTML and Email Template Patterns](../writings/go_in_practice_notes.md#chapter-09-html-and-email-template-patterns) — §9.1 Server-rendered bootstrap shells and dynamic metadata injection.
- [Chapter 10: Sending and Receiving Data](../writings/go_in_practice_notes.md#chapter-10-sending-and-receiving-data) — §10.1 Single-binary static asset embedding using `embed.FS` and `http.FileServer` to deliver production SPA bundles from Go binaries.

Suggested `src/` layout:

```text
src/
├── api/            # generated client + thin wrappers + query keys
├── auth/           # OIDC provider, token refresh, route guards
├── components/     # dumb, reusable (Button, Panel, Badge, EmptyState, ...)
├── hooks/          # useHeadlines, useMapClusters, useSse, useBookmarks, ...
├── scenes/         # one folder per screen
│   ├── map/        #   MapScene, MapLayers, ClusterPopup, TimeSlider, Filters
│   ├── instrument/ #   PriceChart, NewsFlags, Snapshot, RangeSelector, CompareOverlay
│   ├── watchlist/  #   WatchlistTable (sparklines, live flash), AddInstrument
│   ├── moves/      #   MoveCard, CandidateList, MiniMap, "no obvious news" state
│   ├── briefing/   #   DailyBriefing
│   ├── sources/    #   SourcesTable, SourceForm (validation)
│   ├── adapters/   #   AdapterHealth, AssignmentGraph
│   ├── alerts/
│   └── bookmarks/
├── store/          # Zustand slices: filters, mapViewport, ui
├── services/       # non-React logic: sse client, formatters, geo utils
├── workers/        # clustering / downsampling off the main thread
├── routes/
├── i18n/           # en.json, fi.json (or any 2nd language)
└── mocks/          # MSW handlers for dev and tests
```

---

## 🎯 What You Will Learn
- **Core Objective:** A real SPA that exercises every backend contract.
- **Architectural Concepts:** React 18 + TS (strict), Vite, routing, **server state vs client state**,
generated API client, auth (OIDC code flow + PKCE), MapLibre GL, web workers,
SSE, optimistic updates, error boundaries, i18n, accessibility, unit +
component + e2e tests, bundle analysis.

---

## 🛠️ Step-by-Step Implementation Guide

### Implementation Tasks
1. Scaffold with Vite; strict TS; ESLint + Prettier; absolute imports.
2. Generate the API client from `openapi.yaml`; wrap with TanStack Query hooks
   (query keys include filters + bbox).
3. OIDC login (Keycloak) with PKCE; silent refresh; guard routes by role.
4. **Map scene**: MapLibre; debounce viewport changes (e.g. 250 ms); call
   `/map/clusters`; render circles sized by count; click -> popup/list; sync
   viewport + filters to the **URL** (shareable links).
5. **Live updates**: `useSse` hook with auto-reconnect/backoff; merge
   `headline.added` into the cached query data without refetching the world;
   animate new points.
6. **Time slider**: scrub over the last 24 h; query keyed by range; keep
   interaction smooth.
7. Sources admin: table with sort/filter, create/edit form with client-side
   validation mirroring server rules; optimistic toggle enabled/disabled.
8. Adapter health scene: live status, last error, owned sources.
9. Saved views + bookmarks.
10. Web worker for client-side re-clustering of points at high zoom.
11. i18n with at least two languages; date/number formatting via `Intl`.
12. Accessibility: keyboard navigation of the list, ARIA labels, colour
    contrast, "reduced motion" support; a non-map list fallback.
13. Tests: unit (utils), component (RTL), API mocking (MSW), e2e (Playwright:
    login -> add source -> see marker from the replay adapter).

**Market and linking UI (build after Phase 9, extend after Phases 12 and 16):**

14. **Instrument page**: `lightweight-charts` candlesticks + volume; range
    buttons (1D/5D/1M/1Y/5Y) map to bar intervals; load more history on
    scroll-left; last candle updates from SSE `quote.live`; show currency and
    exchange-local time; indicate pre/post-market and market-closed state.
15. **Watchlist table**: live price with up/down flash (respect "reduced
    motion"), day change %, sparkline from `bars?interval=5m`, sorting, drag to
    reorder, add instrument via debounced search. Virtualise rows if > 200.
16. **News flags on the chart**: markers positioned by `published_at`, styled by
    link score, with a popover (title, source, `why` of the link). Hover a flag
    -> highlight the headline's marker on the map; click a map marker -> scroll
    the chart to that time. Keep one shared "selected headline" state.
17. **Moves page / "Why did it move?" card**: event summary (`-2.8% in 15m,
    4.1σ, 3.2x volume`), ranked candidate headlines with *before/after* badge,
    link confidence shown as a label not a bare number, and an explicit "no
    linked news found" state. Never use causal wording ("caused by") - use
    "possible related news".
18. **Daily briefing** page (v4): top movers, their candidate news, a mini-map of
    where the news happened, export as Markdown.
19. Formatting: use `Intl.NumberFormat` with the instrument's currency;
    colour semantics must not rely on red/green alone (add arrows/signs for
    colour-blind users) and may differ by locale convention.
20. Performance: chart data transformed in a **web worker**; SSE ticks batched
    with `requestAnimationFrame`; no re-render of the whole watchlist on each
    tick (row-level subscriptions).

---

## 📦 Deliverables
Production build served by Nginx (or any static server) with SPA fallback and
a reverse-proxy rule for `/api`.

---

## 🤔 Reflection & Architectural Questions
What belongs in the URL, in a global store, in TanStack Query cache, and in
local component state? Why is it dangerous to keep server data in a global
client store?
