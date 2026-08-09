package interconvert

import (
	"testing"
	"math"
)


func TestInterconvertStringToInteger(t *testing.T) {
	tests := []struct {
		input string
		expectedValue int32
	}{
		{"0", 0},
		{"123", 123},
		{"-123", -123},
		{"2147483647", math.MaxInt32},
		{"-2147483648", math.MinInt32},		
	}

	for _, tt := range tests {
		returnValue := StringToInteger(tt.input)
		if returnValue != tt.expectedValue {
			t.Errorf("StringToInteger(%s) = %d; expected value %d",
				tt.input, returnValue, tt.expectedValue,
			)
		}
	}
}

func TestInterconvertIntegerToString(t *testing.T) {
	tests := []struct {
		input int32
		expectedValue string
	}{
		{0, "0"},
		{123, "123"},
		{-123, "-123"},
		{math.MaxInt32, "2147483647"},
		{math.MinInt32, "-2147483648"},
	}

	for _, tt := range tests {
		returnValue := IntegerToString(tt.input)
		if returnValue != tt.expectedValue {
			t.Errorf("IntegerToString(%d) = %s; expected value %s",
				tt.input, returnValue, tt.expectedValue,
			)
		}
	}
}
