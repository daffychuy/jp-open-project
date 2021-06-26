package database

import (
	"context"
	"log"

	"github.com/daffychuy/jp-open-project/middleware"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
)

func GetWords(word string) []primitive.M {

	cur, err := middleware.Collection.Find(
		context.Background(),
		bson.M{"Japanese.kanji": word})

	if err != nil {
		log.Fatal(err)
	}

	var data []bson.M
	if err = cur.All(context.Background(), &data); err != nil {
		log.Fatal(err)
	}

	return data
}
