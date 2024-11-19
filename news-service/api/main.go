package api

import (
	"net/http"
	logger "news-service/utils"
)

func main() {
	setupRoutes()                                     // Настраиваем маршруты
	logger.Log("INFO", "API server running on :8080") // Логируем сообщение о запуске сервера

	// Запуск сервера с обработчиком маршрутов
	err := http.ListenAndServe(":8080", nil) // Запуск сервера
	if err != nil {
		logger.Log("ERROR", "Error starting server: "+err.Error()) // Логируем ошибку при запуске
	}
}
