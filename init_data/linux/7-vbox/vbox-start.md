# Виртуальная машина Virtual Box. 

## Установка Virtual Box на Ubuntu.
        

Для начала давайте установим пакеты, которые нам понадобяться:

    sudo apt install gcc make linux-headers-$(uname -r) dkms

Дальше необходимо добавить репозиторий и ключики. 

Для этого выполните:

    wget -q https://www.virtualbox.org/download/oracle_vbox_2016.asc -O- | sudo apt-key add -

    wget -q https://www.virtualbox.org/download/oracle_vbox.asc -O- | sudo apt-key add -

    sudo sh -c 'echo "deb http://download.virtualbox.org/virtualbox/debian $(lsb_release -sc) contrib" >> /etc/apt/sources.list.d/virtualbox.list'

Обновляем репозиторий.

    sudo apt update

Установка.

    sudo apt install virtualbox-6.0

![start page]({path-to-subject}/images/1.png)

![start page]({path-to-subject}/images/2.png)

## Ставим Kali Linux.

[скачиваем образ](https://www.kali.org/downloads/)

проходи квест.

![start page]({path-to-subject}/images/3.png)

![start page]({path-to-subject}/images/4.png)

![start page]({path-to-subject}/images/5.png)

![start page]({path-to-subject}/images/6.png)

![start page]({path-to-subject}/images/7.png)

![start page]({path-to-subject}/images/8.png)

![start page]({path-to-subject}/images/9.png)

![start page]({path-to-subject}/images/10.png)

![start page]({path-to-subject}/images/11.png)

Первая проблема с дровами.

![start page]({path-to-subject}/images/12.png)

[ссылка на решение](https://askubuntu.com/questions/920689/how-to-fix-modprobe-vboxdrv-error-in-virtualbox)

Пробуем, но сначала закрываем приложение.

    sudo apt install linux-headers-generic

    sudo apt-get install -y virtualbox-dkms

Ошибка

![start page]({path-to-subject}/images/15.png)

При просмотре

    dmesg

![start page]({path-to-subject}/images/13.png)

После отключения UEFI в биосе

![start page]({path-to-subject}/images/19.png)    

И появлении такого при первой перегрузке

![start page]({path-to-subject}/images/18.png)   

Потом запуска

    sudo dpkg-reconfigure virtualbox-dkms

![start page]({path-to-subject}/images/16.png)

Наконец пошло дело.

![start page]({path-to-subject}/images/20.png)








