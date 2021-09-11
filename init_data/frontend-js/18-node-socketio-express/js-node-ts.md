# NodeJs и Typescript.
    
Установим typescript

    npm install typescript --save

Установим типы для nodejs 

    npm install @types/node --save


Создаем конфигурацию в tsconfig.json

    {
        "compilerOptions": {
            "module": "commonjs",
            "target": "ES5",
            "outDir": "dist",
            "rootDir": "src"
        },
        "exclude": [
            "node_modules"
        ]
    }

Создаем папки client и server в src.

Создадим простейший класс.

    export class Server {
        run() {
            console.log('Hello World!');
        }
    }

Запустим компиляцию.


    ./node_modules/.bin/tsc --watch

Установим универсальный загрузчик модулей.

    npm install systemjs@0.19.22 --save

Создаем страницу index.html.

    <!DOCTYPE html>
    <html>
        <head><title>TypeScript Greeter</title>
            <script src="node_modules/systemjs/dist/system.js"></script>
        </head>
        <body>
            <script>
                SystemJS.config({
                    defaultJSExtensions: true
                });
                SystemJS.import('built/index.js');        
            </script>
        </body>
    </html>

Установим библиотеку express для серверной части.

    npm install express --save

Сделаем простейший сервер src/server/index.ts.

    // creating nodeJS server app
    var express = require('express');
    const app = require('express')();
    

    // serving static files
    app.use(express.static('.'));


    // event loop
    server.listen(5000, () => {
        console.log('Listening 5000');
    });

Установим nodemon 

    npm install --save nodemon

Запуск

    node_modules/nodemon/bin/nodemon.js dist/server/index.js

Попробуем соединиться по вебсокету.

Ставим либу.

    npm install socket.io --save

Типы для socket.io

    npm install @types/socket.io --save

Настроим загрузчик.

        <script>
            SystemJS.config({
                defaultJSExtensions: true,
                map: {
                    'socket.io': 'node_modules/socket.io-client/dist'
                },
                packages: {
                    'socket.io': {
                        main: './socket.io.js'
                    }
                }
            },
           );
            SystemJS.import('dist/client/index.js');        
        </script>

Изменим класс клиента.

    import * as io from 'socket.io';

    export class Game {
        connect() {
            const socket = io('ws://localhost:5000', {transports:['websocket']});
        }
    }

    var game = new Game()
    game.connect();

Видим ошибку соединения
        
    index.js:83 WebSocket connection to 'ws://localhost:5000/socket.io/?EIO=3&transport=websocket' failed: Error in connection establishment: net::ERR_CONNECTION_REFUSED

Добавляем сокет сервер на сервере.

    const server = require('http').createServer(app);

    // adding socket listener
    const io = require('socket.io')(server, {});

Делаем класс игры на сервере в core/main.ts

    import { Socket } from 'socket.io';
    export class ServerGame {
        io: Socket;
        constructor(io: Socket) {
            this.io = io;
            this.io.on('connection',() => {
                console.log('connected!');
            })
        }
    }

Импортируем и создаем объект в server/index.ts.

    import { ServerGame } from './../core/main';
    var game = new ServerGame(io);





