# Аркадная игра.

![start page]({path-to-subject}/images/1.png)

[ссылка на репозиторий](https://github.com/zdimon/simple-arcade)

## Передвижение объекта по горизонтали.
  
Задача: перемещать внутренний блок относительного внешнего по горизонтали бесконечно взад-вперед.

## Решение.

Определим 2 блока на странице.

    <div class="out">
      <div class="in" id="ball">
        
      </div>
    </div>

Стили.

    .out {
        width: 200px;
        height: 200px;
        position: relative;
        border: 1px solid silver;
    }

    .in {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        background-color: red;
        position: absolute;
    }

Определим бесконечный таймер.

    var timerFunc = function() {
        console.log($.now());
        id = setTimeout(timerFunc, 1000);
    }

    var id = setTimeout(timerFunc, 1000);


Определим объект шарика с элементом и направление движения.

    $( document ).ready(() => {


        var ball = {
            el: $('#ball'),
            move: 'right'
        };

        var timerFunc = function() {
            id = setTimeout(timerFunc, 1000);
            ball.el.css({'left' : parseInt(ball.el.position().left+5) + 'px'});
        }

        var id = setTimeout(timerFunc, 1000);

        }
    );

Отработаем два направления движения.

    var timerFunc = function() {
        id = setTimeout(timerFunc, 100);
        if(ball.move === 'right') {
            var newCoord =  parseInt(ball.el.position().left+5);
        } else {
            var newCoord =  parseInt(ball.el.position().left-5);
        }
        ball.el.css({'left' : newCoord + 'px'});

        if (newCoord>200) {
            ball.move = 'left';
        } 

        if (newCoord<0) {
            ball.move = 'right'
        }
    }

Проблема возникнет когда у нас будет много объектов, при таком подходе мы будем вынуждены для каждого устанавливать свой таймер и когда их станет много это будет очень неудобно.

Поэтому логичней определить специальную функцию - жизненный цикл, которую запустить с интервалом и в ней передвигать все объекты на странице.


    $( document ).ready(() => {

        var ball2 = {
            el: $('#ball2'),
            move: 'right'
        };


        function gameLoop()
        {
            console.log(parseInt($.now()));
            setTimeout(gameLoop,100);
        }

        gameLoop();
    }

    );

Создадим для игры один единственный блок.

    <div class="out" id="gameApp"> </div>

Далее создадим 3 функции:

clear - для очистки игрового поля

draw - для прорисовки всех элементов

calc - для пересчета координат элементов

И вызовем их в жизненном цикле событий.

    function clear() {

    }

    function calc() {
        
    }

    function draw() {
        
    }

    function gameLoop()
    {
        // change position based on speed
        //moveSelection();
        console.log(parseInt($.now()));
        calc();
        clear();
        draw();
        setTimeout(gameLoop,100);
    }

Далее закинем все объекты игры в один объект.

    var gameApp = {
        balls: [
            {x: 0, y: 30},
            {x: 30, y: 100},
        ]
    }

Опишем функцию очистки.

    function clear() {
        $("#game").clear();
    }

Функция прорисовки.

    function draw() {
        for (let ball of gameApp.balls) {
            $('#gameApp').append(`<div class="ball" style="top:${ball.y}px; left:${ball.x}px">`);
        }
    }

Функция пересчета координат объектов.

    function calc() {
        for (let ball of gameApp.balls) {
            if(ball.x>170) ball.move = 'left';
            if (ball.x<30) ball.move = 'right';

            if(ball.move === 'left') ball.x = ball.x - 4;
            if(ball.move === 'right') ball.x = ball.x + 4;
        }        
    }


Двигаем объект пушки по нажатию стрелок.

Добавим стили для пушки.

    .canon {
        height: 25px;
        width: 5px;
        background-color: black;
        position: absolute;
    }

Добавим координату пушки и статус нажатия клавиш стрелок в объект игры.


    var gameApp = {
        balls: [
            {x: 0, y: 30, move: 'right'},
            {x: 70, y: 100, move: 'left'},
        ],
        cannon_x: 100,
        key_left: 'up',
        key_right: 'up'
    }

Добавим в прорисовку.

    function draw() {
        for (let ball of gameApp.balls) {
            $('#gameApp').append(`<div class="ball" style="top:${ball.y}px; left:${ball.x}px">`);
        }
        $('#gameApp').append(`<div class="canon" style="top:170px; left:${gameApp.cannon_x}px">`);
    }


Отслеживаем нажатие кнопок стрелок.

    $(document).on('keyup', function( e ) {
        
        if(e.keyCode === 39) gameApp.key_right = 'up'
        if(e.keyCode === 37) gameApp.key_left = 'up'

    })

    $(document).on('keydown', function( e ) {
        
        if(e.keyCode === 39) gameApp.key_right = 'down'
        if(e.keyCode === 37) gameApp.key_left = 'down'
        
    })

Добавляем пересчет координат пушки.

    function calc() {
        for (let ball of gameApp.balls) {
            if(ball.x>170) ball.move = 'left';
            if (ball.x<0) ball.move = 'right';

            if(ball.move === 'left') ball.x = ball.x - 4;
            if(ball.move === 'right') ball.x = ball.x + 4;
            
        }      
        if(gameApp.key_left === 'down') gameApp.cannon_x = gameApp.cannon_x - 4;
        if(gameApp.key_right === 'down') gameApp.cannon_x = gameApp.cannon_x + 4;
        
    }

Делаем ограничение движения пушки по размерам экрана.


        if(gameApp.key_left === 'down') (gameApp.cannon_x>0)? gameApp.cannon_x = gameApp.cannon_x - 4: gameApp.cannon_x = 0;
        if(gameApp.key_right === 'down') (gameApp.cannon_x<190)? gameApp.cannon_x = gameApp.cannon_x + 4: gameApp.cannon_x=190;

Добавим пульки в объект игры.

    var gameApp = {
        ....
        bullets: []
    }

Отработаем нажатие на пробел.


    $(document).on('keydown', (e) => {
        ...
        if(e.keyCode === 32) {
            gameApp.bullets.push({x: gameApp.canon_x, y: 185})
        }
       ...
    })

Изменяем координаты пуль и убираем их из массива при выходе за пределы игрового поля.

        for (let bullet of gameApp.bullets){

            bullet.y -= 2;
            if(bullet.y<0) gameApp.bullets.splice(gameApp.bullets.indexOf(bullet),1);

           }

## Пример определения коллизии.

    var rect1 = {x: 5, y: 5, width: 50, height: 50}
    var rect2 = {x: 20, y: 10, width: 10, height: 10}

    if (rect1.x < rect2.x + rect2.width &&
       rect1.x + rect1.width > rect2.x &&
       rect1.y < rect2.y + rect2.height &&
       rect1.y + rect1.height > rect2.y) {
        // collision detected!
    }






