# Сервис бонусов за траты

Этот README содержит инструкции по запуску и проверке работоспособности REST-сервиса для бонусной программы. В приложении использован FastAPI для реализации API и SQLAlchemy для работы с базой данных.

## Клонирование репозитория

1. Склонируйте репозиторий с GitHub:
    ```sh
    git clone <URL репозитория>
    cd <название репозитория>
    ```

## Установка зависимостей

Для управления зависимостями используется Poetry. Установите его, если он еще не установлен, и установите зависимости проекта:

1. Установите Poetry (если его еще нет):
    ```sh
    pip install poetry
    ```

2. Установите зависимости проекта с помощью Poetry:
    ```sh
    poetry install
    ```

## Запуск сервиса локально

Для запуска сервиса локально используется uvicorn:

1. Запустите сервер с помощью uvicorn:
    ```sh
    poetry run uvicorn dop_zhu_zad.main:app --reload
    ```

Сервер будет доступен по адресу `http://127.0.0.1:8000`.

## Сборка и запуск контейнера Docker

Вы также можете запустить приложение в контейнере Docker. В репозитории уже есть Dockerfile для сборки контейнера.

1. Соберите Docker-образ:
    ```sh
    docker build -t bonus-service .
    ```

2. Запустите Docker-контейнер:
    ```sh
    docker run -d -p 8000:8000 bonus-service
    ```

Сервер будет доступен по адресу `http://127.0.0.1:8000`.

## Тестирование функциональности с помощью curl

После запуска сервера или контейнера Docker, вы можете использовать `curl` для отправки запросов к API.

### Регистрация нового пользователя

```sh
curl -X POST "http://127.0.0.1:8000/users/" -H "Content-Type: application/json" -d '{
    "username": "testuser",
    "password": "testpassword"
}'
```

### Получение токена доступа

```sh
TOKEN=$(curl -X POST "http://127.0.0.1:8000/token" -H "Content-Type: application/x-www-form-urlencoded" -d 'username=testuser&password=testpassword' | jq -r '.access_token')
echo "Полученный токен: $TOKEN"
```

### Получение данных о бонусной программе

```sh
curl -X GET "http://127.0.0.1:8000/bonus" -H "Authorization: Bearer $TOKEN"
```

### Регистрация траты

```sh
curl -X POST "http://127.0.0.1:8000/transactions/" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{
    "amount": 1200.0
}'
```

Проверьте ответы на каждую команду, чтобы убедиться в корректной работе сервиса.