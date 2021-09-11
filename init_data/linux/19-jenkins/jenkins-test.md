## Jenkins. Тесты.

Для сбора информации о тестировании будем использовать плагин junit.

При этом запустим его в секции post при любом запуске.

    pipeline {
        agent any
        stages {
            stage('Test') {
                steps {
                    sh './gradlew check'
                }
            }
        }
        post {
            always {
                junit 'build/reports/**/*.xml'
            }
        }
    }
    
При этом это заставит Jenkins собрать и проанализировать результаты тестов и вывести в виде отчета. 

Проваленые тесты будут соответственно помечены.

Для того, чтобы отменить деплой в случае провала теста необходимо использовать опцию skipStagesAfterUnstable.

Или в случае императивного скрипта проветить переменную

     currentBuild.currentResult == 'SUCCESS'
     
При выполнении тестов часто создаются новые файлы - артифакты.

Которые потом приходится анализировать для выяснения причины провала.

Заархивировать артифакты и сформировать отчет можно так:

    always {
        archiveArtifacts artifacts: 'build/libs/**/*.jar', fingerprint: true
        junit 'build/reports/**/*.xml'
    }
        
### Удаление рабочей директории.

    post {
        always {
            echo 'One way or another, I have finished'
            deleteDir() /* clean up our workspace */
        }
        
### Отсылка сообщения на емейл

    post {
        failure {
            mail to: 'team@example.com',
                 subject: "Failed Pipeline: ${currentBuild.fullDisplayName}",
                 body: "Something is wrong with ${env.BUILD_URL}"
        }
    }

