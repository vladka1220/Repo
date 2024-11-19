package api

import (
	"encoding/json"
	"net/http"
	"news-service/parser"
	logger "news-service/utils"
	"strconv"
	"sync"
)

// Импортируем модель из parser/models.go
var (
	newsMu   sync.Mutex    // Мьютекс для синхронизации
	newsList []parser.News // Глобальный список новостей
)

// Обработчик запроса на получение новостей
func getNews(w http.ResponseWriter, r *http.Request) {
	logger.Log("INFO", "Received request for news") // Логируем получение запроса
	newsMu.Lock()                                   // Блокируем доступ к новостям
	defer newsMu.Unlock()                           // Освобождаем после завершения

	w.Header().Set("Content-Type", "application/json")

	if len(newsList) == 0 {
		logger.Log("INFO", "No news available")                  // Логируем, если новостей нет
		http.Error(w, "No news available", http.StatusNoContent) // Возвращаем 204 No Content
		return
	}

	if err := json.NewEncoder(w).Encode(newsList); err != nil {
		logger.Log("ERROR", "Failed to encode news: "+err.Error())             // Логируем ошибку при кодировании
		http.Error(w, "Failed to encode news", http.StatusInternalServerError) // Отправляем ошибку клиенту
		return
	}

	logger.Log("INFO", "Successfully returned news count: "+strconv.Itoa(len(newsList))) // Логируем количество возвращенных новостей
}
