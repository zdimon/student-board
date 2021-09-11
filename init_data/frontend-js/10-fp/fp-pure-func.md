## Чистые функции.
      
Чистыми называют те функции которые работают исключительно с передаваемыми в них параметрами.

Если ф-ция работает с переменными, определенными за ее пределами, то она не является чистой и имеет побочный эффект.

Допустим у нас есть список.

    var fruits = ['cherries', 'apples', 'bananas']

Определим функцию перебора элементов массива.


    function forEach(arr,fn){
        for(let i=0; i<=arr.length-1; i++){
            fn(arr[i]);
        }
    }

Применим ее для вывода элементов в консоль.

    forEach(fruits,(el)=> console.log(el))

Сделаем функцию, которая изменяет элементы массива.

    function map(arr,fn){
        for(let i=0; i<=arr.length-1; i++){
            arr[i] = fn(arr[i]);
        }
    }


    map(fruits,(el)=> el.toUpperCase())

    console.log(fruits);

## Функция every.

Предположим есть два массива.

    var myarr1 = [NaN,2,NaN,NaN];

    var myarr2 = [NaN,NaN,NaN,NaN];

Необходимо проверить есть ли в массиве хоть один елемент, не соотвествующий условию, которое заключено в функцию, и вернуть true если все соответствуют или false если хотябы один нет.


    const every = (arr,fn) => {
        let result = true;
        for(let i=0;i<arr.length;i++){
            result = result && fn(arr[i]);
        }
        return result;
    };

В js есть встроенная функция isNaN, проверяющая является ли значение числом.

    console.log(every(myarr1,isNaN)); false

    console.log(every(myarr2,isNaN)); true

## Функция some.

Делает наоборот, возвращает true если хотя бы один соответствует и возвращает true, в противном случае возвращается false. 

    const some = (arr,fn) => {
        let result = false;
        for(let i=0;i<arr.length;i++){
            result = result || fn(arr[i]);
        }
        return result;
    };

Необходимо отметить неоптимальную работу функции, при которой она в любом случае пройдет весь массив целиком, даже если первый элемент вернет true и необходимости идти по массиву дальше нет.

При помощи таких функций можно писать программы в функциональном стиле, не используя операторов условий (if else) и циклов (for).

Например чтобы определить присуствует ли в массиве 

    var myarr1 = [NaN,2,NaN,'Dima'];

хоть одно значение 'Dima' можно так

    console.log(some(myarr1,(e) => e === 'Dima'));

### Сортировка объектов.

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

## Замыкания.

С замыканием связана область памяти, в которую помещаются переменные в момент возврата одной функции из другой.

Проще говоря замыкание - это внутренняя функция с переменными, которые в нее попадают из внешней.

    function outer() {
        function inner() {
        }
    }

Функция inner называется функцией - замыканием.

Вся сила этих функций заключена в механизме доступа к области видимости переменных внутри текущей функции.

Всего их 3.

1. Переменные, обьявленные в своей собственной области текущей функции.

2. Переменные, объявленные в глобальном пространстве (за пределами функций)

3. Переменные, объявленные во внешней функции относительно текущей.

Вариант 1.

    function outer() {
        function inner(){
            let a = 1;
            console.log(a);
        }
        inner();
    }

Вариант 2.

    var global = 3;
    function outer() {
        function inner(){
            let a = 1;
            console.log(global);
        }
        inner();
    }

Вариант 3.

    
    function outer() {
        let outer = 'Outer';
        function inner(){
            let a = 1;
            console.log(outer);
        }
        inner();
    }
    
При этом внешняя функция как бы замыкает пространство видимости для внутренней функции-замыкании и делает доступным переменные из нее.

Попробуем возвратить внутреннюю функцию из внешней, которой еще и передадим параметр.


    var fn = (arg) => {
        let outer = 'Visible';
        let innerFn = () => {
            console.log(outer);
            console.log(arg);
        } 
        return innerFn;
    }

Вызов будет следующим.

    var closureFn = fn(5);
    closureFn();

Вначале мы присваиваем переменной результат выполнения fn которая принимает аргумент и возвращает функцию-замыкание.

И эта функция-замыкание будет иметь доступ как к аргументу arg так и к outer.

## Функция unary.

Допустим мы хотим преобразовать строки массива в числа.

    console.log(['1','2','3'].map((parseInt)))
 
вывод 

    
     [1, NaN, NaN]

Проблема в том что функция map имеет следующую сигнатуру

    array.map(callback(item, index, array))

[ссылка на перебирающие методы](https://learn.javascript.ru/array-iteration)

А функция parseInt имеет сигнатуру 

    parseInt(string, radix);

где radix эта основа числа в математике и когда map туда заталкивает порядковый номер элемента index - это изменяет ее работу и не желательно

Поэтому создадим функцию unary, которая отссеит все лишние параметры, передаваемые map.


    const unary = function(func) {
        if (func.length === 1){
            return func
        } else {
            return function(el)  {
                return func(el);
            }
        }
    }

Или более которкий вариант со стрелочными функциями и тернарным оператором.

    const unary = (func) => (func.length === 1)? func : (el) => func(el);

И теперь воспользуемся.

    console.log(['1','2','3'].map((unary(parseInt))));

## Работа с массивами.

### Функция map

Смысл - изменить массив функцией.

    const map = (array, fn) => {
        let results = [];
        for(const value in array) {
            results.push(fn(value));
        }
        return results;
    }

Применение.

    console.log(map(['1','2','3'],(el) => parseInt(el)));

Функция filter.

### Функция filter

Смысл - отсеить элементы массива, не удовлетворяющих условиям в передаваемой функции (колбеке).

    const filter = (arr,func) => {
        let result = [];
        for(const value of arr) {
            (func(value)) ? result.push(value): undefined;
        }
        return result;    
    }

Отбираем четные числа.

    console.log(filter([1,2,3,4,5,6],(el) => el%2 === 0));


