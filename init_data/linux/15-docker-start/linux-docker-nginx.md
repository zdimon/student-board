# Nginx с Doker.

Установим прокси-сервер nginx apache c возможностью управлять переменными окружения.

Создадим стартовую страницу index.html

    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <title>Docker Nginx</title>
    </head>
    <body>
      <h2>Hello from Nginx container</h2>
    </body>
    </html>

Создадим файл Dockerfile

    FROM nginx:latest

Создадим сборщик docker-compose.yaml

    version: '3.5'
    services: 
        nginx:
            build: .
            restart: always
            ports:
                - 8081:80

**8000:8080** - мы перенаправляем порт 80 изнутри контейнера наружу на 8081


Сборка и запуск контейнера.

    docker-compose up --build

Запуск не через сборщик

    docker run -it --rm -d -p 8081:80 --name web nginx

Заходим внутрь контейнера.

    docker exec -ti b42580b257e2 bash

Выводим конфигурационный файл nginx.

    cat /etc/nginx/conf.d/default.conf

**b42580b257e2** - идентификатор контейнера, его можно получить командой docker ps

Однако можно и явно задать имя.

    version: '3.5'
    services: 
        nginx:
            build: .
            container_name: my-nginx

И обращаться по имени.

    docker exec -ti my-nginx bash

Создаем конфигурационный файл nginx.conf.

    server { 
     listen 80;
     server_name localhost;
     location / {
       root /app;
       try_files $uri /index.html;
     }
    }

Копируем конфигурационный файл внутрь контейнера и создаем папку app.

    FROM nginx:latest
    RUN mkdir /app
    COPY ./nginx.conf /etc/nginx/conf.d/default.conf

Сделаем ссылку из текущей директории внутрь контейнера.

    version: '3.5'
    services: 
        nginx:
            build: .
            restart: always
            ports:
                - 8081:80
            volumes:
                - .:/app 

Проброс переменных окружения внутрь контейнера.

    version: '3.5'
    services: 
        nginx:
            ...
            environment:
                - NGINX_PORT=8081

Но проблема в том что эти переменные появляются только на этапе запуска контейнера а не в момент сборки образа.

Поэтому чтобы изменять что то на этапе сборки можно в конфигурационном файле добавить метку.

    server { 
     listen __NGINX_PORT__;
     ...
    }

Потом ее менять при сборке.

    FROM nginx:latest
    RUN mkdir /app
    COPY ./default.conf /app/default.conf
    RUN cat /app/default.conf | sed  "s/__NGINX_PORT__/8081/" > /etc/nginx/conf.d/default.conf

TODO: можно попробовать флаг -i 

    sed -i 's/VERSION/8.04/' /etc/nginx/conf.d/default.conf

Или более грамотней, через переменную, которую вначале добавим в процесс сборки в docker-compose.yaml.

    nginx:
        build: 
            context: .
            args:
                - NGINX_PORT=8084

А потом используем.

    ARG NGINX_PORT  
    RUN cat /app/default.conf | sed  "s/__NGINX_PORT__/$NGINX_PORT/" > /etc/nginx/conf.d/default.conf




