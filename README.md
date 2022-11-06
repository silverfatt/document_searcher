# Поисковик по текстам документов

## Эндпоинты
- `/` - проверить, что API запущен
- `/add` - добавить документ
- `/delete` - удалить документ
- `/search` - найти документ по тексту (за отсутствием явных требований поиск делается по вхождению одного слова)

## Технологии

- Фреймворк для бэкенда - `FastAPI`
- СУБД - `PostgreSQL`
- Поисковая машина - `ElasticSearch`
- Тесты - `PyTest`

## Запуск проекта

### При помощи докера

Ввести в терминал `docker-compose up`, находясь в корне проекта.

Запустятся 3 контейнера: с приложением, PostgreSQL и ElasticSearch.

Затем необходимо перейти по ссылке http://127.0.0.1:8000/docs

### Без помощи докера

Сначала устанавливаем зависимости: `pip install -r requirements.txt`

Далее необходимо запустить сервера PostgreSQL и ElasticSearch, а также указать следующие переменные окружения (`set` для Windows или `export` для Linux):

- `DB_NAME` - название базы данных, например, `documents`
- `DB_USER` - пользователь базы данных, например, `postgres`
- `DB_PASSWORD` - пароль пользователя, например, `qwerty123`
- `DB_HOST` - хост базы данных, например, `localhost`
- `ES_HOST` - хост ElasticSearch, например, `localhost` 

Создавать вручную какие-либо таблицы в БД или индексы в ES не обязательно.

## Тесты

Для запуска тестов необходимы работающие сервера PostgreSQL и ElasticSearch. Необходимо указать переменные окружения (см. `Без помощи докера`).

Тесты запускаются из корня проекта командой `pytest -v tests`.

Тесты автоматически очищают БД и ES после своей работы.
