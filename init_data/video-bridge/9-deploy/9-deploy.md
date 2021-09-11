# Деплой на удаленный хост.
 
Настройк nginx.

    map $http_upgrade $connection_upgrade {
        default upgrade;
        '' close;
    }


    upstream imaginsocket {
        server localhost:5001;
    }

    server { 
        listen 80;
        server_name localhost;

        location / {
            proxy_pass http://webrtc-django:8000;
        }

        location /socket.io {
            proxy_pass http://imaginsocket;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $connection_upgrade;
            proxy_set_header Host $host;
        }


    }

**location /socket.io** - тут мы настраиваем локейшин на веб-сокет соединение и проксируем его с 5001 порта.

При первой попытке соединения получаем ошибку, связанную с защитой браузера протоколом ssl.

    Cannot read property 'getUserMedia' of undefined

Установка certbot для получения ssl сертификата

    sudo apt install certbot
    sudo apt-get install python3-certbot-nginx

Запуск.

    sudo certbot --nginx



