package models

import (
	"go.mongodb.org/mongo-driver/bson/primitive"
)

type JMDict struct {
	ID        primitive.ObjectID `json:"_id,omitempty" bson:"_id,omitempty"`
	JMdict_id string             `json:"JMdict_id,omitempty"`
	Japanese  []string           `json:"Japanese,omitempty"`
	Sense     []string           `json:"sense,omitempty"`
}
