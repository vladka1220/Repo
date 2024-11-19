package parser

import (
	logger "news-service/utils"
	"os"
	"strconv"

	"github.com/robfig/cron/v3"
)

func main() {
	// Инициализируем логгер
	logger.Init()

	// Получаем значение переменной окружения FETCH_INTERVAL
	fetchIntervalStr := os.Getenv("FETCH_INTERVAL")

	// Проверяем, является ли значение пустым
	if fetchIntervalStr == "" {
		logger.Log("ERROR", "FETCH_INTERVAL must be set")
		os.Exit(1)
	}

	// Проверяем, является ли значение допустимым числом
	fetchInterval, err := strconv.Atoi(fetchIntervalStr)
	if err != nil || fetchInterval < 1 {
		logger.Log("ERROR", "FETCH_INTERVAL must be a valid number greater than 0: "+err.Error())
		os.Exit(1)
	}

	c := cron.New()
	cronSchedule := "@" + strconv.Itoa(fetchInterval) + "m"
	_, err = c.AddFunc(cronSchedule, fetchNews) // Запускать парсер каждые FETCH_INTERVAL минут
	if err != nil {
		logger.Log("ERROR", "Failed to add fetchNews to cron: "+err.Error())
		os.Exit(1)
	}
	c.Start()

	logger.Log("INFO", "News parser running...")

	// Чтобы программа не завершалась
	select {}
}
