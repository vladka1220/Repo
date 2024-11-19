# Этап 1: Сборка приложения
FROM golang:1.23.2 AS build
WORKDIR /app

# Копируем go.mod и go.sum для кэширования зависимостей
COPY go.mod go.sum ./
RUN go mod download

# Копируем остальную часть кода
COPY . .

# Компилируем приложение
RUN CGO_ENABLED=0 GOOS=linux go build -o news-service .

# Этап 2: Финальная сборка
FROM alpine:latest
WORKDIR /app

# Копируем собранное приложение из этапа сборки
COPY --from=build /app/news-service .

# Установка переменной окружения для порта
ENV PORT=8080

# Экспонируем порт
EXPOSE 8080

# Запуск приложения
ENTRYPOINT ["./news-service"]
