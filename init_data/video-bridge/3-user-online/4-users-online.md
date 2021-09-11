# Отслеживаем пользователей в онлайне.
      
Для отслеживания создадим простейшую страницу, где будем устанавливать сокет-соединение под заданным пользователем.

Создадим вьюху.

    from django.shortcuts import render


    def index(request):
        return render(request, 'index.html')

Роутинг.

    from django.contrib import admin
    from django.urls import path

    from webrtc.views import index

    urlpatterns = [
        path('', index),
        path('admin/', admin.site.urls),
    ]


Шаблон в папке templates/index.html

    <!DOCTYPE html>
    <html>
    <head>
        <script src="/static/node_modules/jquery/dist/jquery.min.js"></script>
        <script src="/static/node_modules/socket.io/client-dist/socket.io.min.js"></script>
    </head>

    <body>
        <h1>Test page</h1>
        <input type="text" id="username" />
        <button id="sendButton">Connect</button>
    <script>


    </script>
    </body>

    </html>

Пропишем в настройках путь к шаблонам.

    TEMPLATES = [
        {
            ...
            'DIRS': [os.path.join(BASE_DIR,'templates')],
            ...
    ]


Установим клиентские библиотеки в папке static

    mkdir static
    cd static
    npm init
    npm install jquery socket.io --save

Пропишем в настройки папку со статикой.

    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static')
    ]


Теперь будем пытаться соединится с сервером по веб-сокетам используя клиент socket.io.

    <script>

        $('#connectButton').on('click', () => {
            const socket = io('http://localhost:5001', {transports:['websocket']}); 
            socket.on('connect', () => {
                console.log('Connection was established');
                window.sessionStorage.setItem('sid',socket.id);
            });
        })

    </script>

Так же мы сохраняем идентификатор соеденения в сессии браузера для последующего использования и передачи серверу в разных запросах.

Результат.

Клиент.

![start page]({path-to-subject}/images/4.png)

Сервер.

![start page]({path-to-subject}/images/5.png)


## Использование Typescript.

    import  io  from "socket.io-client";

    $('#my').html('Hello from jQuery');
    $('#connectButton').on('click', () => {
        const socket = io('http://localhost:5001', {transports:['websocket']});

        socket.on('connect', () => {
            console.log('Connection was established');
            window.sessionStorage.setItem('sid',socket.id);
        })
    });


Теперь создадим модели под пользователей онлайн и под их сокет-соединения.

    from django.db import models
    from django.utils.translation import gettext as _


    class UserProfile(models.Model):
        login = models.CharField(max_length=50,unique=True, verbose_name=_('Name'))
        is_online = models.BooleanField(default=False)


    class UserConnection(models.Model):
        sid = models.CharField(max_length=250,unique=True, verbose_name=_('SID'))
        user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


Админку под них.

    from django.contrib import admin
    from .models import UserProfile, UserConnection

    @admin.register(UserProfile)
    class UserProfileAdmin(admin.ModelAdmin):
        list_display = ['login', 'is_online']

    @admin.register(UserConnection)
    class UserConnectionAdmin(admin.ModelAdmin):
        list_display = ['user', 'sid']

Теперь из клиента пошлем сообщение на сервер после коннекта с просьбой создать запись в этих таблицах по факту установки соединения.

    $('#connectButton').on('click', () => {
        const socket = io('http://localhost:5001', {transports:['websocket']}); 
        socket.on('connect', () => {
            console.log('Connection was established');
            socket.emit('login',{login: $('#username').val()});
        });
    })

Отработаем приход сообщения на сервере.

Это необходимо сделать в отдельном потоке т.к. сокет-сервер работает в асинхронном режиме.

    ...
    import threading
    from webrtc.models import UserProfile, UserConnection
    ...

    def add_user_task(sid,data):
        print('Adding user connection')
      

    @sio.event
    def login(sid, data):
        thread = threading.Thread(target=add_user_task, args=(sid,data))
        thread.start()

Нам осталось создать пользователя с данным логином если его нет и запись с сокет соединением.

    def add_user_task(sid,data):
        try:
            user = UserProfile.objects.get(login=data['login'])
        except:
            print('No user')
            user = UserProfile()
            user.login = data['login']
            user.save()
        con = UserConnection()
        con.user = user
        con.sid = sid
        con.save()

И удалить соединение и пользователя при дисконнекте.

    def remove_connection_task(sid):
        try:
            con = UserConnection.objects.get(sid=sid)
            user = con.user
            con.delete()
        except ObjectDoesNotExist:
            pass

        if UserConnection.objects.filter(user=user).count() == 0:
            user.delete()

Полная версия команды start_socket.py.

    from django.core.management.base import BaseCommand
    import socketio
    import eventlet
    import threading
    from webrtc.models import UserProfile, UserConnection
    from django.core.exceptions import ObjectDoesNotExist

    eventlet.monkey_patch()
    mgr = socketio.RedisManager('redis://localhost:6379/0')
    sio = socketio.Server(cors_allowed_origins='*',
                          async_mode='eventlet',
                          client_manager=mgr)
    app = socketio.WSGIApp(sio)


    def add_connection_task(sid, data):
        try:
            user = UserProfile.objects.get(login=data['login'])
        except ObjectDoesNotExist:
            print('No user')
            user = UserProfile()
            user.login = data['login']
            user.save()
        con = UserConnection()
        con.user = user
        con.sid = sid
        con.save()


    def remove_connection_task(sid):
        try:
            con = UserConnection.objects.get(sid=sid)
            user = con.user
            con.delete()
        except ObjectDoesNotExist:
            pass

        if UserConnection.objects.filter(user=user).count() == 0:
            user.delete()


    @sio.event
    def connect(sid, environ):
        print('connect ', sid)


    @sio.event
    def login(sid, data):
        thread = threading.Thread(target=add_connection_task, args=(sid, data))
        thread.start()


    @sio.event
    def disconnect(sid):
        print('disconnect ', sid)
        thread = threading.Thread(target=remove_connection_task, args=(sid,))
        thread.start()


    class Command(BaseCommand):

        def handle(self, *args, **options):
            print('Statrting socket server')
            eventlet.wsgi.server(eventlet.listen(('', 5001)), app)


Создадим команду для создания аккаунта суперпользователя для входа в админку.

    from django.core.management.base import BaseCommand
    from django.contrib.auth.models import User

    class Command(BaseCommand):

        def handle(self, *args, **options):
            print('creating superuser')
            u = User()
            u.username = 'admin'
            u.set_password('admin')
            u.is_active = True
            u.is_staff = True
            u.email = 'admin@gmail.com'
            u.is_superuser = True
            u.save()









