package main

import "fmt"

func main() {
	x := []int{48, 96, 86, 68, 57, 82, 63, 70, 37, 34, 83, 27, 19, 97, 9, 17}
    smaller := FindSmaller(x)
	fmt.Printf("Smaller element: %d\n", smaller)
}

func FindSmaller(numbers []int) int {
	smaller := numbers[0]
	for _, v := range numbers {
		if smaller > v {
			smaller = v
		}
	}
	return smaller
}