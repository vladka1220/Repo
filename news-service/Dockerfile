# Этап 1: Сборка приложений
FROM golang:1.23 AS build
WORKDIR /app

# Копируем go.mod и go.sum для кэширования зависимостей
COPY go.mod go.sum ./
RUN go mod download

# Копируем исходный код
COPY . .

# Компилируем приложение из папки api
WORKDIR /app/api
RUN CGO_ENABLED=0 GOOS=linux go build -o /app/news-service-api .

# Компилируем приложение из папки parser
WORKDIR /app/parser
RUN CGO_ENABLED=0 GOOS=linux go build -o /app/news-service-parser .

# Этап 2: Финальная сборка
FROM alpine:latest
WORKDIR /app

# Копируем оба собранных приложения из этапа сборки
COPY --from=build /app/news-service-api .
COPY --from=build /app/news-service-parser .

# Установка переменной окружения для порта
ENV PORT=8080

# Экспонируем порт
EXPOSE 8080

# Запуск приложения
ENTRYPOINT ["./news-service"]
