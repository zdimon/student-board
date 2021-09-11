## Jenkins. Скрипты на groovy.

Последовательность операций сборки или тестирования может быть оформлен в виде pipeline (конвеера) в отдельном файле Jenkinsfile и положен в репозиторий.

Это позволит:

- автоматически сгенерировать конвеер для всех бранчей и pull request-ов.

- держать логику тестов в проекте для аудита

Jenkinsfile скрипт может быть написан в декларативном или императивном стиле.

Декларативный стиль предполагает использование высокоуровневых конструкций языка, которые решают комплексные задачи за раз.

При императивном подходе каждую задачу необходимо более подробно описывать.

Пример как может выглядеть процесс сборки, тестирования и деплоя проекта.

![start page]({path-to-subject}/images/29.png)

Конвеер состоит ис следующих элементов.

**нода (node)** - сервер, на котором все исполняется

**стадия (stage)** - блок, определяющий набор операций для одной задачи (сборки тестирования, деплоя и т.д.). Эти стадии потом будут красиво оформлены интерфейсом Jenkins с указанием времени, статуса и пр.

**шаг (step)** - одна операция. Фактически указание что делать в определенный момент времени.

Рассмотрим варианты оформления Jenkinsfile.

Пример оформления конвеера в декларативном стиле.

    pipeline {
        agent any 
        stages {
            stage('Build') { 
                steps {
                    // 
                }
            }
            stage('Test') { 
                steps {
                    // 
                }
            }
            stage('Deploy') { 
                steps {
                    // 
                }
            }
        }
    }


agent any - говорит о том что выполнять нужно на любом агенте

Для декларативных скриптов применяется агент, для императивных нода.

Пример императивного подхода.

    node('node name') {  
        stage('Build') { 
            // 
        }
        stage('Test') { 
            // 
        }
        stage('Deploy') { 
            // 
        }
    }

Рассмотрим еще один декларативный пример 

    pipeline { 
        agent any 
        options {
            skipStagesAfterUnstable()
        }
        stages {
            stage('Build') { 
                steps { 
                    sh 'make' 
                }
            }
            stage('Test'){
                steps {
                    sh 'make check'
                    junit 'reports/**/*.xml' 
                }
            }
            stage('Deploy') {
                steps {
                    sh 'make publish'
                }
            }
        }
    }

**pipeline** - корневой блок всего конвеера

**agent** - сущность, которая будет выполнять код (нода, или компьютер, или докер образ)

**sh** - выполняет shell команду

