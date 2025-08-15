# OpenSearch Demo

Демонстрационное приложение для работы с OpenSearch, реализующее поиск по документам с фильтрацией по типу контента.

## Функциональность

- Создание индекса в OpenSearch с полями:
  - title (текст)
  - content (текст)
  - content_type (4 варианта: article, blog, news, review)
- Генерация и загрузка тестовых документов
- Поиск по ключевому слову в полях title и content
- Фильтрация результатов по типу контента
- Веб-интерфейс для удобного поиска

## Требования

- Docker
- Docker Compose

## Запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/ViPERxds/test.git
cd test
```

2. Запустите приложение с помощью Docker Compose:
```bash
docker-compose up --build
```

3. Откройте браузер и перейдите по адресу: http://localhost:5000

4. Нажмите кнопку "Инициализировать данные" для создания индекса и загрузки тестовых данных

5. Используйте поисковую строку и фильтры для поиска документов

## Структура проекта

- `app.py` - основной файл приложения с бэкендом на Flask
- `templates/index.html` - шаблон веб-интерфейса
- `docker-compose.yml` - конфигурация Docker Compose
- `Dockerfile` - конфигурация Docker для веб-приложения
- `requirements.txt` - зависимости Python

## Технологии

- Python 3.9
- Flask
- OpenSearch
- Docker
- HTML/CSS/JavaScript