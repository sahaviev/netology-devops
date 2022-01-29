package main

import "fmt"

const Total = 100

func main() {
    slice := GenerateMod3Slice(Total)
    fmt.Printf("%v\n", slice)
}

func GenerateMod3Slice(total int) []int {
	var numbers []int
	for i := 1; i < total; i++ {
		if i%3 == 0 {
            numbers = append(numbers, i)
		}
	}
	return numbers
}
