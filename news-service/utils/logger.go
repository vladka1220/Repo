package logger

import (
	"log"
	"os"
)

var logLevel string

// Init initializes the logger by setting the log level from the environment variable.
func Init() {
	logLevel = os.Getenv("LOG_LEVEL")
	if logLevel == "" {
		logLevel = "INFO" // Уровень по умолчанию
	}
}

// Log a message with the specified level.
func Log(level string, msg string) {
	switch level {
	case "DEBUG":
		if logLevel == "DEBUG" {
			log.Printf("[DEBUG] %s", msg)
		}
	case "INFO":
		if logLevel == "INFO" || logLevel == "DEBUG" {
			log.Printf("[INFO] %s", msg)
		}
	case "WARN":
		if logLevel == "INFO" || logLevel == "DEBUG" || logLevel == "WARN" {
			log.Printf("[WARN] %s", msg)
		}
	case "ERROR":
		log.Printf("[ERROR] %s", msg)
	}
}
