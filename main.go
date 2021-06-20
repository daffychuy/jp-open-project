package main

import (
	"github.com/daffychuy/jp-open-project/routes"
	"github.com/gin-gonic/gin"
)

func main() {
	r := gin.Default()
	v1 := r.Group("/api")
	routes.GetWord(v1.Group("/search"))

	r.Run()
}
