package controllers

import (
	"fmt"
	"strings"

	"github.com/daffychuy/jp-open-project/database"
	"github.com/gin-gonic/gin"
	"github.com/ikawaha/kagome-dict/ipa"
	"github.com/ikawaha/kagome/v2/tokenizer"
)

func SearchWord(c *gin.Context) {
	word := c.Query("word")
	if word == "" {
		c.AbortWithStatus(404)
		return
	}
	t, err := tokenizer.New(ipa.Dict(), tokenizer.OmitBosEos())
	if err != nil {
		c.AbortWithStatus(500)
		panic(err)
	}

	tokens := t.Tokenize(word)
	for _, token := range tokens {
		features := strings.Join(token.Features(), ",")
		fmt.Printf("%s\t%v\n", token.Surface, features)
	}
	fmt.Println(word)
	database.GetWords(word)
}
