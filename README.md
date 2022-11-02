# Sanic app example

REST приложение написанное по требованиям с этого [файла](https://docs.google.com/document/d/1lblqae9k0wdV7q7QFjxYcC_rrDbRb5DIUHtHiKM5iz4/edit).

### Технологии
* Tortoise ORM (PostgreSQL)
* Sanic
* Pydantic
* Линтеры flake8 и mypy
* python-dotenv Для env переменных

### Запуск проекта
1) Установить библиотеки `poetry install`
2) создать `env` файл на основе `env.example` для настройки приложения.
3) Применить миграции приложения `aerich upgrade`

### Описание
Для JWT авторизации используются декораторы как в [доке](https://sanic.dev/en/guide/how-to/authentication.html#auth.py), но умеющие различать админа от обычного пользователя.
