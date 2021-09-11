# Настройка виртуальных хостов nginx.
     

Итак, виртуальный хост — это разделение адресного пространства web-сервера, например, по имени сайта, позволяющее запускать несколько web-сайтов/приложений на одном физическом сервере.

Если говорить в терминологии документации nginx, виртуальный хост также называется «Server Block».

## Установка.

    sudo apt-get install -y nginx

## Запуск, останов, проверка конфигурации

    service nginx start|stop
    nginx -t

## Посмотреть под кем работают вокеры nginx

    ps -eo "%U %G %a" | grep nginx


## Создание веб-директории и назначение ей прав.

    sudo mkdir -p /home/webmaster/www/django

    sudo chown -R www-data:www-data /home/webmaster/www/mysite

Вы можете заменить пользователя «www-data», используемого ниже, на другого, но по умолчанию nginx работает от имени именно этого пользователя.

Теперь сделаем так, чтобы все пользователи могли читать наши новые файлы:

    sudo chmod 755 /home/webmaster/www

### Создаем стартовую страницу /home/webmaster/www/mysite/index.html.

    <html>
      <head>
        <title>mysite.ru</title>
      </head>
      <body>
        <h1>Virtual Host в nginx!</h1>
      </body>
    </html>

##Создание конфигурации виртуального хоста

В nginx в директории /etc/nginx/sites-available есть шаблон для создаваемых конфигураций. 


    sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/mysite.ru

## Минимальная конфигурация.

    server {
        listen   80;
        root /home/webmaster/www/mysite;
        index index.html index.htm;
        server_name mysite.ru www.mysite.ru;
    }

В качестве server_name вы также можете задать IP-адрес или несколько имён через пробел, по которым будет доступен хост, как мы и сделали.

Вариант использования listen

    listen *:80;

root директива говорит nginx взять url и добавить его к root пути.

В nginx есть папки sites-available и sites-enabled. В первой хранятся конфигурации ВСЕХ виртуальных хостов, которые могут быть на данном сервере, а в директории sites-enabled символические ссылки на активные. 

 Никто не запрещает в sites-enabled размещать оригинал файла конфигурации, а не ссылку, но это будет менее удобно, т.к. в случае необходимости отключения придётся либо удалять файл (тогда будет проблематично включить обратно), либо перемещать его в другую директорию (тогда мы должны помнить, куда мы перенесли). Гораздо проще грохнуть символическую ссылку!

## Создание символической ссылки.

    sudo ln -s /etc/nginx/sites-available/mysite.ru /etc/nginx/sites-enabled/mysite.ru

Проверка правильности конфигурации.

    sudo nginx -t

Перезапуск сервера.

    sudo service nginx restart

## Настройки локальных хостов.

Если вы хотите работать с вашим виртуальным хостом без реального доменного имени, вы можете настроить локальные хосты на вашей машине и обращатся к ним по имени а не по localhost.

    sudo nano /etc/hosts

Пример конфигурации.

    127.0.0.1 starter.php
    127.0.0.1 market.local

В блоке server могут быть дополнительные блочные директивы. Например location.

Все директивы, которые используются в блоке server, могут использоваться и в блоках location. Но нам не обязательно указывать root и index в каждом location. Если их опустить, то будут наследоваться те, которые были указаны в родительском блоке.

Пример блока location

    server {
        listen *:80;
        server_name example.ru;
        root /usr/share/nginx/html;
        index index.html index.htm;
        location / {}
    }

localion можно направить в другую директорию.

    location / {
        root   /var/www;
        index  index.html index.htm;
    }

Если у нас есть каталог /home/zdimon/www/nginx/web2 и мы хотим натравить в него все запросы по адресу 

http://v1.nginx.loc/web2/

Пишем такой локейшин

    location /web2 {
	    root /home/zdimon/www/nginx;
    }

Такой пример работать не будет

    location /web2 {
	    root /home/zdimon/www/nginx/web2;
    }

т.к. root будет искать в таком каталоге /home/zdimon/www/nginx/web2/web2

Для того чтобы этого избежать можно применить директиву alias.

alias - говорит nginx что заменить в пути location-а на то, что указано в alias.

## Обработка 404 и директива try_files.

    try_files $uri $uri/ =404;

## Проксирование через порт.

Пример проксирования с порта, на котором висит другой веб сервер.

    location / {
	    proxy_pass http://localhost:8080;
    }

При отсутствии процесса на указанном порту получим.

![nginx]({path-to-subject}/images/2.png)

Запуск простого сервера на python.

    python3 -m http.server 8080


Пример проксирования всеx файлов php

	    location ~ \.php$ {
	        fastcgi_pass    127.0.0.1:8002;
	        include snippets/fastcgi-php.conf;
	    }

Пример проксирования статичных файлов.

    location ^~ /images {
        alias /var/www/static;
        try_files $uri $uri/ =404;
    }
     
    location ^~ /css {
        alias /var/www/static;
        try_files $uri $uri/ =404;
    }


## Настройка логов.

	access_log /var/log/nginx/access.log;
	error_log /var/log/nginx/error.log;

## Запуск python uwsgi процесса.

    apt-get install uwsgi uwsgi-plugin-python3

Создание настроечного файла.

## Запуск процессов из под supervisor.

Установка uwsgi и supervisor.

    apt-get install build-essential python3-dev

    apt-get install uwsgi supervisor

    sudo apt-get install uwsgi-plugin-python3

Настроечный файл /etc/uwsgi/apps-enabled/mysite.ini.

    [uwsgi]
    socket = /tmp/pl.sock
    buffer-size=32768
    chmod-socket = 666
    processes = 1
    threads = 2
    virtualenv = /home/zdimon/Desktop/projects/pl/venv/
    chdir = /home/zdimon/Desktop/projects/pl/pl
    module = pl.wsgi:application
    plugins = python3

## Проксирование с unix сокета.

    location / {
        proxy_pass  http://unix:/tmp/pl.sock;
    }

