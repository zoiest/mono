# Story 002: Domain Models, Struct Tags & Enums

## User Story
**As a** financial application developer,
**I want to** define core domain models (`Quote`, `HistoricalPrice`, `CompanyProfile`, `ProviderType`),
**So that** stock data can be serialized to and from JSON with strict type safety, validation, and business methods.

---

## 📖 Book Alignment
* **Book:** *Go in Practice, Second Edition*
* **Chapters:**
  - Chapter 2: *A solid foundation: Building a command-line application* (2.1 Defining valid values via enums)
  - Chapter 3: *Structs, interfaces, and generics* (3.1 Using structs to represent data, anonymous identifiers, tags in structs, encoding data in JSON format; 3.4 Simplifying code with generics)

---

## 🎯 What You Will Learn
1. Defining strongly typed enums using `type` and `iota`.
2. Implementing the `fmt.Stringer` interface (`String()` method) on custom types.
3. Struct tags (`json:"..."`) and controlling JSON marshaling behavior (e.g. `omitempty`).
4. Writing receiver methods (value vs. pointer receivers).
5. Using generics to constrain numeric operations on prices and volume.

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Define Enums with `iota`
In `internal/domain/provider.go`:
```go
package domain

import "fmt"

type ProviderType int

const (
	ProviderUnknown ProviderType = iota
	ProviderYahoo
	ProviderFinviz
	ProviderMock
)

func (p ProviderType) String() string {
	switch p {
	case ProviderYahoo:
		return "yahoo"
	case ProviderFinviz:
		return "finviz"
	case ProviderMock:
		return "mock"
	default:
		return "unknown"
	}
}

func ParseProviderType(s string) (ProviderType, error) {
	switch s {
	case "yahoo":
		return ProviderYahoo, nil
	case "finviz":
		return ProviderFinviz, nil
	case "mock":
		return ProviderMock, nil
	default:
		return ProviderUnknown, fmt.Errorf("unknown provider: %s", s)
	}
}
```

### 2. Define Structs with Tags and Methods
In `internal/domain/quote.go`:
```go
package domain

import (
	"time"
)

type Quote struct {
	Symbol        string       `json:"symbol"`
	CompanyName   string       `json:"company_name,omitempty"`
	Price         float64      `json:"price"`
	PreviousClose float64      `json:"previous_close,omitempty"`
	Open          float64      `json:"open,omitempty"`
	DayHigh       float64      `json:"day_high,omitempty"`
	DayLow        float64      `json:"day_low,omitempty"`
	Volume        int64        `json:"volume,omitempty"`
	Provider      ProviderType `json:"provider"`
	UpdatedAt     time.Time    `json:"updated_at"`
}

// Change returns absolute price change.
func (q Quote) Change() float64 {
	if q.PreviousClose == 0 {
		return 0
	}
	return q.Price - q.PreviousClose
}

// ChangePercent returns the percentage price change.
func (q Quote) ChangePercent() float64 {
	if q.PreviousClose == 0 {
		return 0
	}
	return (q.Change() / q.PreviousClose) * 100
}
```

### 3. Add Historical Data Model
In `internal/domain/historical.go`:
```go
package domain

import "time"

type HistoricalPrice struct {
	Date   time.Time `json:"date"`
	Open   float64   `json:"open"`
	High   float64   `json:"high"`
	Low    float64   `json:"low"`
	Close  float64   `json:"close"`
	Volume int64     `json:"volume"`
}
```

---

## ✅ Acceptance Criteria
- [X] `ProviderType` implements `fmt.Stringer` and a parsing function.
- [X] `Quote` struct includes JSON tags and methods for `Change()` and `ChangePercent()`.
- [X] Unit tests in `internal/domain/quote_test.go` verify math calculations and JSON marshaling.
