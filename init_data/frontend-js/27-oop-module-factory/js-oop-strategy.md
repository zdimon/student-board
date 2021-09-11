# ООП патерны в javascript.

После появления ООП программный мир преобразился с использованием классов и объектов.

Однако это во многих сложных проектах приводило к неразберихе из за отсутствия признанных методик решения типовых задач.

Эрих Гамма внес в это ясность и открыл нам мир паттернов, которые он разделил на 3 категории:

**Порождающие шаблоны** - которые описывают как правильно создавать объекты.

**Поведенческие** - описывающие взаимодействия между классами и объектами

**Структурные** - дают представления о правильной архитектуре классов и объектов

## Паттерн Стратегия (из разряда поведенческих).

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

- отображение;

- перемещение.

Пример кода.

    var Animal = function(){
    };

    Animal.prototype.move = function() {
        console.log('I am mooving')
    };
    Animal.prototype.size = 100
    Animal.prototype.show = function() {
        $("#root").append(`<img src="${this.image}" width="${this.size}" />`);
    };

Мы забрасываем методы в prototype для того, чтобы наследоваться и при этом не плодить методы в памяти.


## Собаки и коты.

Данные.

- картинка

- имя

Функции.

- голос

Пример функции-конструктора.

    var Dog = function(name,image) {
        this.name = name;
        this.image = image;
        this.voice = function() {
            console.log(`gav gav my name is ${this.name} ${this.size}`);
        }
    }

    Dog.prototype = Animal.prototype;

Клиентский код.

    var d = new Dog('Bobik','bobik.png');
    d.voice();
    d.show();

## Перепишем на классах, используя ES6

Слава богу, он поддерживается всеми современными браузерами.

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

Из неочевидного отметим:

**id="v-button-${this.name}** - мы присваиваем уникальный идентификатор кнопкам для подвязки колбеков. Пока полагаем, что имя зверей будет уникальным.


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

Добавляем метод в базовый класс Animal c кнопкой.

    class Animal {
        size = 150;
       
        show() {
            const tpl = `
            ...
                    <button id="j-button-${this.name}">Jump</button>
            ...
            `
            ...
            $('#j-button-'+this.name).on('click',()=> {this.jump()});
        };
        ...
        jump() {
            console.log('I am jumping!!!');
        };

    }

В результате на всех дочерних к Animal объектах классов Dog и Cat появилась новая кнопка.

Это не удивительно т.к. эти классы наследуют (расширяют) класс Animal ключевым словом extends.

### Проблема.

Как оказалось, в нашем зоопарке присутствует ряд животных, которые изготовлены из дерева и представляют собой чучела и соответственно не могут прыгать. 

    class WoodenCat extends Animal {

        constructor(name,image) {
            super();
            this.name = name;
            this.image = image;
        }

        voice() {
            console.log(`I am a wooden cat miau miau my name is ${this.name}`);
        }
    }


    var catMaket = new WoodenCat('WoodMurka','catwood.png');
    catMaket.show();


![start page]({path-to-subject}/images/3.png)


При решении с методом в базовом классе у нас прыгают все (.

### Первый вариант решения.

Переопределять метод в дочерних классах.



    class WoodenCat extends Animal {

        ....
        
        jump() {
            console.log(`I can not jump!`);
        }
    }

Цель достигнута.

![start page]({path-to-subject}/images/5.png)

Однако такой подход имеет недостатки.

При добавлении новых классов, необходимо в каждом переопределять этот метод и дублировать его.

Но самое страшное то, что если логика этого метода будет изменяться, то нам прийдется изменять его по всем классам.

Для того, чтобы этого избежать, данную функцию выносят в отдельный класс и вставляют его экземпляр (объект) внутрь класса животного. При этом в соответствующем методе jump  базового класса Animal вызывается метод внутреннего обьекта.

Данный прием носит название полиморфизма.

Классы, определяющие способность прыгать.


    class CanJump {
        jump() {
            console.log(`Jump Jump!`);
        }
    }

    class CanNotJump {
        jump() {
            console.log(`I can not jump!`);
        }
    }

Изменения базового класса Animal.

    class Animal {
       ...
        constructor(canJumpObj){
            this.canJump = canJumpObj; 
        }
       
       ...

        jump() {
            this.canJump.jump();
        };

    }

"Протаскиваем" объекты классов CanJump и CanNotJump внутрь конструктора базового класса Animal

    class Dog extends Animal {

        constructor(name,image,canJumpObj) {
            super(canJumpObj);
            ...
        }
    ...

    class Cat extends Animal {

        constructor(name,image,canJumpObj) {
            super(canJumpObj);
            ...
        }
    ...

    class WoodenCat extends Animal {

        constructor(name,image,canJumpObj) {
            super(canJumpObj);
           ...
        }

       ...

Таким образом мы сосредоточили логику прыжков в одном месте, инкапсулируя ее.

Так же мы обеспечили полиморфность объектов классов потомков и теперь можем менять их поведение на лету внутри клиентского кода.

Вот так можно дать возможность прыгать тому, у кого ее не было.

    var catMaket = new WoodenCat('WoodMurka','catwood.png',new CanNotJump());
    catMaket.canJump = new CanJump();
    catMaket.show();

Данный подход (паттерн) носит название Стратегия и звучит так:

Стратегия (англ. Strategy) — поведенческий шаблон проектирования, предназначенный для определения семейства алгоритмов, инкапсуляции каждого из них и обеспечения их взаимозаменяемости. Это позволяет выбирать алгоритм путём определения соответствующего класса. Шаблон Strategy позволяет менять выбранный алгоритм независимо от объектов-клиентов, которые его используют.

## UML диаграмма

![start page]({path-to-subject}/images/1d.png)



