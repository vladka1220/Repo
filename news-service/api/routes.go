package api

import (
	"net/http"
	"os"
	"strings"

	logger "news-service/utils"

	"github.com/gorilla/csrf"
	"github.com/gorilla/handlers"
)

// Инициализация CORS и CSRF middleware
var (
	trustedOrigins = os.Getenv("CSRF_TRUSTED_ORIGINS")
	CSRF           = csrf.Protect([]byte("32-byte-long-secret"), csrf.TrustedOrigins(strings.Split(trustedOrigins, ",")))
	CORS           = handlers.CORS(
		handlers.AllowedOrigins(strings.Split(os.Getenv("CORS_ALLOWED_ORIGINS"), ",")),
		handlers.AllowedMethods(strings.Split(os.Getenv("CORS_ALLOW_METHODS"), ",")),
		handlers.AllowedHeaders(strings.Split(os.Getenv("CORS_ALLOW_HEADERS"), ",")),
		handlers.AllowCredentials(), // Без аргумента, как должно быть
	)
)

// LogRequestMiddleware логирует информацию о каждом входящем запросе.
func LogRequestMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		logger.Log("INFO", "Received request: "+r.Method+" "+r.URL.Path) // Логируем запрос
		next.ServeHTTP(w, r)                                             // Используем ServeHTTP, так как next — это http.Handler
	})
}

// Определяем маршруты для API
func setupRoutes() {
	http.Handle("/news", LogRequestMiddleware(CORS(CSRF(http.HandlerFunc(getNews)))))
}
