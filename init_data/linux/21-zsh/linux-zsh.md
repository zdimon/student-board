# Установка zsh и OH-MY-ZSH.
       
Прежде чем поставить такой инструмент как OH-MY-ZSH вначале нам необходимо установить zsh как коммандный интепретатор по умолчанию.

    sudo apt install zsh

Посмотреть какой шел используется можно коммандой

    echo $SHELL

Посмотреть где находится бинарник команды

    which zsh

Установим zsh как шел по дефолту.

    chsh -s $(which zsh)

После перезапуска терминала видим такую картину.

![start page]({path-to-subject}/images/2.png)

Нажимаем 1 и переходим в главное меню.

Теперь можно побежаться по пунктам и понажимать 0 или что потребуется для того, чтобы запомнить рекомендуемы опции.

Далее нажимаем 0.

Он выкинет нас в шел и скажет что повторить установку конфигурации можно командами

    The function will not be run in future, but you can run
    it yourself as follows:
      autoload -Uz zsh-newuser-install
      zsh-newuser-install -f

![start page]({path-to-subject}/images/3.png)

![start page]({path-to-subject}/images/4.png)

Устанавливаем OH-MY-ZSH

    sh -c "$(wget https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh -O -)"

Установим тему powerlevel10k

[ссылка на репозиторий](https://github.com/romkatv/powerlevel10k)

Вначале установим шрифты meslo.

https://github.com/romkatv/powerlevel10k#meslo-nerd-font-patched-for-powerlevel10k

Скачиваем 4 шрифта, открываем и нажимаем установить.

![start page]({path-to-subject}/images/5.png)

Прописываем шрифт в vscode.

![start page]({path-to-subject}/images/8.png)

Клонируем репозиторий в нужный каталог

    git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ~/powerlevel10k

Вставляем строку в настройки zsh

    echo 'source ~/powerlevel10k/powerlevel10k.zsh-theme' >>~/.zshrc

После перезапуска видим настройщик темы.

![start page]({path-to-subject}/images/6.png)

Проходим по всем пунктам настроек.

Установка автоподсказок

git clone https://github.com/zsh-users/zsh-autosuggestions.git $ZSH_CUSTOM/plugins/zsh-autosuggestions

Установка подсветки кода

git clone https://github.com/zsh-users/zsh-syntax-highlighting.git $ZSH_CUSTOM/plugins/zsh-syntax-highlighting

Прописываем плагины в .zshrc

    plugins=(git zsh-autosuggestions zsh-syntax-highlighting)

## Полный скрипт команд

    wget https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Regular.ttf -P ~/.fonts
    wget https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold.ttf -P ~/.fonts
    wget https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Italic.ttf -P ~/.fonts
    wget https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold%20Italic.ttf -P ~/.fonts
    git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ~/powerlevel10k
    git clone https://github.com/zsh-users/zsh-autosuggestions.git $ZSH_CUSTOM/plugins/zsh-autosuggestions
    git clone https://github.com/zsh-users/zsh-syntax-highlighting.git $ZSH_CUSTOM/plugins/zsh-syntax-highlighting
    sudo apt install zsh
    sudo chsh -s $(which zsh)
    sh -c "$(wget https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh -O -)"
    echo 'source ~/powerlevel10k/powerlevel10k.zsh-theme' >>~/.zshrc
    echo 'zsh' >>~/.bashrc

## Консультант - [Василий Короткий](https://www.linkedin.com/in/vasylii-k-5023bb68/).




