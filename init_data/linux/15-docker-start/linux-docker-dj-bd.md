# Джаного и база данных с Doker.

[источник](https://webdevblog.ru/kak-ispolzovat-django-postgresql-i-docker/)

## Создаем новый проект.

Файл зависимостей requirements.txt

    Django
    psycopg2

Установка ВО и зависимостей.

![doker]({path-to-subject}/images/12.png)

Старт проекта и сервера.

![doker]({path-to-subject}/images/13.png)

В данном случае мы не применяли миграцию и база данных не была создана.

Теперь задача состоит в том, чтобы не использовать папку venv а установить зависимости внутри образа Docker. 

При этом сделав так, чтобы все файлы проекта оставались в локальной области для разработки и не переносились внутрь контейнера.

Таким образом все что служит для запуска проекта (окружение) будет изолировано внутри контейнера.

Создадим файл Dockerfile.

    FROM python:3.6 AS django
    ENV PYTHONUNBUFFERED 1
    RUN mkdir /app
    WORKDIR /app
    RUN apt update
    RUN apt -y install libpq-dev
    COPY requirements.txt /app
    RUN pip install -r requirements.txt



**ENV PYTHONUNBUFFERED 1** - приказывает python выводить все в терминал  


Запускаем сборку образа

    docket build .

и наблюдаем процесс

![doker]({path-to-subject}/images/14.png)

Видим что просит обновить инсталятор pip.

![doker]({path-to-subject}/images/15.png)

Добавим команду обновления как просит.

    ...
    COPY requirements.txt /app
    RUN /usr/local/bin/python -m pip install --upgrade pip
    RUN pip install -r requirements.txt

Теперь наша задача запустить образ в контейнере.

Проще всего это слеать через docker-compose up.

Для этого нужен конфигурационный файл docker-compose.yaml.

    version: '3.5'
    services: 
        django:
            build: .
            restart: always
            ports:
                - 8000:8080

Запускаем команду сборки и запуска контейнера.

    docker-compose up

![doker]({path-to-subject}/images/16.png)

Теперь нам нужно запустить несколько команд внутри контейнера чтобы поднять веб-сервер с джанго проектом.

Так же нам необходимо сделать ссылку внутри контейнера на наш каталог с проектом снаружи.

    version: '3.5'
    services: 
        django:
            build: .
            restart: always
            ports:
                - 8000:8000
            working_dir: /app
            command: python manage.py runserver 0.0.0.0:8000
            volumes:
                - ./blog:/app

Добавим контейнер с PostgreSQL.


    db:
        restart: always
        image: postgres:latest
        ports:
            - "5432:5432"
        volumes:
            - ./pg_data:/var/lib/postgresql/data/
        environment:
            - POSTGRES_USER=postgres
            - POSTGRES_PASSWORD=1q2w3e
            - POSTGRES_DB=blog

Теперь добавим файл настроек окружения для проекта .env.dev

    DEBUG=1
    SECRET_KEY=foo
    DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
    SQL_ENGINE=django.db.backends.postgresql
    SQL_DATABASE=blog
    SQL_USER=postgres
    SQL_PASSWORD=1q2w3e
    SQL_HOST=db
    SQL_PORT=5432

Включим его в контейнер.

    version: '3.5'
    services: 
        django:
            ...
            env_file:
                - ./.env.dev

И пропишем коннект в settings.py

    DATABASES = {
        "default": {
            "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
            "NAME": os.environ.get("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
            "USER": os.environ.get("SQL_USER", "user"),
            "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
            "HOST": os.environ.get("SQL_HOST", "localhost"),
            "PORT": os.environ.get("SQL_PORT", "5432"),
        }
    }

Пересобираем контейнеры.

    docker-compose up --build

Проводим миграцию.

    docker-compose exec django python manage.py migrate --noinput

## Точка входа для образа

Используется для запуска скрипта при каждом запуске образа.

Например если мы хотим применять миграцию каждый раз, когда запускаем образ создадим файл entrypoint.sh.

    #!/bin/sh

    if [ "$DATABASE" = "postgres" ]
    then
        echo "Waiting for postgres..."

        while ! nc -z $SQL_HOST $SQL_PORT; do
          sleep 0.1
        done

        echo "PostgreSQL started"
    fi

    python manage.py flush --no-input
    python manage.py migrate

    exec "$@"

И хобавим его в образ.

    FROM python:3.6 AS python36
    ...
    RUN mkdir /entry
    COPY entrypoint.sh /entry
    ENTRYPOINT ["/entry/entrypoint.sh"]

### Если нужно использовать разные Dockerfile для контейнеров.

    services:
      service1:
        build:
            context: .
            args:
                - NODE_ENV=local
            dockerfile: Dockerfile_X
        ports:
            - "8765:8765"



### Полезные команды

Удаление контейнеров.
    
    docker-compose down -v
    
Просмотр списка запущенных контейнеров

    docker ps
    
Удалить контейнер 

    docker-compose rm db
    



