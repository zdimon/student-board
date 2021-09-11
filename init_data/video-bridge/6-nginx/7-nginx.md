# Прокси-сервер nginx.

Создадим образ для веб-сервера Dockerfile.nginx.

    FROM nginx:latest
    RUN mkdir /app
    COPY ./conf/nginx.default.conf /etc/nginx/conf.d/default.conf

Конфигурация виртуального хоста /conf/nginx.default.conf.

    server { 
        listen 80;
        server_name localhost;

        location / {
            root /app;
            try_files $uri /index.html;
        }
    }

Создаем контейнер.

    pressa-nginx-server:
        build: 
            context: .
            dockerfile: Dockerfile.nginx
            args:
                - NGINX_PORT=80
        container_name: pressa-nginx-server
        # restart: always
        ports:
            - 80:80
        volumes:
            - .:/app
        depends_on:
            - pressa-django
        networks: 
            - webrtc_network

Теперь нам необходимо пробросить порт, на которм джанга в нжинкс, в его настройках.

    server { 
        listen 80;
        server_name localhost;

        location / {
            proxy_pass http://pressa-django:8000;
        }
    }

proxy_pass http://pressa-django:8000 - тут мы говорим что все что приходит на базовый урл получает то, что отдает 8000 порт контейнера pressa-django.


Прицепим на кнопку подключение по вебсокету.


   <script>
    $('#journals').on('click', (e) => {
        const socket = io('http://localhost:5001', {transports:['websocket']}); 
    })
   </script>





