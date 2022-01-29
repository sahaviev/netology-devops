package main

import "fmt"

const Total = 100

func main() {
	for i := 1; i < Total; i++ {
		if i%3 == 0 {
			fmt.Printf("%d\n", i)
		}
	}
}
