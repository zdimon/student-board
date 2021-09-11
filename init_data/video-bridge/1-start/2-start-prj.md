# Старт проекта.
      
Создаем Dockerfile.

    FROM python:3.8-alpine3.12 AS python38
    ENV PYTHONUNBUFFERED 1
    RUN mkdir /app
    WORKDIR /app
    RUN apt update
    RUN apt -y install libpq-dev netcat
    COPY requirements.txt /app
    RUN /usr/local/bin/python -m pip install --upgrade pip
    RUN pip install -r requirements.txt
    RUN mkdir /entry
    COPY entrypoint.sh /entry
    ENTRYPOINT ["/entry/entrypoint.sh"]

3.8-alpine3.12 - тег образа

[ссылка на документацию](https://hub.docker.com/_/python)

Пробуем собрать.

    docker build .

В данном случае alpine не имеет установщика apt, это сильно урезанная версия Linux.

Пример как ставить в него программы.

    RUN apk add wget bash

Мы будем использовать образ python:3.8-buster на основе Debian.

    FROM python:3.8-buster AS python38
    ENV PYTHONUNBUFFERED 1
    RUN mkdir /app
    WORKDIR /app
    RUN apt update
    RUN apt -y install libpq-dev netcat
    COPY requirements.txt /app
    RUN /usr/local/bin/python -m pip install --upgrade pip
    RUN pip install -r requirements.txt
    RUN mkdir /entry
    COPY entrypoint.sh /entry
    ENTRYPOINT ["/entry/entrypoint.sh"]


Создаем файл requirements.txt

    Django

Создаем файл entrypoint.sh

    #!/bin/sh

    while :
    do
        sleep 5
        echo "Ok"
    done


Собираем контейнер и тагируем его чтоб было легче запускать по тегу.

    docker build -t python-test .

Пытаемся запустить.


    ❯ docker run python-test
    docker: Error response from daemon: OCI runtime create failed: container_linux.go:349: starting container process caused "exec: \"/entry/entrypoint.sh\": permission denied": unknown.
    ❯ docker run python-test
    docker: Error response from daemon: OCI runtime create failed: container_linux.go:349: starting container process caused "exec: \"/entry/entrypoint.sh\":

Отметим entrypoint.sh как исполняемый.

    chmod +x entrypoint.sh

Сбилдим еще раз и поднимем контейнер.

    docker build -t python-test .
    docker run python-test

Создадим файл docker-compose.yaml для упрощения запуска и сборки контейнеров.

    version: '3.5'
    services: 
        webrtc-django:
            build: .
            ports:
                - 8000:8000
            working_dir: /app
            container_name: webrtc-server
            networks: 
                - webrtc_network


    networks:
        webrtc_network:
            driver: bridge
        
Поднимаем контейнера 

    docker-compose up

## Создание и запуск проекта Django

Для создания заготовки проекта создадим виртуальное окружение и активируем его.

    python3 -m venv venv
    . ./venv/bin/activate

Установим Django.

    pip install Django

Стартуем проект, создаем БД и запускаем сервер разработки.

    django-admin startproject app
    cd app
    ./manage.py migrate
    ./manage.py runserver 0.0.0.0:8181

Если вы будете использовать исключительно докер при разработке то папку venv теперь можно удалить. Она нам была нужна только для старта проекта и сосдания папки с начальными файлами.

Прокинем локальную папку app внутрь контейнера и порты.

    version: '3.5'
    services: 
        webrtc-django:
           ....
            volumes:
                - ./app:/app

            ports:
                - 8181:8181


Изменим entrypoint.sh где запустим джанго-сервер внутри контейнера.

    #!/bin/sh

    ./manage.py runserver 0.0.0.0:8181

    # while :
    # do
    #     sleep 5
    #     echo "Ok"
    # done

Перезапустим контейнер с флагом --build чтобы его пересобрать.


    docker-compose up --build

Можно запускать команду внутри контейнера через docker-compose.yaml, а не через entrypoin.sh

    version: '3.5'
    services: 
        webrtc-django:
            build: .
            ports:
                - 8000:8000
            working_dir: /app
            container_name: webrtc-server
            command: python manage.py runserver 0.0.0.0:8181

        ...

Или так

    command: '/entry/entrypoint.sh'






