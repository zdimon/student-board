# Домашнее задание. Решение.
    

1.Запросите у пользователя его имя и выведите в ответ:
«Привет, его имя!».

    <script>

        var Name = prompt('input your name')

        alert('Hello, '+Name)

    </script>

2.Запросите у пользователя год его рождения, посчитайте,
сколько ему лет и выведите результат. Текущий год укажите
в коде как константу.

    <script>
        const Year  = prompt('input the year of your Birth Date')

        alert(2020-Year)

    </script>

3.Запросите у пользователя длину стороны квадрата и выведите периметр такого квадрата.


    <script>
        var side=prompt('input A side of the square')

        alert(side*4)
    </script>

4.Запросите у пользователя радиус окружности и выведите
площадь такой окружности.

    <script>
        var radius = prompt('input radius of the circle')

        alert(Math.PI*Math.pow(radius,2))

    </script>

5.Запросите у пользователя расстояние в км между двумя
городами и за сколько часов он хочет добраться. Посчитайте скорость, с которой необходимо двигаться, чтобы успеть вовремя.

    <script>
        var Time=prompt('input Time in hours')
        var Dist=prompt('input distance in km')

        alert(Dist/Time +' km/h')

    </script>

6.Реализуйте конвертор валют. Пользователь вводит долла-
ры, программа переводит в евро. Курс валюты храните в
константе.

    <script>
        const kurs = 0.84

        var Dollars =prompt('input summ in dollars')

        alert((Dollars*kurs).toFixed(2) +' Euro')

    </script>

7.Пользователь указывает объем флешки в Гб. Программа
должна посчитать сколько файлов размером в 820 Мб по-
мещается на флешку.

    <script>

       var Vol=prompt('input volume')

       var numb = Math.floor((Vol*1024)/820)

       alert(numb)

    </script>

8.Пользователь вводит сумму денег в кошельке и цену одной
шоколадки. Программа выводит сколько шоколадок может
купить пользователь и сколько сдачи у него останется.
Для решения задачи вам понадобится
оператор % (остаток от деления).

    <script>
        
        var pocket=prompt('input amount of money in your pocket')

        var choc=prompt('input price of the chocolate')

        var buyAble=(pocket/choc)-(pocket/choc)%1

        var left =pocket-buyAble*choc 

        alert('number of chocolates:'+buyAble)

        alert('left in pocket:'+left)       
    </script>


9.Запросите у пользователя трехзначное число и выведите
его задом наперед.

    number.split("").reverse().join("");


    a = number % 10 // 6
    b = Math.floor( ( number % 100 ) / 10 ); //5
    c = Math.floor( ( number % 1000 ) / 100 ); // 4
    alert( `${a}${b}${c}` );








