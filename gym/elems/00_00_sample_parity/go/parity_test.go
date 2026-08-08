package parity

import "testing"

func TestComputeParity(t *testing.T) {
	tests := []struct {
		input uint64
		want  int16
	}{
		{0b1011, 1},
		{0b10001, 0},
		{0, 0},
	}

	for _, tt := range tests {
		got := ComputeParity(tt.input)
		if got != tt.want {
			t.Errorf("ComputeParity(%b) = %d; want %d", tt.input, got, tt.want)
		}
	}
}
