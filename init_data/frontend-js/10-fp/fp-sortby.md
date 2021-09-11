# Сортировка объектов.

Предположим у нас есть массив.

     var fruits = ['cherries', 'apples', 'bananas']

Функция сортировки имееет вид.

    arr.sort([функция-сравниватель])

Ее можно вызвать без аргументов.


    console.log(fruits.sort())

Общий вид функции-сравнивателя.


    function cmp(a,b) {
        if ( a > b ) return 1;
        if ( a < b ) return -1;
        return 0; 
    }

    console.log(fruits.sort(cmp))    

Предположим у нас есть сложныый объект.


    var people = [
        {firstname: 'Dima', lastname: 'Ivanov'},
        {firstname: 'Vova', lastname: 'Putin'},
        {firstname: 'Anna', lastname: 'Karenina'}
    ]

Мы хотим отсортировать его по полю firstname.

Для этого определим такую функцию.

    function cmp(a,b) {
        return ( a.firstеname > b.firstname )? 1: ( a.firstname < b.firstname )? -1: 0;
    }


Усовершенствуем функцию передав параметром значения поля, по которому хотим отсортировать.

    function sortBy(field) {
        return function(a,b) {
            return ( a[field] > b[field] )? 1: ( a[field] < b[field] )? -1: 0;
        }
    }

Проверка.

    console.log(people.sort(sortBy('lastname')))

