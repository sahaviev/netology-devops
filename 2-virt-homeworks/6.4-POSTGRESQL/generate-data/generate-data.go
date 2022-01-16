package main

import (
    "database/sql"
    "crypto/rand"
    "math/big"
    "fmt"
    "github.com/UltiRequiem/lorelai/pkg"
    _ "github.com/lib/pq"
)

const (
    host     = "localhost"
    port     = 5432
    user     = "rail"
    password = "test"
    dbname   = "test_database"
)

func main() {
    psqlconn := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=disable", host, port, user, password, dbname)
    db, err := sql.Open("postgres", psqlconn)
    CheckError(err)
    fmt.Println("Connected!")

    defer db.Close()

    fmt.Println("Start data inserting.")
    for i := 1; i < 1000; i++ {
        price, err := GetRandom(10, 1000)
        CheckError(err)

        wordsCount, err := GetRandom(4, 7)
        CheckError(err)

        phrase := lorelai.LoremWords(wordsCount)

        fmt.Printf("    insert phrase: %s with price %d. \n", phrase, price)

        insertDynStmt := `insert into "orders"("title", "price") values($1, $2)`
        _, err = db.Exec(insertDynStmt, phrase, price)
        CheckError(err)
    }
    fmt.Println("End data inserting.")
}

func GetRandom (min, max int64) (number int, err error) {
    nBig, err := rand.Int(rand.Reader, big.NewInt(max - min))
    return int(nBig.Int64() + min), err
}

func CheckError(err error) {
    if err != nil {
        panic(err)
    }
}