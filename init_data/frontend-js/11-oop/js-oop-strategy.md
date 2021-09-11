# ООП патерны в javascript.

## Паттерн Стратегия.

Предположим создаем приложении "Зоопарк".

В котором мы имеем следующую иерархию классов.

Класс Животное.

Класс Кот

Класс Собака

Классы Кот и Собака являются наследниками  класса животного.

Прямое использование классов в js (ES6) не будет поддерживаться  старыми браузерами

    SyntaxError: Unexpected token class(…)

И для этого необходимо использовать транспиляторы типа babel webpack и пр. или полифилы.

Однако использование конструкции class является вовсе не обязательным в js и все можно реализовать исключительно в функциональном стиле.

При помощи объектов и функций в яваскрипт мы можем реализовать любой каприз ООП.


Составим данную программу и отобразим животных на странице.

Как создать "типа-класс" в js?

    var Animal = function() {}

или так

    function Animal() {}

При этом фокус в том, что мы полагаем, что эту функцию будут вызывать с ключевым словом new.

Поэтому такие функции называют функции-конструкторы и названия пишут (для удобства) с большой прописной буквы.

Шаблон.

    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <style>
        </style>
        <title>Zoo</title>
      </head>
      <body>
        <h1>Zoo</h1>
        <div id="root"> </div>
        <script src="jquery.min.js" ></script>
        <script src="app.js" ></script>
      </body>
    </html>

## Создадим класс (функцию-конструктор) животного.

Данные.

- размер (пиксели)

Функции.

- отображение

- перемещение

    var Animal = function(){
    };

    Animal.prototype.move = function() {
        console.log('I am mooving')
    };
    Animal.prototype.size = 100
    Animal.prototype.show = function() {
        $("#root").append(`<img src="${this.image}" width="${this.size}" />`);
    };


## Собаки и коты.

Данные.

- картинка

- имя

Функции.

- голос


    var Dog = function(name,image) {
        this.name = name;
        this.image = image;
        this.voice = function() {
            console.log(`gav gav my name is ${this.name} ${this.size}`);
        }
    }

    Dog.prototype = Animal.prototype;

Клиентский код

    var d = new Dog('Bobik','bobik.png');
    d.voice();
    d.show();

## ES6

    class Animal {
        size = 50;
        show() {
            $("#root").append(`<img src="${this.image}" width="${this.size}" />`);
        };
        move() {
            console.log('I am mooving');
        };
    }


    class Dog extends Animal {

        constructor(name,image) {
            super();
            this.name = name;
            this.image = image;
        }

        voice() {
            console.log(`gav gav my name is ${this.name} ${this.size}`);
        }
    }


    var d = new Dog('Bobik','bobik.png');
    d.show();

Добавим кнопки и оформим все на странице.

    class Animal {
        size = 150;
       
        show() {
            const tpl = `
            <div>
                 <img src="${this.image}" width="${this.size}" />
                 <p>
                    <button id="v-button-${this.name}">Voice</button>
                    <button id="m-button-${this.name}">Move</button>
                 </p>
            </div>
            `
            $("#root").append(tpl);
            $('#m-button-'+this.name).on('click',this.move);
            $('#v-button-'+this.name).on('click',()=> {this.voice()});
        };
        move() {
            console.log('I am mooving');
        };
    }


    class Dog extends Animal {

        constructor(name,image) {
            super();
            this.name = name;
            this.image = image;
        }

        voice() {
            console.log(`gav gav my name is ${this.name}`);
        }
    }


    var d = new Dog('Bobik','bobik.png');
    d.show();

**<button id="v-button-${this.name}">Voice</button>** - мы присваиваем уникальный идентификатор кнопкам для подвязки колбеков. Пока полагаем, что имя зверей будет уникальным.


**$(...).on('click',()=> {this.voice()})** - тут мы обвязали колбек стрелочной функцией чтобы не потерять контекст this т.к. если этого не сделать, в нем окажется элемент кнопки и мы не сможем обратиться к this.name внутри метода voice.

Создаем класс для котов.

    class Cat extends Animal {

        constructor(name,image) {
            super();
            this.name = name;
            this.image = image;
        }

        voice() {
            console.log(this);
            console.log(`miau miau my name is ${this.name}`);
        }
    }


Используем классы в клиентском коде.


    var dogObj = new Dog('Bobik','bobik.png');
    dogObj.show();

    var catObj = new Cat('Murka','murka.png');
    catObj.show();

Результат.

![start page]({path-to-subject}/images/2.png)



## Новая задача от заказчика.

Необходимо добавить новую функцию прыжка для всех зверей.


### Решение "В лоб".

Добавляем метод в базовый класс Animal.





