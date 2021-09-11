# Flask с Doker.

Создадим стартовую страницу index.html и положим ее в папку templates.

    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <title>Docker Flask</title>
    </head>
    <body>
      <h2>Hello from Flask container</h2>
    </body>
    </html>

Создадим файл с зависимостями requirements.txt.

    Flask

Создадим файл Dockerfile

    FROM python:3.6
    RUN mkdir /app
    WORKDIR /app
    COPY ./requirements.txt /app/requirements.txt
    RUN apt update
    RUN pip install -r requirements.txt

Создадим сборщик docker-compose.yaml.

    version: '3.5'
    services: 
        flask:
            build: 
                context: .
                dockerfile: Dockerfile-flask
            volumes:
                - .:/app

Создадим скрипт для запуска start.py.

    from flask import Flask
    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    if __name__ == '__main__':
        app.run(debug=True,host='0.0.0.0')

Добавим проброс портов.


    ports:
        - 8082:5000

Добавим команду запуска.

    CMD python start.py

Добавим рендеринг шаблона.

    from flask import render_template

    @app.route('/')
    def hello_world():
        return render_template('index.html')

### Проксирование через nginx.

Cоздаем файл для образа Dockerfile-nginx

    FROM nginx:latest
    RUN mkdir /app
    COPY ./default.conf /etc/nginx/conf.d/default.conf

Файл конфигурации.

    server { 
         listen 80;
         server_name localhost;
         location / {
           proxy_pass http://flask:5000;
         }
    }

Добавляем контейнер в сборщик.

    nginx:
        build: 
            context: .
            dockerfile: Dockerfile-nginx
        volumes:
            - .:/app
        ports:
            - 8084:80

Проксируем статику.

    <img src="/static/test.png" />

Добавляем путь к статике в default.conf.

      
       ...

      location /static/ {
          alias /app/static/;
      }  
        
       ...
