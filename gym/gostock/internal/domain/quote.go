package domain

import "time"

type Quote struct {
	Symbol        string       `json:"symbol"`
	CompanyName   string       `json:"company_name,omitempty"`
	Price         float64      `json:"price"`
	PreviousClose float64      `json:"previous_close,omitempty"`
	Open          float64      `json:"open,omitempty"`
	DayHigh       float64      `json:"day_high:omitempty"`
	DayLow        float64      `json:"day_low,omitempty"`
	Volume        int64        `json:"volume,omitempty"`
	Provider      ProviderType `json:"provider"`
	UpdateAt      time.Time    `json:"update_at"`
}

func (q Quote) Change() float64 {
	if q.PreviousClose == 0 {
		return 0
	}
	return q.Price - q.PreviousClose
}

func (q Quote) ChangePercent() float64 {
	if q.PreviousClose == 0 {
		return 0
	}
	return (q.Change() / q.PreviousClose) * 100
}
