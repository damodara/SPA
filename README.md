# SPA

Проект на Django REST Framework с Celery. Деплой реализован в одном сценарии: **Docker Compose**.

## Стек
- Django + DRF
- PostgreSQL
- Redis
- Celery worker + Celery beat
- Nginx (reverse proxy)
- Docker / Docker Compose

## Локальный запуск (Docker Compose)
1. Создайте файл окружения:
   ```bash
   cp .env_example .env
   ```
2. Заполните переменные в `.env` (`SECRET_KEY`, `POSTGRES_*`, `STRIPE_*`).
3. Соберите и поднимите сервисы:
   ```bash
   docker compose build --pull
   docker compose up -d
   ```
4. Примените миграции и соберите статику:
   ```bash
   docker compose exec -T web python manage.py migrate
   docker compose exec -T web python manage.py collectstatic --noinput
   ```
5. Проверка:
   ```bash
   docker compose ps
   ```

API доступно через Nginx: `http://localhost/`  
Swagger: `http://localhost/swagger/`  
ReDoc: `http://localhost/redoc/`

## Что делает `docker-compose.yaml`
- `web`: Django в gunicorn
- `nginx`: проксирование в `web`, раздача `static`/`media`
- `db`: PostgreSQL
- `redis`: broker/result backend
- `celery`, `celery_beat`: фоновые задачи

## CI/CD (GitHub Actions)
Workflow: `.github/workflows/test_and_deploy.yml`

### Этап test
- Поднимает PostgreSQL service в GitHub Actions
- Ставит зависимости
- Запускает `python manage.py test`

### Этап deploy (Docker Compose over SSH)
После успешных тестов workflow:
1. Подключается по SSH на сервер
2. Обновляет `.env` на сервере из секрета `APP_ENV_FILE`
3. Делает `git pull`
4. Выполняет:
   ```bash
   docker compose pull || true
   docker compose build --pull
   docker compose up -d --remove-orphans
   docker compose exec -T web python manage.py migrate
   docker compose exec -T web python manage.py collectstatic --noinput
   docker compose ps
   ```

## Секреты GitHub для деплоя
Обязательные:
- `SERVER_IP` — IP сервера
- `SSH_USER` — SSH пользователь
- `SSH_KEY` — приватный ключ (не `.pub`)
- `DEPLOY_DIR` — директория проекта на сервере
- `APP_ENV_FILE` — содержимое серверного `.env` целиком (многострочный secret)


## Подготовка сервера
На сервере должны быть установлены:
- Docker Engine
- Docker Compose plugin
- Git

Первичная подготовка:
```bash
mkdir -p /path/to/project
cd /path/to/project
git clone <your-repo-url> .
```
Дальше деплой выполняется автоматически workflow.