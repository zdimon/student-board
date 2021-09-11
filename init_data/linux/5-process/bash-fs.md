# Консоль. Работа с файловой системой.

# pwd

Получение текущей директории.

# cd  <Directory>
    
Смена каталога.

Может использоваться без параметров для перехода в домашний каталог.    

# mkdir [options] <Directory>

Создание директории.

    mkdir /home/ryan/foo
    mkdir ./blah
    mkdir ../dir1
    mkdir ~/linuxtutorialwork/dir2

Мы можем использовать абсолютные и относительные пути.

Мы можем использовать .. для создания каталогов на уровне выше текущего каталога.

Мы можем использовать префикс ~ для обозначения домашнего каталога.

Полезные опции.

**-p** - говорим о том, что хотим создать родительские каталоги если их нет.

**-v** - подробный вывод что происходит.

## rmdir [options] <Directory>

Удаление директорий.

Опции аналогичные с mkdir. 


## touch [options] <filename>

Создание пустого файла.

## cp [options] <source> <destination>

Копирование файла или директории.

    cp /home/ryan/linuxtutorialwork/example2 example3
    cp example2 ../../backups
    cp example2 ../../backups/example4
    cp /home/ryan/linuxtutorialwork/example2 /otherdir/foo/example5
    
При копированиифайла он создастся с новым именем, указанным в source.

При копировании директории, она будет скопирована со всеми файлами с теми же именами но необходимо использовать ключ -r.  
    

## mv [options] <source> <destination>

Перемещение файлов и директорий.

Работает так же как cp но при перемещении директории не обязательно использовать ключ -r.

## rm [options] <file>

Удаляет файлы и не пустые директории.

Для того, чтобы удалить не пустую директорию используется ключ -r.


