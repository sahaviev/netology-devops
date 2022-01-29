package main

import "fmt"

const FeetsInMeter = 3.28084

func main() {
	fmt.Print("Enter a number: ")
	var input float64
	fmt.Scanf("%f", &input)

	output := input * FeetsInMeter

	fmt.Println(output)
}
