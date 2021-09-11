# Dart. Начало работы.

[ссылка на источник](https://www.thepolyglotdeveloper.com/2019/04/building-simple-web-application-dart/)
     
## Установим SDK


Вначале поставим публичный ключ и ссылку на репозиторий.

     sudo apt-get update
     sudo apt-get install apt-transport-https
     sudo sh -c 'wget -qO- https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -'
     sudo sh -c 'wget -qO- https://storage.googleapis.com/download.dartlang.org/linux/debian/dart_stable.list > /etc/apt/sources.list.d/dart_stable.list'

Установка 

     sudo apt-get update
     sudo apt-get install dart

Прописываем путь к бинарникам

    echo 'export PATH="$PATH:/usr/lib/dart/bin"' >> ~/.bashrc

Инструменты коммандной строки

dart - виртуальная машина

dartdoc - документирование API

dart2js - компилятор в js

dartfmt - форматирование кода

dartanalyzer - анализатор кода

pub - пакетный менеджер

dartdevc - быстрый компилятор для разработки


[ссылка да документацию по CLI](https://dart.dev/tools#cli)

Инсталируем инструменты разработки при помощи пакетного менеджера

    pub global activate webdev

![uml]({path-to-subject}/images/2.png)

Теперь нам доступна команда webdev.

webdev - исструмент для сборки запуска и тестов приложения.

[ссылка на документацию](https://dart.dev/tools/webdev)

Добавим переменную пути для кеша в окружение.

    export PATH="$PATH":"$HOME/.pub-cache/bin"

Теперь установим инструмент stagehand

    pub global activate stagehand

[ссылка на документацию](https://pub.dev/packages/stagehand)


Теперь можем генерировать такие приложения.

console-simple - Приложение командной строки.

console-full - Примеры для приложения командной строки.

package-simple - Для библиотек и пакетов.

server-shelf - Веб-сервер на пакете shelf.

web-angular - Веб приложение на Material Design.

web-simple - Приложение на основе чистого Dart.

web-stagexl - Игровое приложение и анимация.

Генерируем новое приложение в текущем каталоге.

    stagehand web-simple

![uml]({path-to-subject}/images/3.png)

В pubspec.yaml находим зависимости.

    name: code
    description: An absolute bare-bones web app.
    # version: 1.0.0
    #homepage: https://www.example.com

    environment:
      sdk: '>=2.10.0 <3.0.0'

    #dependencies:
    #  path: ^1.7.0

    dev_dependencies:
      build_runner: ^1.10.0
      build_web_compilers: ^2.11.0
      pedantic: ^1.9.0

Устанавливаем их.

    pub get

Запускаем сервер.

    webdev serve

На порту

    webdev serve web:8087

Билдим проект

    webdev build

## Установка Android Studio.

Скачиваем архив.

![uml]({path-to-subject}/images/4.png)

Устанавливаем некоторые библиотеки под 32-х разрядную платформу.

    sudo apt-get install libc6:i386 libncurses5:i386 libstdc++6:i386 lib32z1 libbz2-1.0:i386

Распаковываем и запускаем

    ./bin/studio.sh

![uml]({path-to-subject}/images/5.png)

![uml]({path-to-subject}/images/6.png)

![uml]({path-to-subject}/images/7.png)

![uml]({path-to-subject}/images/8.png)

На этом шаге пришлось изменить каталог под SDK.

![uml]({path-to-subject}/images/9.png)

![uml]({path-to-subject}/images/10.png)

Распаковываем и прописываем переменную окружения в ту папку, в которую распаковали.

    ANDROID_HOME = /home/zdimon/android-sdk/



## Установка Flutter.

Клонируем 

    git clone https://github.com/flutter/flutter.git

Прописываем переменную окружения в .bashrc.

    export PATH="$PATH":"$HOME/flutter/bin"

Проверяем все ли в порядке командой 

    flutter doctor

![uml]({path-to-subject}/images/11.png)

Создаем новый пустой проект и переходим в виртуальные устройства - эмуляторы.

![uml]({path-to-subject}/images/12.png)

![uml]({path-to-subject}/images/13.png)

Сталкиваемся с проблемой доступа.

![uml]({path-to-subject}/images/14.png)

Решаем командой 

    sudo chown zdimon:zdimon /dev/kvm
    

![uml]({path-to-subject}/images/15.png)

Опять проблема.

![uml]({path-to-subject}/images/16.png)

Пробуем скачать библиотеку.

![uml]({path-to-subject}/images/17.png)

Не помогло. Но увидел что доступа к .android у текущего пользователя нет.

![uml]({path-to-subject}/images/18.png)

Добавляю.

    sudo chown -R zdimon:zdimon .android

Наконец то получилось создать устройство.

![uml]({path-to-subject}/images/19.png)

Установим плагин в VSCode.

![uml]({path-to-subject}/images/20.png)

Через View - Command Palette стартуем приложение.

![uml]({path-to-subject}/images/21.png)

![uml]({path-to-subject}/images/22.png)

Получаем ошибку пути к SDK.

![uml]({path-to-subject}/images/24.png)

Создание приложения.

![uml]({path-to-subject}/images/23.png)

Запуск приложение по F5

![uml]({path-to-subject}/images/25.png)




