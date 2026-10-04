package domain

import (
	"encoding/json"
	"math"
	"strings"
	"testing"
)

func TestQuote_ChangeAndPercent(t *testing.T) {
	tests := []struct {
		name          string
		quote         Quote
		wantChange    float64
		wantChangePct float64
	}{
		{
			name: "gain in price",
			quote: Quote{
				Price:         110.0,
				PreviousClose: 100.0,
			},
			wantChange:    10.0,
			wantChangePct: 10.0,
		},
		{
			name: "loss in price",
			quote: Quote{
				Price:         90.0,
				PreviousClose: 100.0,
			},
			wantChange:    -10.0,
			wantChangePct: -10.0,
		},
		{
			name: "zero previous close (avoid division by zero)",
			quote: Quote{
				Price:         100.0,
				PreviousClose: 0.0,
			},
			wantChange:    0.0,
			wantChangePct: 0.0,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			gotChange := tt.quote.Change()
			if math.Abs(gotChange-tt.wantChange) > 1e-9 {
				t.Errorf("Change() = %v, want %v", gotChange, tt.wantChange)
			}

			gotChangePct := tt.quote.ChangePercent()
			if math.Abs(gotChangePct-tt.wantChangePct) > 1e-9 {
				t.Errorf("ChangePercent() = %v, want %v", gotChangePct, tt.wantChangePct)
			}
		})
	}
}

func TestQuote_JSONMarshaling(t *testing.T) {
	t.Run("omits empty fields", func(t *testing.T) {
		q := Quote{
			Symbol:   "AAPL",
			Price:    150.0,
			Provider: ProviderYahoo,
		}

		data, err := json.Marshal(q)
		if err != nil {
			t.Fatalf("json.Marshal failed: %v", err)
		}

		jsonStr := string(data)

		if !strings.Contains(jsonStr, `"symbol":"AAPL"`) {
			t.Errorf("expected JSON to contain symbol, got: %s", jsonStr)
		}

		if strings.Contains(jsonStr, "company_name") {
			t.Errorf("expected company_name to be omitted, got: %s", jsonStr)
		}
		if strings.Contains(jsonStr, "volume") {
			t.Errorf("expected volume to be omitted, got: %s", jsonStr)
		}

	})

	t.Run("unmarshaling", func(t *testing.T) {
		rawJSON := `{
                "symbol": "MSFT",
                "company_name": "Microsoft Corp",
                "price": 310.5,
                "previous_close": 305.0,
                "provider": 1}`
		var q Quote
		if err := json.Unmarshal([]byte(rawJSON), &q); err != nil {
			t.Fatalf("json.Unmarshal failed : %v", err)
		}

		if q.Symbol != "MSFT" || q.CompanyName != "Microsoft Corp" || q.Price != 310.5 {
			t.Errorf("unmarshaled values do not match, got: %+v", q)
		}
	})
}
