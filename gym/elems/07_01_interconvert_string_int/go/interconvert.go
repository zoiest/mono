package interconvert

import (
	"slices"
)

func StringToInteger (input string) int32 {	
	var returnValue int32 = 0
	
	var isNegative bool = false

	runes := []rune(input)
	
	if runes[0] == '-' {
		isNegative = true
	}

	for i := range runes {
		if isNegative && i==0 {
			continue
		}
		digitValue := runes[i] - '0'
		returnValue = returnValue*10 + digitValue
	}
	if isNegative { returnValue = -returnValue }
	return returnValue
}

func IntegerToString(input int32) string {
	if input == 0 { return "0" }
	
	val := int64(input)
	var isNegative bool = false
	if val < 0 {
		isNegative = true
		val = -val
	}

	runes := []rune{}
	for val > 0 {
		runes = append(runes, rune(val % 10) + '0')
		val = val / 10
	}
	
	if isNegative { runes = append(runes, '-') }
	
	slices.Reverse(runes)
	return string(runes)
}
