# Продуктовый помошнмк foodgram. pre-alpha version 0.0.1

На данном этапе бэк пректа запускается в дебаг режиме, локально, из терминала.
База postgres, фронт и nginx разворачиваются в котейнерах.

Все это сделано для внесения изменений в мой корявый код, который требует проверки.

### Как запустить проект:

1. Клонируем репозиторий.
2. Заходим в папку foodgram-project-react, создаём виртуальное окружение.
3. Устанавливаем все зависимости из backend/requirements.txt
4. Заходим в папку backend и создаём .env файл и заполняем его по примеру:
```
SECRET_KEY="bla-bla-bla-bla-bla-bla-bla-aaaaaaaaaa!!!!!!!!!Отпустите меня поспать немного, спасибо."
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД 
```
5. Переходим в папку foodgram-project-react/infra и выполняем команду поразворачиванию docker-compose 
```
docker-compose up -d --build
```
6. После разворачивания контейнеров снова идем в папку foodgram-project-react/backend и выполняем команды:
    - Выполняем миграции в базу данных.
        ```
        python manage.py migrate
        ```
    - Создаем суперюзара для джанги.
        ```
        python manage.py createsuperuser
        ```
    - Грузим подготовленные данные ингредиентов для рецептов в базу данных.
        ```
        python manage.py load_csv
        ```
    - Стартем сервак джанги.
        ```
        python manage.py runserver
        ```
