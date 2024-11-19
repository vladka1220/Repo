package parser

import (
	logger "news-service/utils"
	"os"
	"strings"
	"sync"

	"github.com/gocolly/colly/v2"
)

const maxNews = 100 // Максимальное количество новостей для хранения

// Глобальный список новостей и мьютекс для синхронизации доступа
var (
	newsMu   sync.Mutex // Мьютекс для синхронизации
	newsList []News     // Глобальный список новостей
)

// Функция для добавления новости с удалением старых
func addNews(news News) {
	newsMu.Lock()         // Синхронизируем доступ к списку
	defer newsMu.Unlock() // Освобождаем мьютекс после завершения

	if len(newsList) >= maxNews {
		newsList = newsList[1:] // Удаляем первую новость, если список переполнен
	}
	newsList = append(newsList, news) // Добавляем новую новость
}

// Функция для парсинга новостей с сайтов
func fetchNews() {
	c := colly.NewCollector()

	c.OnHTML("article", func(e *colly.HTMLElement) {
		news := News{
			Title:       e.ChildText("h2 a"),
			Description: e.ChildText("p"),
			Source:      e.Request.URL.Hostname(),
		}
		addNews(news)                                   // Сохраняем новость в список
		logger.Log("INFO", "Fetched news: "+news.Title) // Логируем новость
	})

	// Получаем список сайтов для парсинга из переменной окружения
	urls := os.Getenv("NEWS_URLS")
	if urls == "" {
		logger.Log("ERROR", "NEWS_URLS environment variable is not set")
		return
	}

	// Разделяем URL-адреса по запятой
	urlList := strings.Split(urls, ",")

	// Проходим по каждому URL и запускаем парсинг
	for _, url := range urlList {
		// Проверяем статус ответа и логируем
		err := c.Visit(url)
		if err != nil {
			logger.Log("ERROR", "Error visiting URL: "+url+", error: "+err.Error())
		} else {
			logger.Log("INFO", "Visited URL: "+url) // Логируем успешный визит
		}
	}
}
