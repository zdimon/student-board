# Jenkins. Работа с GIT.
     
Для работы с репозиторием в начале необходимо добавить пользователя и его приватные ключи, используемые в git.

![start page]({path-to-subject}/images/24.png)

Затем можно создать следующую задачу типа Pipeline.

    node('pi') {
        stage('Git clone') {
            dir('/home/zdimon/project01') {
                git credentialsId: '0acbc9ab-ca88-4fbd-a13e-59c3c81c1722', url: 'git@github.com:zdimon/web-starter.git', branch: 'master'
            
                script {
                    def stdOut = sh(script: "pwd && ls -alh",
                        returnStdout: true)
                    echo stdOut
                }
            }
        }
    }


node('pi') - указываем в какой ноде (на каком сервере) работать.

stage('Git clone') - обозначиваем статию.

dir('/home/zdimon/project01') { ... } - говорим в какой директории работать.

Если директорию не указывать, то jenkins для каждой задачи будет создавать отдельный каталог внутри папки workspace.

При формировании команды клона я воспользовался помошником.

![start page]({path-to-subject}/images/26.png)

![start page]({path-to-subject}/images/25.png)

Далее в блоке script мы выполням bash команду, заносим ее вывод в файл и выводим его в консоль.

        script {
            def stdOut = sh(script: "pwd && ls -alh",
                returnStdout: true)
            echo stdOut
        }

Результат.

![start page]({path-to-subject}/images/27.png)

![start page]({path-to-subject}/images/28.png)

## Привязываем запрос на сборку к git хуку.

В папке .git есть каталог hooks c шаблонами bash скриптов, срабатывающих в разных ситуациях.

Создаем новый файл post-commit

    #!/bin/sh
    echo "Post commit"

Добавляем права на выполнение

    chmod +x ./git/hooks/post-commit
    
Теперь этот скрипт будет выполнятся при каждом коммите.

Можно в него добавить запрос на сервер с jenkins.

    curl http://yourserver/jenkins/git/notifyCommit?url=<URL of the Git repository>
    
Этот запрос просканирует все задачи, которые сконфигурированы с проверкой специфичного url.

Еще один вариант запуска.

    #!/bin/bash
    /usr/bin/curl --user USERNAME:PASS -s \

    http://jenkinsci/job/PROJECTNAME/build?token=1qaz2wsx
    
Для работы этого запроса необходимо сконфигурировать задачу удаленным триггером с токеном.    
    
Запуск определенной задачи по ее имени.

    curl http://localhost:8080/job/someJob/build?delay=0sec
    
    curl -X POST http://:/job/job-name-in-jenkins/build?delay=0sec --user user:password
    









