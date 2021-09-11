# Удаленная разработка с Visual Studio Code.
       

Расширение Visual Studio Code Remote позволяет открыть произвольную папку на удаленной машине или докер контейнере и работать внути ее.

Установим этот плагин Remote Development.

После установки появится значек внизу.

![start page]({path-to-subject}/images/2.png)


Добавим соединение в .ssh/config

    Host 78.46.160.16
      HostName pl
      User pl

Либо можно щелкнуть на значек и выбрать Remote-SSH Connect to host.

## Синхронизация через Sync-Rsync

Ставим плагин.

[ссылка на страницу](https://marketplace.visualstudio.com/items?itemName=vscode-ext.sync-rsync)

Теперь можем указывать в .vscode/settings.json каталоги, которые хотим синхронизировать.


{
    "sync-rsync.sites": [
        {
            "localPath":"main/",
            "remotePath":"pressa@95.163.104.122:/home/pressa/pressa-besa/main"
        }
    ]
}

Однако для синхронизации необходимо запускать команду ctrl+shift+p Sync-Rsync: Sync Local to Remote


