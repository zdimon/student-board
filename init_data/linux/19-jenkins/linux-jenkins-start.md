# Jenkins. Начало работы.
       
Установка Doсker контейнера.

Создадим docker-compose.yaml.


    version: '3.7'
    services:
      jenkins:
        image: jenkins/jenkins:lts
        privileged: true
        user: root
        ports:
          - 8081:8080
          - 50000:50000
        container_name: jenkins
        volumes:
          - .data:/var/jenkins_home

Устанавливаем.

    docker-compose up --build

![start page]({path-to-subject}/images/2.png)

Заходим на станицу http://localhost:8081/

![start page]({path-to-subject}/images/3.png)

Копируем и вставляем пароль из файла .data/secrets/initialAdminPassword

Далее попадаем на страницу установки плагинов.

![start page]({path-to-subject}/images/4.png)

Вся работа в Jenkins сводится к созданию так называемых Конвееров (Pipeline).

Они представляют собой последовательность действий для деплоя и тестиррования вашего приложения.

Эта последовательность содержиться в файле Jenkinsfile и написана на языке Groovy.

Groovy — объектно-ориентированный язык программирования разработанный для платформы Java как альтернатива языку Java с возможностями Python, Ruby и Smalltalk.

Возможности Groovy (отличающие его от Java):

— Статическая и динамическая типизация

— Встроенный синтаксис для списков, ассоциативных массивов, массивов и регулярных выражений

— Замыкания

— Перегрузка операций

Более того, почти всегда java-код — это валидный groovy-код.

## Установка groovy.

Прежде всего необходимо поставить java.

Затем запускаем следующие команды.

    curl -s get.sdkman.io | bash

    source "$HOME/.sdkman/bin/sdkman-init.sh"

## Создание образа для jenkins с Docker.

Создаем файл Dockerfile c установкой всего необходимого для Docker в контейнер.

    FROM jenkins/jenkins:lts

    ARG DOCKER_COMPOSE_VERSION=1.25.0

    USER root
    RUN apt-get update && \
       apt-get upgrade -y && \
       apt-get -y install apt-transport-https \
          ca-certificates \
          curl \
          gnupg2 \
          git \
          software-properties-common && \
       curl -fsSL https://download.docker.com/linux/$(. /etc/os-release; echo "$ID")/gpg > /tmp/dkey; apt-key add /tmp/dkey && \
       add-apt-repository \
          "deb [arch=amd64] https://download.docker.com/linux/$(. /etc/os-release; echo "$ID") \
          $(lsb_release -cs) \
          stable" && \
       apt-get update && \
       apt-get -y install docker-ce && \
       apt-get clean autoclean && apt-get autoremove && rm -rf /var/lib/{apt,dpkg,cache,log}/

    RUN curl -L https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose 

    RUN usermod -aG docker jenkins && gpasswd -a jenkins docker
    USER jenkins

Собираем образ.

    docker build .

Изменяем файл docker-compose.yaml

    image: jenkins/jenkins:lts

Заменим на 

    build: .

Так же добавим два volumes в которым перенаправим бинарники докера изнутри контейнера на локальную машину.

    volumes:
      - ./data:/var/jenkins_home
      - /var/run/docker.sock:/var/run/docker.sock
      - /usr/local/bin/docker:/usr/local/bin/docker

Перезапускаем контейнер.

    docker-compose up --build

Получаем проблему в правах.

![start page]({path-to-subject}/images/5.png)

Дело в том что пользователь внутри контейнера имеет отличные от локальных UID и GID и следовательно не может писать в папку data.

Существует вариант все команды пропускать через скрипт entry-point.sh

    #!/bin/sh
    set -e

    # first arg is `-f` or `--some-option`
    # or first arg is `something.conf`
    if [ "${1#-}" != "$1" ] || [ "${1%.conf}" != "$1" ]; then
	    set -- redis-server "$@"
    fi

    # allow the container to be started with `--user`
    if [ "$1" = 'redis-server' -a "$(id -u)" = '0' ]; then
	    find . \! -user redis -exec chown redis '{}' +
	    exec gosu redis "$0" "$@"
    fi

    exec "$@"

