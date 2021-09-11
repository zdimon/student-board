## ООП. В javascript.

Объектно-ориентированное программирование (ООП) — это парадигма программирования, которая использует абстракции, чтобы создавать модели, основанные на объектах реального мира. 

ООП использует несколько техник из ранее признанных парадигм, включая наследование, полиморфизм и инкапсуляция. 

В javascript изначально было применено прототипное программирование.

## Прототипное программирование

Прототипное программирование — это модель ООП которая не использует классы, а вместо этого сначала выполняет поведение класса и затем использует его повторно (эквивалент наследования в языках на базе классов), декорируя (или расширяя) существующие объекты прототипы. 

Принцип ООП заключается в том, чтобы составлять систему из объектов, решающих простые задачи, которые вместе составляют сложную программу. Объект состоит из приватных изменяемых состояний и функций (методов), которые работают с этими состояниями. У объектов есть определение себя (self, this) и поведение, наследуемое от чертежа, т.е. класса (классовое наследование) или других объектов (прототипное наследование).

Наследование — способ сказать, что эти объекты похожи на другие за исключением некоторых деталей. Наследование позволяет ускорить разработку за счёт повторного использования кода.

## Функция - конструктор.

Выполняется с ключевым словом new и обычно начинается с заглавной буквы.

    function test() {
        this.name = 'Dima';
    }

    var me = new test();

При вызове с new создается пустой объект и в него забрасываются свойства из this.


Создадим и экспортируем функцию в библиотечном модуле.

    export var Animal = function(name: string): void {
        this.name = name;
        this.show = function() {
            console.log('Drawing object..');
        };
    } 

Использование в клиентском коде.

    import { Animal } from "./lib";

    var animal = new Animal('Muhtar');
    console.log(animal);
    animal.show();

Мы можем определить метод в прототипе функции, при этом будет экономиться память при наследовании.



    export var Animal = function(name: string): void {
        this.name = name;
    } 
    Animal.prototype.show = function() {
        console.log('Drawing object..');
    }

JS использует дифиренциально наследование, при котором методы не копируются от родителей к потомкам, а вместо этого передается ссылка на метод и потомки имеют скрытую ссылку на методы родителей.

Если теперь создать объект animal.

    var animal = new Animal('dog');

То объект не будет иметь собственного метода show.

    animal.hasOwnProperty('show') === false

И когда мы обращаемся к свойству, которого в объекте нет, то JS начинает его искать в цепочке прототипов (у родителя).

## Создание конструктора - наследника. Метод Object.create()

При вызове такого метода.

     var parent = {
     foo: function() {
     console.log(‘bar’);
     }
    };
    var child = Object.create( parent );
    child.hasOwnProperty(‘foo’); // false
    child.foo(); // ‘bar’

Создается новый пустой обьект и в его прототип помещается parent.

Таким образом мы можем описать функцию-конструктор Dog с новыми свойствами и перетянув свойства конструктора Animal.

    export var Dog = function (name: string): void {
        this.bite = function(){
            console.log('Biting');
        }
        Animal.call(this,name);
    }

А затем связать их по прототипу.

    Dog.prototype = Object.create(Animal.prototype);

