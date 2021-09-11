# Условия.
     
Под условием (англ. — condition) в программировании
подразумевается особый вид выражений, приводящих
к одному из двух возможных результатов.

Альтернативно, можно говорить «условие ложно» либо «условие истинно».

Т.е. результатом условия может быть true или false.

![start page]({path-to-subject}/images/1.png)

Синонимы условному выражению - предикативное выражение, булево выражение.

## Условный оператор if.

Его называют оператором ветвления.

Синтаксис.

    if(condition) 
        statement;

Выполняется в случае если улсовие равно true    

Если необходимо выполнить несколько операций то их заключают в фигурные скобки.

    if(condition) {
        statement1;
        statement2;
        statement3;
    }

Пример.

    if(1>0) alert("Yes")

## Расширенная форма условия.

    if(condition)
        statement_if_true;
    else
        statement_if_false;

При множественных условиях.

    if(condition1)
        statement_if_true;
    else if(condition2)
        statement_if_true;
    else
        statement_if_false;




Применяется когда нужно отработать и ситуацию, при которой условие не выполняется.

Аналогично с группой операций.

    if(condition) {
        statement_if_true1;
        statement_if_true2;
        statement_if_true3;
    }
    else {
        statement_if_false1;
        statement_if_false2;
    }

Синонимами ложного результата кроме false является также 0 "undefined", "null" или пустая строка.

Поэтому проверить на четность числа можно так.

    if(x % 2 == 0)...

Или более коротко, воспользовавшись динамическим преобразованием типов.

    if(x % 2)

## Тернарный оператор.

Синтаксис.

    condition ? exprIfTrue : exprIfFalse 

Решает проблему при которой нам необходимо поместить в переменную то или иное значение исходя из условия.

Таким образом такая конструкция:

    if(x % 2) {
       parity = "even";
    }
    else {
       parity = "odd";
    }    

Может быть записана более коротко.

    parity = x % 2 == 0 ? “even” : “odd”

Для более понятной записи используют круглые скобки.

    parity = (x % 2 == 0) ? “even” : “odd”

## Опрератор switch

Для обработки множественных условий не всегда удобен оператор if

Например.

    if(protocol == "HTTP") description = "Hypertext transfer protocol";
    else if(protocol == "HTTPS") description = "Secure hypertext transfer protocol";
    else if(protocol == "FTP") description = "File transfer protocol";
    else description = "Unsupported protocol";

Для того чтобы упростить подобный множественный
анализ применяется оператор «switch».

    switch(protocol){
        case "HTTP":
            description = "Hypertext transfer protocol";
            break;
        case "HTTPS":
            description = "Secure hypertext transfer protocol";
            break;
        case "FTP":
            description = "File transfer protocol";
            break;
        default :
            description = "Unsupported protocol";
    }

Инструкция прерывания breack используется для того, чтобы исключить дальнейшее продолжение выполнения кода.

