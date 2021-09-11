# Bash. Работа со строками. Команды tail head join wc sort sed.
 
##  head  tail

Показывают начальные и конечные строки файлов

    head -4 /etc/passwd

    tail -4 /etc/passwd

Может использоваться с флагом -f для отслеживания добавления новых строк.

## Команда join обьеденяет поля ф файлах.

    //displaying the contents of file1.txt//
    $cat file1.txt
    1 AAYUSH
    2 APAAR
    3 HEMANT
    4 KARTIK
    5 DEEPAK

    //displaying contents of file2.txt//
    $cat file2.txt
    1 101
    2 102
    3 103
    4 104

    //using join command//
    $join file1.txt file2.txt
    1 AAYUSH 101
    2 APAAR 102
    3 HEMANT 103
    4 KARTIK 104

