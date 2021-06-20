package main

import (
	"github.com/daffychuy/jp-open-project/routes"
	"github.com/gin-gonic/gin"
)

func main() {

	r := gin.Default()

	r.NoRoute(func(c *gin.Context) {
		c.JSON(404, gin.H{"code": "PAGE_NOT_FOUND", "message": "Page not found"})
	})

	v1 := r.Group("/api")
	routes.GetWord(v1.Group("/search"))

	r.Run()
}
