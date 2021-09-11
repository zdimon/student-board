# Cервер непрерывной интеграции на python.
       
Непрерывная интеграция включает процесс применения изменений кода после их внесений через git на серверах.

Т.е. после того, как разработчик внес изменения и залил их в git, система в автоматическом режиме производит деплой кода на тестовый сервер, проводит все необходимые операции по сборке и тестированию, и затем переносит все на боевой.

Для автоматизации подобных процессов есть такие инстументы как Jenkins.

Он представляет собой отдельный сервер со множеством функций и даже своим языком для описания сценариев. Он способен обслуживать сразу множество проектов но довольно сложен в изучении.

Предлагаю для начала построить свой собственный сервер интеграции на основе Django и "заточить" его под один единственный проект.

Задача сервера будет заключаться в следующем:

Пользователю предлагается ввести email и надавить на кнопку "Создать рабочую область".

Система на сервере производит следущее: 

1. Создает на диске каталог с именем предоставленного emeil-a.

2. Клонирует в него репозиторий проекта на Django (в нашем случае).

3. Создает и пушит новый бранч в git по имени email-а.

4. Устанавливает все зависимости проекта.

5. Создает конфиги где:

- подключает проект к БД.

- создает конфиг для nginx в котором описывает новый поддомен, направленный на новый репозиторий

- подключает репозиторий к папке media (одна для всех т.к. она большая)

- предоставляет доступ папке проекта

Нам понадобится настроить доменную зону и указать в А записи, что мы хотим иметь произвольное количество поддоменов.

![start page]({path-to-subject}/images/2.png)

Cоздадим стартовый проект Django с именем ci.

    django-admin startproject ci

Файл зависимостей requirements.txt

    Django

Скрипт установки install

    python3 -m venv venv
    . ./venv/bin/activate
    pip3 install -r requirements.txt
    cd ci
    ./manage.py migrate

Создаем приложение

    ./manage.py startapp main

Включаем его в настройках.

Шаблон главной страницы.

    <html lang="en">
    <!-- Basic -->
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title> CI </title>
    </head>

    <body>
     
        <h1> Создать рабочую область </h1>
        <form method="POST" action="" >
            {% csrf_token %}
            Email 
            <input type="text" name="email" />
            <button>Создать</button>
        </form>
    </body>
    </html>

Нам понадобится где-то хранить переменные окружения.

Для этого создадим файл .env

Определяем папку, где будем создавать окружения и репозиторий, с которого будем клонировать проекты в окружения.

    WORK_DIR=/home/zdimon/tmp
    GIT_URL=git@github.com:zdimon/pressa-besa.git  

Установим пакет для чтения файлов подобного типа.

    pip install python-dotenv

И пропишем в settings.py

    from dotenv import load_dotenv
    load_dotenv()

    WORK_DIR = os.getenv('WORK_DIR')
    GIT_URL = os.getenv('GIT_URL')


Создадим модель и применим миграцию.

    from django.db import models

    class Env(models.Model):
        email = models.CharField(max_length=60,unique=True)
        port = models.IntegerField(default=8080,unique=True)

Админка.

    from django.contrib import admin

    from .models import Env

    @admin.register(Env)
    class EnvAdmin(admin.ModelAdmin):
        list_display = ['email','port']

Создадим класс формы в файле forms.py

    from django.forms import ModelForm
    from .models import Env


    class EnvForm(ModelForm):
        class Meta:
            model = Env
            fields = ['email']

Выводим в шаблоне.

    <form method="POST" action="" >
        {% csrf_token %}
        {{ form }}
        <button>Создать</button>
    </form>

Отработаем сабмит.

    from django.shortcuts import render
    from .forms import EnvForm

    def index(request):
        if request.method == 'POST':
            form = EnvForm(request.POST)
            if form.is_valid():
                form.save()
        else:
            form = EnvForm()
        return render(request,'index.html', {"form": form})


Результат

![start page]({path-to-subject}/images/3.png)

Реализуем в модели прибавление номера порта для каждой новой записи.

    from django.db import models
    from django.db.models.signals import post_save
    from django.db.models import Max

    class Env(models.Model):
        email = models.CharField(max_length=60,unique=True)
        port = models.IntegerField(default=8080)

        @classmethod
        def post_create(cls, sender, instance, created, *args, **kwargs):
            if created:
                maxp = Env.objects.aggregate(Max('port'))
                print(maxp)
                instance.port = maxp["port__max"]+1
                instance.save()

    post_save.connect(Env.post_create, sender=Env)

В файле tasks.py создадим функцию создания каталога.


    from django.conf import settings
    import os

    def create_dir(env):
        login = env.email.replace('@','---')
        path = os.path.join(settings.WORK_DIR,login)
        os.mkdir(path)

