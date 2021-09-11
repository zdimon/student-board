# Серверная часть на NodeJs.
    
Устанавливаем необходимые библиотеки.

    npm install express --save
    npm install socket.io --save
    npm install rx --save
    npm install jquery --save

Делаем простейший сервер server.js.

    var express = require('express');
    const app = require('express')();
    const server = require('http').createServer(app);
    app.use(express.static('.'));

    server.listen(5000, () => {
        console.log('Listening 5000');
    });

Шаблон index.html.


    <!DOCTYPE html>
    <html>
        <head><title>Test</title>
            <script src="node_modules/jquery/dist/jquery.min.js"></script>
        </head>
        <body>
            <h1>Test</h1>
        </body>
    </html>

Запуск сервера.

    node server.js

Обслужим кастомный url.

    app.get('/test', (req, res) => {
        res.send('Hello World!')
    })

Проверяем на адресе http://localhost:5000/test

Прикрутим веб-сокет сервер. 

    const server = require('http').createServer(app);
    const io = require('socket.io')(server, {});

Опишем событие подключения.

    io.on('connection', socket => { 
        console.log('Connected');
        console.log(socket.id);
     });

Подключимся с фронтенда.

    <script src="node_modules/socket.io-client/dist/socket.io.js"></script>

    ...

       const socket = io('ws://localhost:5000', {transports:['websocket']});  
       socket.on('connect', () => {
            console.log(socket);
       });

Создадим приложение в файле app/main.js.

    app = {blocks: []}

    app.init = function(io) {
        this.io = io;
        for(let i of [1,2,3]){
            app.blocks.push(i);
        }
    }

    module.exports = app;

Использование.

    const myapp = require('./app/main');
    myapp.init(io);
    console.log(myapp);

Переодические сообщения всем клиентам.

    ...
    var Rx = require('rx');
    ...
    app.init = function(io) {
        ...
        this.ping();
    }

    app.ping = function() {
        Rx.Observable.interval(1000).subscribe((evt) => {
            this.io.send({data: evt});
        })
    }

Создаем статические блоки со случайными координатами.

    app.createMap = function(){
        this.blocks = [];
        for(let i of [1,2,3,4,5,6,7]) {
            let b = {
                x: parseInt(Math.random() * 300),
                y: parseInt(Math.random() * 300),
                size: 10
            }
            app.blocks.push(b);
        }
    }

Отправляем их с частотой fps.

    app.ping = function() {
        Rx.Observable.interval(1000).subscribe((evt) => {
            this.io.send({data: this.blocks});
        })
    }

Отрисуем блоки на холсте.

     <canvas id="canvas" width="300" height="300" style="border: 1px solid red;"></canvas>

            <script>
               const socket = io('ws://localhost:5000', {transports:['websocket']});  
               socket.on('connect', () => {
                    socket.on('message', msg => {                  
                        draw(msg.data);
                    })
               });

             
               var canvas = $("#canvas")[0];
               var ctx = canvas.getContext("2d");

               function draw(stars){
                    ctx.fillStyle = '#000000';
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    ctx.fillStyle = '#ffffff';
                    stars.forEach(function(star) {
                        ctx.fillRect(star.x, star.y, star.size, star.size);
                    });
               }
            </script>


Принимаем сообщение от клиента.

Вынесем инициализацию веб-сокет соединения в main.js и определим колбек для события поступления сообщения.

    app.init = function(io) {
        ...
        io.on('connection', socket => { 
            console.log('Connected');
            socket.on('message', data => {
                if(data.data === 'refresh') {
                    this.createMap();
                }
            });
            
         });
    }

Добавим кнопку на фронтенд и функцию отправки сообщения.

    <button id="button">Refresh</button>
    ...
       $('#button').on('click',() => {
           socket.emit('message',{data: 'refresh'});
       });

Нарисуем персонаж.

        base_image = new Image();
        base_image.src = 'static/tank.png';
        base_image.onload = function(){
            ctx.drawImage(base_image, 0, 0);
        }

Создадим на сервере столько персонажей, сколько соединений.


    app.createTank = function(sid){
        let t = {
            x: parseInt(Math.random() * 300),
            y: parseInt(Math.random() * 300),
            sid: sid
        }
        this.tanks.push(t);
    }


