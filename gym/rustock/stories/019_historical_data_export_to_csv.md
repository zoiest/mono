# Story 019: Historical Data Export to CSV

## User Story
**As a** quantitative analyst,
**I want to** export historical OHLCV stock prices to a downloadable CSV file via both the CLI and HTTP API,
**So that** I can import market history directly into spreadsheets or data analysis pipelines.

---

## 📖 Book Alignment
* **Reference:** *The Rust Programming Language* (TRPL — [doc.rust-lang.org/book](https://doc.rust-lang.org/book/))
* **Chapters:**
  - Chapter 8: *Common Collections* (`Vec<HistoricalPrice>`, UTF-8 `String`)
  - Chapter 12: *An I/O Project: Building a Command Line Program* (File & `std::io::Write` streams)
  - Chapter 13: *Functional Language Features: Iterators and Closures*
    - 13.2 *Processing a Series of Items with Iterators*

---

## 🎯 What You Will Learn
1. Writing records through `std::io::Write` abstractions (`Vec<u8>`, `std::fs::File`, `BufWriter`) using the `csv` crate.
2. Combining `serde::Serialize` with `csv::Writer` for zero-boilerplate CSV column headers.
3. Streaming CSV downloads from Axum with `Content-Type: text/csv` and `Content-Disposition: attachment; filename="..."`.
4. Validating ticker symbols safely before embedding them in HTTP header filenames.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Add `csv = "1.3"` to `Cargo.toml`

### 2. Implement a Generic `std::io::Write` CSV Exporter
In `src/export/csv.rs`:
```rust
use std::io::Write;

use crate::domain::HistoricalPrice;

pub fn write_history_csv<W: Write>(
    writer: W,
    rows: &[HistoricalPrice],
) -> Result<(), csv::Error> {
    let mut wtr = csv::Writer::from_writer(writer);
    for row in rows {
        wtr.serialize(row)?;
    }
    wtr.flush()?;
    Ok(())
}
```
Notice how generic `W: Write` works identically whether writing to an in-memory `Vec<u8>` buffer for HTTP responses or a `BufWriter<File>` in the CLI!

### 3. Add HTTP Export Handler
Expose `GET /api/v1/stocks/{symbol}/export.csv`, sanitize `symbol` to ASCII alphanumerics/dots/hyphens, write CSV rows, and return response headers:
- `Content-Type: text/csv; charset=utf-8`
- `Content-Disposition: attachment; filename="{SYMBOL}_history.csv"`

---

## ✅ Acceptance Criteria
- [ ] `write_history_csv<W: Write>` writes valid CSV with header row (`date,open,high,low,close,volume`).
- [ ] `GET /api/v1/stocks/{symbol}/export.csv` triggers a clean browser file download.
- [ ] `rustock-cli` supports exporting historical data to a file path or `stdout`.
- [ ] Unit tests verify CSV formatting and symbol filename sanitization.