Вызовем ее при создании записи.

    def post_create(cls, sender, instance, created, *args, **kwargs):
        if created:
            ...
            create_dir(instance)

Установим библиотеку для гита

    pip install GitPython

Клонирование репозитория.

    import git

    def git_clone(env)
        path = os.path.join(settings.WORK_DIR,env.email.replace('@','---'))
        git.Git(path).clone(settings.GIT_URL)


Но тут мы сталкиваемся с проблемой времени выполнения т.к. процесс может быть долгим и пользователя негоже заставлять ждать долгой загрузки страницы.

Для этого придумали отложеные задачи (типа получи ЩАС html страничку с OK, а мы в работе, и ПОТОМ будет выхлоп).

Решаем их с помощью celery (основной игрок на поле python).

Установка.

    pip install redis
    pip install celery


Необходимо создать приложение celery в новом файле celery_app.py рядом с settings.py.

    from celery import Celery
    from django.conf import settings
    import os

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ci.settings')


    app = Celery()
    app.config_from_object('django.conf:settings', namespace='CELERY')
    app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


В settings.py установить Redis в качестве брокера сообщений.

    REDIS_HOST = os.getenv('SQL_HOST', 'redis-server')
    REDIS_PORT = os.getenv('SQL_PORT', '6379')

    CELERY_BROKER_URL = 'redis://' + REDIS_HOST + ':' + str(REDIS_PORT)

Добавить импорт в __init__.py

    from .celery_app import app as celery_app

Запуск вокера.

    celery -A ci worker -l info

ci - имя проекта

Задекорируем функции.

    from django.conf import settings
    import os
    import git
    from celery.decorators import task

    @task()
    def create_dir(env):
        login = env.email.replace('@','---')
        path = os.path.join(settings.WORK_DIR,login)
        os.mkdir(path)
        
    @task()
    def git_clone(env):
        path = os.path.join(settings.WORK_DIR,env.email.replace('@','---'))
        git.Git(path).clone(settings.GIT_URL)
        
        
Передадим на выполнение вокеру селери.

    create_dir.delay(instance)
    git_clone.delay(instance)
    
Передача объекта не работает, поетому передадим id.

    git_clone.delay(instance.id)

И выберем из базы объект.

    @task()
    def git_clone(env_id):
        from .models import Env
        env = Env.objects.get(pk=env_id)
        path = os.path.join(settings.WORK_DIR,env.email.replace('@','---'))
        git.Git(path).clone(settings.GIT_URL)
        
        
from .models import Env - импорт проводим внутри функции чтобы избежать циклического импорта.

## Конфиг nginx

Добавляем дополнительные переменные в .env

    NGINX_PATH=/etc/nginx/sites-enabled
    DOMAIN=local
    MEDIA_PATH=/home/zdimon/Desktop/work/pressa-besa/media/
    PROJECT_PATH=pressa-besa
    DB_PATH=/home/zdimon/Desktop/work/pressa-besa/backend/db.sqlite3
    
Прописываем в settings.

    DOMAIN = os.getenv('DOMAIN')
    NGINX_PATH = os.getenv('NGINX_PATH')
    MEDIA_PATH = os.getenv('MEDIA_PATH')
    PROJECT_PATH = os.getenv('PROJECT_PATH')
    DB_PATH = os.getenv('DB_PATH')

Прежде чем писать в системный каталог создадим в нем подкаталог и установим права на запись.

    sudo chown $UID:$GID /etc/nginx/sites-enabled

Так же, если вы хотите, чтобы рабочий каталог находился в домашней директории отдельного пользователя необходимо дать права на запись тому пользователю от имени которого стартует система.

Например, если сервер интеграции стартует от имени пользователя pressa, а работать должны от имени пользователя dev

    sudo setfacl -m u:pressa:rwx  /home/dev

Даем права dev для записи в директории, созданные от имени pressa, добавляя его в группу pressa

    sudo usermod -a -G pressa dev
    

Функция записи конфига nginx.

    def nginx_conf(env_id):
        from .models import Env
        env = Env.objects.get(pk=env_id)
        path = os.path.join(settings.BASE_DIR, 'tpl', 'nginx_vhost.conf')
        with open(path, 'r') as f:
            tpl = f.read()

        tpl = tpl.replace('%media_path%', settings.MEDIA_PATH)
        sname = '%s.%s' % (env.email.replace('@', '---'), settings.DOMAIN)
        tpl = tpl.replace('%server_name%', sname)
        tpl = tpl.replace('%port%', str(env.port))
        conf_path = os.path.join(
            settings.NGINX_PATH, env.email.replace('@', '---'))
        with open(conf_path, 'w+') as f:
            f.write(tpl)
        