Отрабатываем дисконнект и удаляем персонаж.

    io.on('connection', socket => { 
        ...
        socket.on('disconnect', () => { 
            console.log('disconnection');
            this.deleteTank(socket.id);
        })

    ...

    app.deleteTank = function(sid){
        console.log(`deleting ${sid}`);
        for(let t in this.tanks){
            if(this.tanks[t].sid === sid){
                this.tanks = this.tanks.splice(t-1,1);
            }
        }
    }

Отреагируем на нажатие стрелок на клиенте.

    var keydown = Rx.Observable.fromEvent(document, 'keydown')
    .sample(1000);
    keydown.subscribe((evt) => {

        if(evt.key === 'ArrowLeft') {
             socket.emit('message',{data: 'move_left'});
        }
        if(evt.key === 'ArrowRight') {
         socket.emit('message',{data: 'move_right'});
        }       
        if(evt.key === 'ArrowUp') {
         socket.emit('message',{data: 'move_forward'});
        }  
        if(evt.key === 'ArrowDown') {
         socket.emit('message',{data: 'move_back'});
        }   
        
    })

Мы выставили задержку в 1 сек для уменьшения частоты событий.

Создадим файл с утилитами и в ней функцию, поворачивающую танк установкой переменной от 1 до 8 что означает 8 вариантов поворота.

    utils = {
        rotateTank: function(tank,direction){
            if(direction === 'right') {
                if (tank.angle === 8 ) {
                    return 1
                } else {
                    return tank.angle + 1;
                }
            }
            if(direction === 'left') {
                if (tank.angle === 1 ) {
                    return 8
                } else {
                    return tank.angle - 1;
                }
            }
        }
    }

Вызовем ее в обработчике.

            socket.on('message', data => {
            ...
                if(data.data === 'move_left') {
                    let tank = this.findTank(socket.id);
                    tank.angle = utils.rotateTank(tank,'left');
                }
                if(data.data === 'move_right') {
                    let tank = this.findTank(socket.id);
                    tank.angle = utils.rotateTank(tank,'right');
                }

Отрисуем на клиенте повернутый танк.

     data.tanks.forEach(function(tank) {
        drawTank(tank_image,tank.x, tank.y, 1, getRadians(tank.angle));
     });
    ...
    function drawTank(image, x, y, scale, rotation){
        ctx.setTransform(scale, 0, 0, scale, x, y); // sets scale and origin
        ctx.rotate(rotation);
        ctx.drawImage(image, -image.width / 2, -image.height / 2);
        ctx.setTransform(1,0,0,1,0,0);
    } 

    function getRadians(angle){
        switch(angle) {
            case 1:
                var n = 0;
                break;
            case 2:
                var n = 45;
                break;         
            case 3:
                var n = 90;
                break;
            case 4:
                var n = 135;
                break;
            case 5:
                var n = 180;
                break;         
            case 6:
                var n = 225;
                break;
            case 7:
                var n = 270;
                break;
            case 8:
                var n = 315;
                break;
            
        }
        return n * Math.PI / 180;
    }

Определим событие для стрельбы и сделаем поток с посылкой на сервер сообщения.

    var shotStream$ = Rx.Observable.fromEvent(document, 'keydown')
    .filter((evt) => evt.keyCode == 32 )
    .sample(1000).subscribe(evt => {
        socket.emit('message',{data: 'shot'});
    });

Отработаем на сервере.

            app = {
                    ...
                    shots: []
                  }

            ...
            if(data.data === 'shot') {
                let tank = this.findTank(socket.id);
                this.shots.push(
                    {
                        tank: socket.id,
                        x: tank.x,
                        y: tank.y
                    }
                );
                console.log(this.shots);
            }

Добавляем в утилиты перемещение пульки.

        moveShots: function(shots) {
            shots.forEach((el,index) => {
                
                switch(el.angle){
                    case 1:
                        el.y = el.y-3;
                        break;
                    case 2:
                        el.y = el.y - 3;
                        el.x = el.x + 3;
                        break;
                    case 3:
                        el.x = el.x + 3;
                        break;
                    case 4:
                        el.y = el.y + 3;
                        el.x = el.x + 3;
                        break;
                    case 5:
                        el.y = el.y + 3;
                        break;
                    case 6:
                        el.x = el.x - 3;
                        el.y = el.y + 3;
                        break;
                    case 7:
                        el.x = el.x - 3;
                        break;
                    case 8:
                        el.x = el.x - 3;
                        el.y = el.y - 3;
                        break;
                }            
            });
        }

Вызовем функцию.

    app.ping = function() {
        Rx.Observable.interval(100).subscribe((evt) => {
            utils.moveShots(this.shots)
    ...


Убираем пульку по достижению конца экрана.

        shots.forEach((el,index) => {
            if (el.y > 300 || el.x > 300 || el.y < 0 || el.x < 0) {
                shots.splice(index,1);
            }
        ...

[полезная ссылка](https://stackoverflow.com/questions/17411991/html5-canvas-rotate-image)


