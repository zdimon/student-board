# Создание репозитория GIT на сервере.

Для создания репозитория необходимо залогиниться на сервере по ssh.

Установить git.

    apt install git

Затем создадим нового пользователя.

    adduser git

Зайдем под этим пользователем.

    su git

Перейдем в его домашнюю директорию.

    cd
    
Создадим папку.

    mkdir repo.git


Зайдем внутрь папки.

    cd repo.git

Запустим создание репозитория с флагом --bare что будет означать что наш репозиторий не будет содержать исходников а только файлы для контроля версий.
git init --bare

Теперь локально можно создать репозиторий.

    git init
    
Добавить удаленный репозиторий в него.
    
    git remote add origin ssh://git@domainname/home/git/repo.git
    
И залить файлы.
    
    git add --all
    git commit -m 'init'
    git push --set-upstream origin master

Ответить на вопрос о добавлении отпечатка сервера.

    The authenticity of host 'dima.webmonstr.com (188.120.241.104)' can't be established.
    ECDSA key fingerprint is SHA256:fQQiO1wiRMkF9jsH7Qk3Qhi1Z1hA1MnYbp6bm+ZHPRs.
    Are you sure you want to continue connecting (yes/no)? 

Клонировать репозиторий можно командой.

    git clone ssh://git@domainname/home/git/repo.git




