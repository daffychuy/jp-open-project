package routes

import (
	"github.com/daffychuy/jp-open-project/controllers"
	"github.com/gin-gonic/gin"
)

func GetWord(router *gin.RouterGroup) {
	// /api/search route
	router.GET("/", controllers.SearchWord)
}
