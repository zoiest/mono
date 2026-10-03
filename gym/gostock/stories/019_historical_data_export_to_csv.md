# Story 019: Historical Data Export to CSV

## User Story
**As a** quantitative analyst,  
**I want to** export historical stock prices to a downloadable CSV file,  
**So that** I can import stock metrics into spreadsheet or analysis programs.

---

## 📖 Book Alignment
* **Book:** *Go in Practice, Second Edition*
* **Chapters:**
  - Chapter 7: *File access and basic networking* (7.1 Dealing with files, Writing to files)
  - Chapter 10: *Sending and receiving data* (10.2 Sending and receiving data)

---

## 🎯 What You Will Learn
1. Using the `encoding/csv` standard library package.
2. Streaming output directly to an `http.ResponseWriter` without buffering large files in RAM.
3. Setting HTTP download headers (`Content-Disposition: attachment; filename=...`).
4. Working with Go's `io.Writer` interface abstraction.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Build CSV Export Handler
In `internal/server/export.go`:
```go
package server

import (
	"encoding/csv"
	"fmt"
	"net/http"
	"strings"
	"time"
)

func (s *Server) handleExportCSV(w http.ResponseWriter, r *http.Request) {
	symbol := strings.ToUpper(r.PathValue("symbol"))
	history, err := s.aggregator.GetHistorical(r.Context(), symbol, "1d")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "text/csv")
	w.Header().Set("Content-Disposition", fmt.Sprintf(`attachment; filename="%s_history.csv"`, symbol))

	writer := csv.NewWriter(w)
	defer writer.Flush()

	// Write CSV Header
	_ = writer.Write([]string{"Date", "Open", "High", "Low", "Close", "Volume"})

	// Write Data Rows
	for _, row := range history {
		record := []string{
			row.Date.Format(time.DateOnly),
			fmt.Sprintf("%.2f", row.Open),
			fmt.Sprintf("%.2f", row.High),
			fmt.Sprintf("%.2f", row.Low),
			fmt.Sprintf("%.2f", row.Close),
			fmt.Sprintf("%d", row.Volume),
		}
		if err := writer.Write(record); err != nil {
			return
		}
	}
}
```

---

## ✅ Acceptance Criteria
- [ ] `GET /api/v1/stocks/{symbol}/export` prompts a file download.
- [ ] Output CSV parses cleanly in standard CSV tools.
- [ ] Data streams directly with low memory overhead.
