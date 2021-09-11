# Настраиваем веб-сокет сервер и Celery.

Создадим новое приложение.

    ./manage.py startapp webrtc

Подключим его в app/settings.py

    INSTALLED_APPS = [
        ...
        'webrtc'
    ]

## Сокет сервер.

Создадим новую команду для запуска сокет сервера.


    from django.core.management.base import BaseCommand
    import socketio
    import eventlet

    eventlet.monkey_patch()
    mgr = socketio.RedisManager('redis://localhost:6379/0')
    sio = socketio.Server(cors_allowed_origins='*',async_mode='eventlet',client_manager=mgr)
    app = socketio.WSGIApp(sio)


    @sio.event
    def connect(sid, environ):
        print('connect ', sid)


    @sio.event
    def disconnect(sid):
        print('disconnect ', sid)


    class Command(BaseCommand):

        def handle(self, *args, **options):
            print('Statrting socket server')
            eventlet.wsgi.server(eventlet.listen(('', 5001)), app)



Добавим зависимости

    Django
    python-socketio
    eventlet
    redis

При этом нужно иметь запущенным REDIS сервер локально.

Запуск сервера.


   ./manage.py start_socket

## Система отложенных задач Celery

Добавляем зависимость.

    Django
    python-socketio
    eventlet
    redis
    celery

Далее нам необходимо создать приложение celery в новом файле celery_app.py рядом с settings.py.

    from celery import Celery
    from django.conf import settings
    import os

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prj.settings')


    app = Celery()
    app.config_from_object('django.conf:settings', namespace='CELERY')
    app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

В settings.py установить Redis в качестве брокера сообщений.

    REDIS_HOST = os.getenv('SQL_HOST', 'redis-server')
    REDIS_PORT = os.getenv('SQL_PORT', '6379')

    CELERY_BROKER_URL = 'redis://' + REDIS_HOST + ':' + str(REDIS_PORT)

Запуск вокера.

    celery -A app worker -l info

Добавить импорт в __init__.py

    from .celery_app import app as celery_app

Добавим 3 контейнера в docker-compose.yaml

- для celery

- для Redis

- для веб-сокет сервера

### Redis контейнер

    version: '3.5'
    services: 
       ...
        redis-server:
            image: "redis:alpine"
            container_name: webrtc-redis-server
            networks: 
                - webrtc_network


![start page]({path-to-subject}/images/2.png)

### Celery контейнер

    webrtc-celery-worker:
        build: .
        working_dir: /app
        command: celery -A app worker -l info
        volumes:
            - ./app:/app
        depends_on:
            - webrtc-redis-server
        container_name: webrtc-celery-worker
        networks: 
            - webrtc_network

![start page]({path-to-subject}/images/3.png)

Теперь осталось поменять хост для подключения к REDIS

    REDIS_HOST = os.getenv('SQL_HOST', 'webrtc-redis-server')

## Вебсокет контейнер.

    webrtc-socketio-server:
        build: .
        working_dir: /app
        command: ./manage.py start_socket
        volumes:
            - ./app:/app
        depends_on:
            - webrtc-redis-server
        container_name: webrtc-socketio-server
        ports:
            - 5001:5001
        networks: 
            - webrtc_network

Забор параметров окружения из файла .env в settings.py.

    from dotenv import load_dotenv
    load_dotenv()





