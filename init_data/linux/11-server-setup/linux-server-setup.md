# Первичная настройка сервера. Работа с сервером по протоколу ssh.

## Генерация ключей.

    ssh-keygen

## Вывод ключа в терминале

    cat ~/.ssh/id_rsa.pub

![start page]({path-to-subject}/images/2.png)


## Команда копирования публичного ключа.

    ssh-copy-id root@servaername.com

## Соддание алиаса для быстрой команды подключения.

В файле .bash_aliases домашней директории прописываем.

    alias putin='ssh root@tity.webmonstr.com'

## Команда соединения с сервером

    ssh username@host
    ssh root@mydomain.com
    ssh root@234.12.5.67

## Обновление репозитория.

    sudo apt update

Далее установим 

    sudo apt install software-properties-common

Эта библиотека предоставляет инструменты для управления репозиторием apt (добавление и удалением источников приложений) через команды, иначе пришлось бы редактировть файл /etc/apt/sources.list.d руками.

## Проблема с локалью.

![start page]({path-to-subject}/images/3.png)

Проверяем локаль.

    locale -a

Locale – это локализация Linux которая определяет в какой кодировке пользователь видит всё в терминале.

Установим редактор nano

    apt install nano

Откроем для редактирования файлик /etc/locale.gen

    nano /etc/locale.gen

Поищем через ctrl+W en_US

Раскомментируем строку

    en_US.UTF-8 UTF-8
    uk_UA.UTF-8 UTF-8

И сохраним через ctr+O и Enter и ctrl+x - выходим.

Осталось сгенерировать локаль

    sudo locale-gen

![start page]({path-to-subject}/images/4.png)

Проверим теперь.

![start page]({path-to-subject}/images/5.png)
   

## Добавление пользователя.

   sudo adduser webmaster

## Переход на произвольного пользователя

    su webmaster

## Включение пользователя в группу sudo

Провверить какие пользователи имеют право запускать команды через sudo можно командой.

    sudo whoami

В файле /etc/sudoers содержаться пользователи и группы, которые это могут.

Включить пользователя в sudoers.

    sudo adduser <username> sudo

    sudo usermod -a -G sudo <username>

Сделать безпарольный запуск.

    username  ALL=(ALL) NOPASSWD:ALL

    %sudo	ALL=(ALL:ALL) NOPASSWD: ALL

## Установка Python.

    sudo apt install python2 python3 -y

y - автоматическое согласие на вопросы при установке

Когда мы имеем дело с несколькими версиями одной комманды, например

    python
    python2
    python3

Посмотреть где находятся бинарники.

     which python2
     which python3

Удобно пользоваться инструментом  update-alternatives для управления переключением использования версии по умолчанию.

## Установим питон по старше из репозитория "мертвых змей".

    sudo add-apt-repository ppa:deadsnakes/ppa

Официальные репозитории Ubuntu хоть и содержат огромное количество пакетов, труднодоступных для обычных разработчиков, в них сложно поддерживать актуальные версии своей программы, да и вообще, не каждый проект имеет шанс туда попасть. Для создания собственного репозитория необходимы ресурсы, как минимум, сервер, и неплохие навыки администратора. Всё это создаёт некоторые препятствия для распространения программ для Ubuntu.

(Personal Package Arhive - PPA) - сервис для обычного пользователя который дает возможность любому создать свой репозиторий. 

Обновляем, ставим.

    apt update
    apt install python3.7

Добавляем альтернативы.

    sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.5 1
    sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.7 2

Выбираем

    sudo update-alternatives --config python

![start page]({path-to-subject}/images/7.png)

## Создание виртуального окружения.

Установка

    apt install python3.7-venv python3.7-dev

Создание 

    python3 -m venv venv

Активация 

    . ./venv/bin/activate

Установка библиотек.

    pip install django
    pip install pytelegrambotapi

## Создание и запуск проекта Django в скрине

Устанавливаем скрины

    apt install screen

Создаем скрин

    screen -S dj

Создаем проект и запускаем сервер

    django-admin startproject prj
    cd prj
    ./manage.py migrate
    ./manage.py createsuperuser
    ./manage.py runserver 0.0.0.0:8080

Отключаемся от скрина по ctrl+A потом D

Вывод запущенных скринов.

    screel -ls

Подключение к скрину

    screen -r <id или name>

К чужому скрину в многопользовательском режиме

    screen -x <id или name>

Установка дополнительного ПО

    apt install htop mc git wget nginx

## Запуск команд удаленно

    ssh root@tiny.webmonstr.com 'ls'





    


