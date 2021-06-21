package database

import (
	"context"
	"fmt"
	"log"

	"github.com/daffychuy/jp-open-project/middleware"
	"go.mongodb.org/mongo-driver/bson"
)

func GetWords(word string) {

	cur, err := middleware.Collection.Find(
		context.Background(),
		bson.M{"Japanese.kana": word})

	if err != nil {
		log.Fatal(err)
	}

	for cur.Next(context.Background()) {
		var result bson.M
		e := cur.Decode(&result)
		if e != nil {
			log.Fatal(e)
		}
		fmt.Println(e)
		fmt.Println(result)

	}
}
