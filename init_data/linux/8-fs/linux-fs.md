# Файловая система

## Структура диска.

Жесткий диск, флешка, ssd это все имеет блочную органицацию данных.

LBA (англ. Logical block addressing) — стандартизованный механизм адресации и доступа к блоку данных.

При котором системному контроллеру нет необходимости учитывать специфику накопителя (например, геометрию жёсткого диска — количество цилиндров, головок, секторов на дорожке).

Жесткий диск не умеет адресовать свое пространство побайтно, условно оно разбито на блоки. 

В LBA каждому адресуемому блоку назначается уникальный номер — целое число, начиная с нуля.

Размер блока в обычных дисках = 512 байт

![start page]({path-to-subject}/images/1.png)

Как видно из рисунка, блоки LBA обозначен как уровень HDD.

Просмотреть размер блока.

    sudo blockdev --getpbsz /dev/sdb

Уровнем выше размечен раздел, один на весь диск (для простоты). 

Чаще всего используют разметку разделов двух типов: msdos и gpt. Соответственно msdos — старый формат, поддерживающий диски до 2Tb, gpt — новый формат, способный адресовать до 1 зеттабайта 512 байтных блоков. В нашем случае имеем раздел типа msdos, как видно из рисунка, раздел при этом начинается с блока №1, нулевой же используется для MBR.


sudo tune2fs -l /dev/sdb6

В первом разделе создана файловая система ext4

Посмотреть размер блока файловой системы можно так:

    tune2fs -l /dev/sdb6

![start page]({path-to-subject}/images/2.png)

Файл состоит из одного или нескольких блоков файловой системы, в которых хранятся его данные. Зная имя файла, как его найти? Какие блоки читать?


Вот тут нам и пригождаются inode. В файловой системе ext2fs есть «таблица», в которой содержится информация по всем inode. Количество inode в случае с ext2fs задается при создании файловой системы. 

В inode содержится нужная нам информация: список блоков файловой системы для искомого файла. Как найти номер inode для указанного файла?


Соответствие имени и номера inode содержится в директории, а директория в ext2fs — это файл особого типа, т.е. тоже имеет свой номер inode. Чтоб разорвать этот порочный круг, для корневой директории назначили «фиксированный» номер inode «2».

Смотрим содержимое inode за номером 2:

    sudo debugfs /dev/sdb6
    debugfs:  stat <2>

![start page]({path-to-subject}/images/3.png)

Как видно нужная нам директория сидит в блоке под номером 9293.

В ней мы найдем номер нода для папки home, и так далее по цепочке, пока не увидим номер нода для запрошенного файла.

# Полезные команды

## Команды просмотра всех блоковых устройств (дисков)

    sudo lsblk

    sudo fdisk -l

## Информация о устройствах

    sudo lshw

Выясняем идентификатор устройства UUID

    sudo blkid

## Монтирование устройства в папку

    sudo mount -t vfat /dev/sdb1 /media/usbstick 

    sudo mount /dev/hda1 /home/user/Desktop/whereEver



## Монтирование диска при запуске системы

Создаем каталог для монтирования, под него групу и устанавливаем права для каталога группе.

    sudo mkdir /data
    sudo groupadd data
    sudo chown -R :data /data

Добавляем текущего пользователя к группе.

    sudo usermod -aG data USERNAME

Открываем конфиг.

    sudo nano /etc/fstab

Добавляем.

    UUID=14D82C19D82BF81E /data    auto nosuid,nodev,nofail,x-gvfs-show 0 0

UUID=14D82C19D82BF81E - is the UUID of the drive. You don't have to use the UUID here. You could just use /dev/sdj, but it's always safer to use the UUID as that will never change (whereas the device name could).
/data - is the mount point for the device.

auto - automatically mounts the partition at boot 

nosuid - specifies that the filesystem cannot contain set userid files. This prevents root escalation and other security issues.

nodev - specifies that the filesystem cannot contain special devices (to prevent access to random device hardware).

nofail - removes the errorcheck.

x-gvfs-show - show the mount option in the file manager. If this is on a GUI-less server, this option won't be necessary.

0 - determines which filesystems need to be dumped (0 is the default).

0 - determine the order in which filesystem checks are done at boot time (0 is the default).

Тестируем монтирование.

    sudo mount -a

## Форматирование

Вначале стоит отмонтировать диск.

    sudo umount /dev/sdc1

Забиваем все нулями

    dd if=/dev/zero of=/dev/[disk device]

Форматируем в fat

    sudo mkfs.vfat /dev/sdc1

Форматируем в ntfs

    sudo mkfs.ntfs /dev/sdc1

Форматируем в ext4

    sudo mkfs.ext4 /dev/sdc1

Удаление таблицы разделов

    sfdisk --delete /dev/sda

## Создание образа диска 

    sudo dd if=/dev/mmcblk0p2 of=~/disk/backup.img

где /dev/mmcblk0p2 - диск например флеш накопитель


## Раскатка образа на диск

     sudo dd if=~/disk/backup.img of=/dev/mmcblk0p2 

## СОЗДАНИЕ SQUASHFS ОБРАЗА

Преимущество Squashfs в том, что это полноценная файловая система в одном файле, которую можно очень быстро примонтировать и быстро извлечь нужные файлы. 

    sudo mksquashfs / /root-backup.sqsh -e root-backup.sqsh home media dev run mnt proc sys tmp