**junit** - плагин, собирающий статистику и формирующий xml отчет[ссылка](https://plugins.jenkins.io/junit/)
 
### Установка агента.

Агент будет указывать где именно выполнять работу.

     agent any 
     
выполнит на любом доступном агенте

     agent none
     
При этом мы заставляем прописывать агента для каждого шага, а для всего конвеера устанавливаем в none.

     agent { label 'my-defined-label' } 
     
выберет агента по метке

     agent { node { label 'labelName' } }
     
Работает так же как и с меткой но позволяет использовать дополнительные настройки для ноды, например customWorkspace.

    agent {
        node {
            label 'my-defined-label'
            customWorkspace '/some/other/path'
        }
    }

customWorkspace может быть как относительным так и абсолютным путем и позволяет выйти за пределы дефолтного воркспейса (рабочего каталога)

Агент для докер образа.

    agent {
        docker {
            image 'maven:3-alpine'
            label 'my-defined-label'
            args  '-v /tmp:/tmp'
        }
    }

args - передает аргумены команде docker run

Образ можно собрать из файла Dockerfile

    agent {
        dockerfile {
            filename 'Dockerfile.build'
            dir 'build'
            label 'my-defined-label'
            additionalBuildArgs  '--build-arg version=1.0.2'
            args '-v /tmp:/tmp'
        }
    }

То же что запуск 

    "docker build -f Dockerfile.build --build-arg version=1.0.2 ./build/


Пример запуска команды внутри контейнера в декларативном стиле.

    pipeline {
        agent { docker 'maven:3-alpine' } 
        stages {
            stage('Example Build') {
                steps {
                    sh 'mvn -B clean verify'
                }
            }
        }
    }

Агента можно определять для разных стадий.

    pipeline {
        agent none 
        stages {
            stage('Example Build') {
                agent { docker 'maven:3-alpine' } 
                steps {
                    echo 'Hello, Maven'
                    sh 'mvn --version'
                }
            }
            stage('Example Test') {
                agent { docker 'openjdk:8-jre' } 
                steps {
                    echo 'Hello, JDK'
                    sh 'java -version'
                }
            }
        }
    }

## Конструкция post

Позволяет выполнить код при определенных обстоятельствах, условиях или результатах выполнения стадий (в зависимосте где его всунуть).

### Условия.

**allways** - выполнится всегда

**failure** - только когда провален

**success** - только когда успешно выполнен

**changed** - только если результаты отличаются от предыдущего запуска

**fixed** - если предыдущий запуск был провален а текущий нет

**regression** - наоборот

Пример.

    pipeline {
        agent any
        stages {
            stage('Example') {
                steps {
                    echo 'Hello World'
                }
            }
        }
        post { 
            always { 
                echo 'I will always say Hello again!'
            }
        }
    }
    
Можно определять сразу несколько вариантов.

    pipeline {
        agent any
        stages {
            stage('Test') {
                steps {
                    sh 'echo "Fail!"; exit 1'
                }
            }
        }
        post {
            always {
                echo 'This will always run'
            }
            success {
                echo 'This will run only if successful'
            }
            failure {
                echo 'This will run only if failed'
            }
            unstable {
                echo 'This will run only if the run was marked as unstable'
            }
            changed {
                echo 'This will run only if the state of the Pipeline has changed'
                echo 'For example, if the Pipeline was previously failing but is now successful'
            }
        }
    }
        

### Переменные окружения. Директива environment.

Пары ключ - значение, которые передадуться внутрь каждого шага.

    pipeline {
        agent any
        environment { 
            CC = 'clang'
        }
        stages {
            stage('Example') {
                environment { 
                    AN_ACCESS_KEY = credentials('my-predefined-secret-text') 
                }
                steps {
                    sh 'printenv'
                }
            }
        }
    }
 
Как видим существует иерархия видимости переменных в зависимости куда их втыкать ко всему конвееру или конкретному шагу.

Еще пример вывода переменных окружения.

    pipeline {
        agent {
            label '!windows'
        }

        environment {
            DISABLE_AUTH = 'true'
            DB_ENGINE    = 'sqlite'
        }

        stages {
            stage('Build') {
                steps {
                    echo "Database engine is ${DB_ENGINE}"
                    echo "DISABLE_AUTH is ${DISABLE_AUTH}"
                    sh 'printenv'
                }
            }
        }
    }


### Директива options.

Позволяет конфигурировать некоторые полезные опции при выполнении конвеера.

**buildDiscarder** - управляет сохранением артифактов сборки и вывода в консоль

**checkoutToSubdirectory** - проверяет наличие произвольного каталога

    options { checkoutToSubdirectory('foo') }
    
**disableConcurrentBuilds** - помогает исключить одновременное использование разделяемого ресурса

**newContainerPerStage** - будет создавать по новому контейнеру на каждую стадию

**timeout** - таймаут по которому нужно прервать конвеер

    pipeline {
        agent any
        options {
            timeout(time: 1, unit: 'HOURS') 
        }
        stages {
            stage('Example') {
                steps {
                    echo 'Hello World'
                }
            }
        }
    }

**retry** - сколько раз повторить после провала

Опции можно устанавливать как ко всему конвееру так и к определенным стадиям.

### Триггеры

Определяют условие при котором конвеер должен быть запущен.

**cron** -  определяет расписание для запусков

    triggers { cron('H */4 * * 1-5') }

**pollSCM**  - определяет кроновый интервал для проверки изменений в исходниках. Если изменения обнаружены, то запускается конвеер.

    triggers { pollSCM('H */4 * * 1-5') }
    
**upstream** - принимает строку с задачами через запятую и порог. Если хоть одна задача завершилась с указанным порогом, то конвеер перезапустится.

     triggers { upstream(upstreamProjects: 'job1,job2', threshold: hudson.model.Result.SUCCESS) }

Пример.

    pipeline {
        agent any
        triggers {
            cron('H */4 * * 1-5')
        }
        stages {
            stage('Example') {
                steps {
                    echo 'Hello World'
                }
            }
        }
    }

**triggers{ cron('H/15 * * * *') }** - каждые 15 мин.

**triggers{ cron('H(0-29)/10 * * * *') }** - каждые 10 мин в первой половине часа

### Директива tools.

Позволяет предустановить программы в конвеер.

    pipeline {
        agent any
        tools {
            maven 'apache-maven-3.0.1' 
        }
        stages {
            stage('Example') {
                steps {
                    sh 'mvn --version'
                }
            }
        }
    }

### Директива input.

Позволяет забирать данные, вводимые пользователем.

    pipeline {
        agent any
        stages {
            stage('Example') {
                input {
                    message "Should we continue?"
                    ok "Yes, we should."
                    submitter "alice,bob"
                    parameters {
                        string(name: 'PERSON', defaultValue: 'Mr Jenkins', description: 'Who should I say hello to?')
                    }
                }
                steps {
                    echo "Hello, ${PERSON}, nice to meet you."
                }
            }
        }
    }
    
К примеру, мы можем это использовать для получения разрешения на деплой кода на продакшин сервер после успешных тестов.
    
### Директива when

Определяет условие, при котором нужно выполнять стадию.


Например если бранч соответствует маске.

    when { branch pattern: "release-\\d+", comparator: "REGEXP"}


Когда билд содержит тег.

    when { buildingTag() }
    
Когда в логе содержится искомая строка.

     when { changelog '.*^\\[DEPENDENCY\\] .+$' }
     
Если исходники содержат интересующие файлы

    when { changeset "**/*.js" }
    
При запросах Pull Request

    when { changeRequest() }.

Если присутствует определенная переменная в окружении.

    when { environment name: 'DEPLOY_TO', value: 'production' } 
 
Если присутствует тег

    when { tag "release-*" }.
    
Отрицание     
     
     when { not { branch 'master' } }
     
Если сработал определенный триггер

    when { triggeredBy 'TimerTrigger' }     
 
Пример.

    pipeline {
        agent any
        stages {
            stage('Example Build') {
                steps {
                    echo 'Hello World'
                }
            }
            stage('Example Deploy') {
                when {
                    branch 'production'
                }
                steps {
                    echo 'Deploying'
                }
            }
        }
    }
         
Условия можно комбинировать.

   when {
        branch 'production'
        environment name: 'DEPLOY_TO', value: 'production'
    }
     
Либо влаживать друг в друга.

    when {
        allOf {
            branch 'production'
            environment name: 'DEPLOY_TO', value: 'production'
        }
    }     
    
## Последовательные стадии

Стадии могут быть не только вложенными, но и определять последовательность при помощи директив  steps, stages, parallel или matrix. 

Паралельное выполнение (paralel).

        stage('Parallel In Sequential') {
            parallel {
                stage('In Parallel 1') {
                    steps {
                        echo "In Parallel 1"
                    }
                }
                stage('In Parallel 2') {
                    steps {
                        echo "In Parallel 2"
                    }
                }
            }
        }
                     
stage может содержать только один блок paralel.

Установка параметра failFast true позволяет прервать выполнение в случае провала онтой из стадий.

        stage('Parallel Stage') {
            when {
                branch 'master'
            }
            failFast true
            parallel {
                stage('Branch A') {
                    agent {
                        label "for-branch-a"
                    }
                    steps {
                        echo "On Branch A"
                    }
                }
              ....
              
## Matrix

Позволяет конструировать матрицу из ячеек.

Например так можно создать матрицу 4 на 3 из 12 значений.

    matrix {
        axes {
            axis {
                name 'PLATFORM'
                values 'linux', 'mac', 'windows'
            }
            axis {
                name 'BROWSER'
                values 'chrome', 'edge', 'firefox', 'safari'
            }
        }
        // ...
    }
    
Если теперь вложить внутрь стадии, то они выполнятся для каждой ячейки последовательно.

    matrix {
        axes {
            axis {
                name 'PLATFORM'
                values 'linux', 'mac', 'windows'
            }
        }
        stages {
            stage('build') {
                // ...
            }
            stage('test') {
                // ...
            }
            stage('deploy') {
                // ...
            }
        }
    }
    
## Директива script

Внутрь этой директивы может быть вложен код groovy и выполнен на уровне одного шага.

    pipeline {
        agent any
        stages {
            stage('Example') {
                steps {
                    echo 'Hello World'

                    script {
                        def browsers = ['chrome', 'firefox']
                        for (int i = 0; i < browsers.size(); ++i) {
                            echo "Testing the ${browsers[i]} browser"
                        }
                    }
                }
            }
        }
    }

## Условия

    node {
        stage('Example') {
            if (env.BRANCH_NAME == 'master') {
                echo 'I only execute on the master branch'
            } else {
                echo 'I execute elsewhere'
            }
        }
    }
    
# Императивные скрипты.    
    
## Исключения

    node {
        stage('Example') {
            try {
                sh 'exit 1'
            }
            catch (exc) {
                echo 'Something failed, I should sound the klaxons!'
                throw
            }
        }
    }
