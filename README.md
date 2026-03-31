# SPA

Это проект на Django REST Framework (DRF) с интеграцией Docker и Celery.

## Возможности
- Django REST Framework для разработки API
- Celery для асинхронных задач
- Docker и Docker Compose для контейнеризации
- База данных PostgreSQL
- Redis в качестве брокера сообщений

## Требования
- Docker и Docker Compose
- Python 3.13

## Установка
1. Скопируйте .env_example в .env и настройте переменные окружения
2. Соберите контейнеры:
   ```bash
   docker-compose build --no-cache
   ```
3. Запустите сервисы:
   ```bash
   docker-compose up
   ```

## Структура проекта
- `config/` - настройки и URL-адреса проекта Django
- `courses/` - приложение курсов
- `users/` - приложение пользователей
- `docker-compose.yaml` - конфигурация Docker Compose
- `Dockerfile` - конфигурация Docker для веб-сервисов и celery
- `requirements.txt` - зависимости Python

## Документация API
Документация API доступна по следующим адресам после запуска проекта:
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/
- JSON schema: http://localhost:8000/swagger.json

## Разработка
Проект использует лучшие практики, включая форматирование кода (black, isort), линтинг (flake8) и проверку типов (mypy).

## Лицензия
MIT License