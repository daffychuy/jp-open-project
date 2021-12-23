package controllers

import (
	"fmt"
	"strings"

	jp "github.com/daffychuy/japanese"
	"github.com/gin-gonic/gin"
	"github.com/ikawaha/kagome-dict/ipa"
	"github.com/ikawaha/kagome/v2/tokenizer"
)

func SearchWord(c *gin.Context) {
	word := c.Query("word")
	if word == "" {
		c.JSON(200, "")
	}

	// Tokenize the word first using IPA
	t, err := tokenizer.New(ipa.Dict(), tokenizer.OmitBosEos())
	if err != nil {
		c.AbortWithStatus(500)
		panic(err)
	}

	tokens := t.Tokenize(word)
	fmt.Println(tokens[0].Pronunciation())
	for _, token := range tokens {
		features := strings.Join(token.Features(), ",")
		fmt.Printf("%s\t%v\n", token.Surface, features)
	}
	fmt.Println(word)

	godan, ichiban := jp.DictionaryForm(word)
	fmt.Println(godan)
	fmt.Println(ichiban)

	// Return data
	// c.JSON(200, database.GetWords(word))
}
