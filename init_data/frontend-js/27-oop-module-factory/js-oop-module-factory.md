# ООП. Паттерны Модуль и Фабрика.
       
Задача.

Создать на странице эмуляцию нескольких банкоматов.

Банкомат будет представлять собой блок с такими полями

- номер карты;

- пин код; 

- сумма пополнения.

Кнопки

- показать баланс;

- пополнить счет.

Шаблон страницы.

    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <style>
        </style>
        <title>Bankomet</title>
      </head>
      <body>
        <h1>Bankomet</h1>
        <div id="root"></div>
        <script src="jquery.min.js" ></script>
        <script src="app.js" ></script>
      </body>
    </html>


UML диаграмма класса банкомата.

![uml]({path-to-subject}/images/1d.png)


Строим начальные классы.

    class Card {
        
        constructor(number,pin,account){
            this.number = number; 
            this.pin = pin;
            this.account = account;
        }
    }
    class Bankomat {
        cards = [];

        constructor(cards){
            this.cards = cards;
        }

        check() {

        }

        replanish() {
            console.log('replanish money');
        }

        show() {
            console.log('show money');
        }

        display() {
            const tpl = `
            <div>
                 <img src="bankomat.png" width="200" />
                 <p>
                    <input id="cnum" type="text" placeholder="Номер карты" />
                 </p>
                 <p>
                    <input id="cpin" type="text" placeholder="ПИН" />
                 </p>
                 <p>
                    <input id="csum" type="text" placeholder="Сумма" />
                 </p>
                 <p>
                    <button id="show-button">Show balance</button>
                    <button id="repl-button">Add money</button>
                 </p>
            </div>
            `
            $("#root").append(tpl);
            $('#show-button').on('click',()=> {this.show()});
            $('#repl-button').on('click',()=> {this.replanish()});        
        }
    }

    var bankomat = new Bankomat();
    bankomat.display();

![factory]({path-to-subject}/images/2.png)


Генерируем набор карт и перерисовываем input в select с выбором карты.

    class Bankomat {
        cards = [];

    ...

    display() {
        const tpl = `
        <div>
             <img src="bankomat.png" width="200" />
             <p>
                <select>
                    ${this.cards.map((el) => `<option>${el.number}</option>`)}
                </select>

    ....

    const card1 = new Card('123123','1',0);
    const card2 = new Card('223123','2',1);
    const card3 = new Card('323123','3',2);
    const bankomat = new Bankomat([card1,card2,card3]);
    bankomat.display();

Данный подход неудобен тем, что в клиентском коде мы вынуждены заботиться о процессе создания карт.

Логичней эту продцедуру делегировать банкомату в виде фабричного метода.

Везде, где вы встретите слова Фабрика, Фабричный метод, Абстрактная фабрика - имеется в виду логика создания новых объектов. Иногда она включает условные выражения. Например если мы в одном банкомате генерируем одни тыпы карт (Mastercard) а в другом - другие. Тогда в эти фабрики и закладываются подобные условия.


### Создаем фабричный метод.

    class Bankomat {
        cards = [];

        constructor(){
            this.cardFabrik();
        }

        cardFabrik(){
            const card1 = new Card('123123','1',0);
            const card2 = new Card('223123','2',1);
            const card3 = new Card('323123','3',2);
            this.cards = [card1,card2,card3];
        }

    ...
    
При этом значительно упрощается клиентский код.

    var bankomat = new Bankomat();
    bankomat.display();

Наполним функцию проверки пин кода.

    class Bankomat {
        ....

        check(cardNumber,pin) {
            let isCorrect = false;
            this.cards.forEach((el) => {
                if(cardNumber === el.number){  
                    if(el.pin === pin) {
                        isCorrect = true;
                    }
                }
            })
            return isCorrect;
        }

Вызовем ее при пополнении баланса.

    replanish() {
        const pin = $('#cpin').val();
        const cardNumber = $('#cnum').val();
        if(!this.check(cardNumber,pin)) {
            alert('Wrong PIN!');
        } else {
            console.log('replanish money');
        }
        
    }

![factory]({path-to-subject}/images/3.png)

Тут возникает следующая проблема.

Из клиентского кода можно поменять пин код и "взламать" карту.

    bankomat.cards[0].pin = 'fake';

Равно как и ее номер!

![factory]({path-to-subject}/images/4.png)

Что делает наш код класса карты уязвимым и не безопастным для недобросовестных программистов.

Поэтому необходимо защитить данные карты и сделать их приватными.

К великому сожалению в ES6 нет такой поддержки.

Но мы можем воспользоваться скрытой переменной в конструкторе и возвращать ее отдельной функцией.

    class Card {
        
        constructor(number,pin,account){
            ...
            var _pin = pin;
            this.getPin = function() { return _pin };
        }
    }

При проверке явно вызываем функцию getPin.

    check(cardNumber,pin) {
        let isCorrect = false;
        this.cards.forEach((el) => {
            if(cardNumber === el.number){
                if(el.getPin() === pin) {
                    isCorrect = true;
                }
            }
        })
        return isCorrect;
    }


Пробуем поменять пин и убеждаемся в невозможности.

    bankomat.cards[0]._pin = 'fake';

Если бы мы использовали ES5 и писали на функциях, то того же результата можно было достичь, возвратив объект из внешней функции. А в этот объект положить методы, возвращающие приватные (защищенные) данные. 

Таким образом pin был бы зашит в замыкание с локальной областью видимости. 


    let card = (function(){
        let pin = 123;
         
        return {
            getPin: function(){
                return pin;
            }
        }
    })();

    card.getPin(); 


Этот прием называется Модуль.