В котором перебивать права на нужного пользователя.

    COPY docker-entrypoint.sh /usr/local/bin/
    ENTRYPOINT ["docker-entrypoint.sh"]


[источник](https://github.com/docker-library/redis)

[обсуждение в StackOverflow](https://stackoverflow.com/questions/24288616/permission-denied-on-accessing-host-directory-in-docker)

## Ручная установка.

Для работы необходима Java машина

    java -version

Добавляем ключ репозитория в систему.

    wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -

Затем добавьте в адрес репозитория пакетов Debian в sources.list сервера:

    sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
 
Обновляем список репозиториев.

    sudo apt update

Установка

    sudo apt install jenkins

Старт сервера.

    sudo systemctl start jenkins

Проверка сервера.

    sudo systemctl status jenkins

![start page]({path-to-subject}/images/6.png)


Настраиваем виртуальный хост nginx.

    server {
            listen 80;
            server_name jenkins.wezom.webmonstr.com;
            location / { 
                    proxy_pass http://localhost:8080;
            }
    }

## Задача.

Предположим что у нас есть удаленная машина со средой разработки какого-нибудь проекта и командами для тестирования.

Мы хотим переодически запускать тесты на удаленной машине. 

Для того, чтобы jenkins мог успешно установить своего агента на удаленном хосте должна стоять java.

Поставим вариант headless без всяких лишних графических "прибамбасов".

    sudo apt install openjdk-8-jre-headless


## Добавление нового пользователя с правами захода на удаленный хост по ssh.


![start page]({path-to-subject}/images/7.png)

![start page]({path-to-subject}/images/8.png)

![start page]({path-to-subject}/images/9.png)

![start page]({path-to-subject}/images/10.png)

![start page]({path-to-subject}/images/11.png)

Мы выбираем способ доступа по ssh ключу.

Поэтому в jenkins копируем приватный ключ из файла ~/.ssh/id_rsa

А на удаленной машине добавляем публичный ключ в файл .ssh/authorized_keys, который берем из ~/.ssh/id_rsa.pub

После добавления пользователя можно приступить к созданию новой среды сборки (сборщика) и привязать ее к удаленному хосту, на котором мы собираемся запускать тесты.

![start page]({path-to-subject}/images/12.png)

![start page]({path-to-subject}/images/13.png)


![start page]({path-to-subject}/images/14.png)


При создании среды (Ноды) необходимо указать рабочий каталог, IP адрес и порт во вкладке Дополнительно если он отличается от стандартного 22-го. 

Также необходимо выбрать пользователя, под которым будет выполнен вход на удаленную машину.

И указать метку для удобной привязке к нему задач.

Также можно указать количество вокеров в пуле сборщика на тот случай, если на удаленной машине есть доп. ресурсы в виде простаивающих ядер процессора.

![start page]({path-to-subject}/images/15.png)

Наконец можно приступить к созданию новой задачи.

![start page]({path-to-subject}/images/16.png)

Первым делом привязываем задачу к сборщику по его метке.

![start page]({path-to-subject}/images/17.png)

Далее выбираем тип действия сборщика. 

В простейшем случае выполнение команды BASH.

![start page]({path-to-subject}/images/19.png)

![start page]({path-to-subject}/images/18.png)

![start page]({path-to-subject}/images/20.png)

В команде мы вначале прыгаем внутрь домашней директории для того, чтобы выйти за пределы рабочего каталога jenkins, который он создает для того, чтобы не "засерать" рабочую область проекта.


Запускаем сборку.

![start page]({path-to-subject}/images/21.png)

Проверяем результат.

![start page]({path-to-subject}/images/22.png)

![start page]({path-to-subject}/images/23.png)
