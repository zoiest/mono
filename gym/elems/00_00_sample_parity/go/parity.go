package parity

func ComputeParity(x uint64) int16 {
	var result int16
	for x > 0 {
		result ^= int16(x & 1)
		x >>= 1
	}
	return result
}
