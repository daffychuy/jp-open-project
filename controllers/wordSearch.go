package controllers

import (
	"fmt"

	"github.com/gin-gonic/gin"
)

func SearchWord(c *gin.Context) {
	word := c.Param("word")
	fmt.Println(word)
}
