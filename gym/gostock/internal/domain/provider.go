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
