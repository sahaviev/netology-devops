package main

import "testing"

func TestMeterToFeets(t *testing.T) {
    v := MeterToFeets(1);
    if v != 3.28084 {
        t.Error("Expected 3.28084 got ", v)
    }
}