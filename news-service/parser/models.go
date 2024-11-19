package parser

// News представляет структуру для хранения информации о новости.
type News struct {
	Title       string `json:"title"`       // Заголовок новости
	Description string `json:"description"` // Описание новости
	Source      string `json:"source"`      // Источник новости
}
