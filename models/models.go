package models

import (
	"go.mongodb.org/mongo-driver/bson/primitive"
)

type JMDict struct {
	ID        primitive.ObjectID `json:"_id" bson:"_id"`
	JMdict_id string             `json:"JMdict_id"`
	Japanese  []Reading          `json:"Japanese"`
	Sense     []string           `json:"sense"`
}

type Reading struct {
	Kanji        string `json:"kanji,omitempty"`
	Kana         string `json:"kana,omitempty"`
	Kanji_Common string `json:"kanji_common,omitempty"`
	Kana_Common  string `kson:"kana_common,omitempty"`
}

type Sense struct {
	PartsOfSpeech  []string     `json:"partsOfSpeech"`
	AppliesToKanji []string     `json:"appliesToKanji"`
	AppliesToKana  []string     `json:"appliesToKana"`
	Related        []string     `json:"related"`
	Antonym        []string     `json:"antonym"`
	Field          []string     `json:"field"`
	Dialect        []string     `json:"dialect"`
	Misc           []string     `json:"misc"`
	Info           []string     `json:"info"`
	LanguageSource []LangSource `json:"languageSource"`
	Gloss          []gloss      `json:"gloss"`
}

type LangSource struct {
	Lang  string `json:"lang"`
	Wasei bool   `json:"wasei"`
	Text  string `json:"text"`
}

type gloss struct {
	Lang string `json:"lang"`
	Type string `json:"type"`
	Text string `json:"text"`
}