## Конфиг supervisor

Устанавливаем супервизор

    sudo apt install supervisor
    
Смотрим путь по которому он инклудит конфы

    sudo nano /etc/supervisor/supervisord.conf

    [include]
    files = /etc/supervisor/conf.d/*.conf

Изменим путь.

    [include]
    files = /home/zdimon/Desktop/work/pressa-besa/ci/configs/supervisor/*.conf

Перегрузим

    sudo service supervisor restart
    
Получаем ошибку

![start page]({path-to-subject}/images/4.png)
        
Значит запускать будем через sudo

Посмотр задач

    supervisorctl
           
Пробуем тестовый сервер в файле test.conf.
           
    [program:test]
    user = zdimon
    directory = /home/zdimon/Desktop/work/pressa-besa/ci/ci
    command = python3 manage.py runserver 0.0.0.0:9898
    autostart = true
    autorestart = true   
    
![start page]({path-to-subject}/images/5.png)  

Пробуем добавить окружение и лог ошибок.

    environment=PYTHONPATH="/home/zdimon/Desktop/work/pressa-besa/ci/venv"
    stderr_logfile=/home/zdimon/Desktop/work/pressa-besa/ci/logs/error.log

Можем наблюдать в логе 

    ModuleNotFoundError: No module named 'celery'

![start page]({path-to-subject}/images/6.png)  

Похоже на то, что окружение не подключается.

Пробую применить бинарник интерпретатора изнутнри окружения

    command = /home/zdimon/Desktop/work/pressa-besa/ci/venv/bin/python3 manage.py runserver 0.0.0.0:9898


Теперь все работает.

![start page]({path-to-subject}/images/7.png)

Создаем шаблон под конфиг

    [program:%name%]
    directory = %prj_dir%
    command = %env_dir%/bin/python3 manage.py runserver 0.0.0.0:%port%
    autostart = true
    autorestart = true
    environment=PYTHONPATH="%env_dir%"
    stderr_logfile=/home/zdimon/Desktop/work/pressa-besa/ci/logs/%name%.log

Оформляем функцию под конфиг. 

    def supervisor_conf(env_id):
        from .models import Env
        env = Env.objects.get(pk=env_id)
        path = os.path.join(settings.BASE_DIR, 'tpl', 'supervisor.conf')
        with open(path, 'r') as f:
            tpl = f.read()
        sname = '%s.%s' % (env.email.replace('@', '---'), settings.DOMAIN)
        tpl = tpl.replace('%name%', sname)
        tpl = tpl.replace('%port%', str(env.port))
        prj_dir = os.path.join(settings.WORK_DIR, env.email.replace(
            '@', '---'), settings.PROJECT_PATH)
        tpl = tpl.replace('%prj_dir%', prj_dir)
        tpl = tpl.replace('%env_dir%', settings.ENV_PATH)
        filename = '%s.conf' % env.email.replace('@', '---')
        conf_path = os.path.join(
            settings.BASE_DIR, 'configs', 'supervisor', filename)
        with open(conf_path, 'w+') as f:
            f.write(tpl)


Осталось сделать рестарт supervisor-а и nginx-а.

    bashCommand = "sudo service supervisor restart"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print(error)

Получили запрос пароля в окне с селери.

![start page]({path-to-subject}/images/8.png)

Значит будем запускать из под рута.

    sudo celery -A ci worker -l info

Тогда отвалился git т.к. в git не добавлены ключи суперпользователя.

    Please make sure you have the correct access rights
    and the repository exists.'

Пробуем подавить запрос пароля для sudo

    sudo visudo

Вставляем строку.

    zdimon ALL=(ALL) NOPASSWD: ALL
    
## Удаление рабочей  области.

Создадим задачу для celery, которая будет удалять всю область при удалении пользователя из модели Env.

    @task()
    def clear_env(email):
        import subprocess
        # remove env path
        env_path = os.path.join(settings.WORK_DIR, email)
        bashCommand = "sudo rm -r %s" % env_path
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        print(error)

        # remove nginx conf
        nginx_path = os.path.join(
            settings.NGINX_PATH, email)
        os.remove(nginx_path)

        # remove supervisor conf
        filename = '%s.conf' % email
        supervisor_conf_path = os.path.join(
            settings.BASE_DIR, 'configs', 'supervisor', filename)
        os.remove(supervisor_conf_path)

В эту задачу мы будем передавать email т.к. на момент ее вызова записи в базе может уже не быть и мы не сможет ее выбрать по id.

Вызываем задачу.

    from django.db.models.signals import pre_delete

    def pre_delete_handler(sender, instance, using, **kwargs):
        clear_env.delay(normalize_email(instance.email))


    pre_delete.connect(pre_delete_handler, sender=Env)






