package main

import (
    "testing"
)

func TestSmallerItem(t *testing.T) {
    x := []int{48, 96, 86, 68, 57, 82, 63, 70, 37, 34, 83, 27, 19, 97, 9, 17}
    v := FindSmaller(x);
    if v != 9 {
        t.Errorf("Expected 9 got %d", v)
    }
}