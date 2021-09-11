# NodeJS начало. Использование express и web-socket-ов для обмена клиент-сервер.
       
Ставим реакт.
    
    npm install react react-dom --save

Ставим express.

    npm install express --save

Ставим typescript.

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

Запуск билдера.

    node ./node_modules/typescript/bin/tsc --watch

Установим nodemon 

    npm install --save nodemon

Настроим его конфигурацию в nodemon.json

    {
        "verbose": false,
        "ignore": ["node_modules"],
        "watch": ["src/*"],
        "ext": "*"
    }

Необходимо отслеживать исходный код в src, а не откомпилированный в dist!

Создадим простой сервер.

    var express = require('express');
    const app = require('express')();
    const server = require('http').createServer(app);
    app.use(express.static('.'));

    server.listen(5000, () => {
        console.log('Listening 5000');
    });

Запуск

    node_modules/nodemon/bin/nodemon.js dist/server/index.js

Простой шаблон страницы.

    <!DOCTYPE html>
    <html>
        <head><title>TypeScript Greeter</title>
            <script src="node_modules/systemjs/dist/system.js"></script>
        </head>
        <body>
           <h1>Hello from Node!</h1>
        </body>
    </html>

Установим универсальный загрузчик модулей.

    npm install systemjs@0.19.22 --save

## Фронтенд приложение.

Создаем файл client/index.ts

    console.log('Start!!!')

Добавим скрипт загрузки.

        <script>
            SystemJS.config({
                defaultJSExtensions: true
            });
            SystemJS.import('dist/client/index.js');        
        </script>


## Сделаем обновление страницы после запуска сервера.

Ставим либу socket.io.

    npm install socket.io @types/socket.io --save

Подключим ее на клиенте и попытаемся создать подключение.

Создаем новый файл в client/includes/SocketConnection.ts

    import { Client } from 'socket.io';
    import * as io from 'socket.io';
    export class SocketConnection {
        socket: any; 
        constructor(url: string) {
            this.socket = io(url, {transports:['websocket']});
        }
    }

## Пример отработки соединения и посыл сообщения на сервер.


    this.socket = io(url, {transports:['websocket']})
    .on('connect', (connection) => {
        this.socket.emit('hello',{message: 'hello message'});
    })
        


Подключаем и используем в client/index.ts

    import { SocketConnection } from './includes/SocketConnection';
    var socket = new SocketConnection('ws://localhost:5000')
    console.log('Start!!!')

![start page]({path-to-subject}/images/2.png)

Добавляем пути в загрузчик.

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
            });
            SystemJS.import('dist/client/index.js');        
        </script>

[ссылка на документацию по клиенту](https://socket.io/docs/client-api/)


Добавляем сокет сервер на сервере .

    const server = require('http').createServer(app);

    // adding socket listener
    const io = require('socket.io')(server, {});

Создаем класс сокет соединения на сервере server/includes/SocketServer.ts

    export class SocketServer {
        constructor(io: any) {
            io.on('connection', socket => { 
                console.log('Connected');
                console.log(socket.id);
             });
        }
    }

Создаем объект класса SocketServer в входном файле сервера server/index.ts.

    // adding socket listener
    const io = require('socket.io')(server, {});
    var socketServer = new SocketServer(io);

## Добавление шаблонизатора swig

    npm install swig --save

Доработаем входной файл сервера.

    app.set('views', __dirname + '/../../src/server/tpl');
    app.engine('html', require('swig').renderFile);
    app.use("/", function(request, response){
        response.render("index.html");  
    });

Перенесем шаблон index.html в src/server/tpl.

## Перегрузка страницы в браузере.

Установим библиотеку.

    npm install livereload --save

Добавим следующее в  server/index.ts.

    // livereload  
    const livereload = require("livereload");
    const liveReloadServer = livereload.createServer();
    liveReloadServer.watch(__dirname, '/../../src');   
    liveReloadServer.server.once("connection", () => {
        setTimeout(() => {
          liveReloadServer.refresh("/");
        }, 1000);
      });    
    const connectLivereload = require("connect-livereload");
    app.use(connectLivereload());  

app.use(connectLivereload()) - автоматически добавит тег скрипта на все страницы.

** Необходимо следить за позицией кода и размещать перед подключение шаблонизатора **

Иногда сервер livereload не завершается и оставляет открытым порт 35729.

Поэтому перед стартом сервера можно принудительно прибивать процесс на порту 35729.

    kill -9 $(lsof -t -i:35729)

## Объеденим сервер NodeJs и транспилятор Typescript.

(ссылка на библиотеку)https://www.npmjs.com/package/concurrently

    npm install concurrently --save

Запустим 2 команды, пропишем команду start в package.json


  "scripts": {
    ...
    "start": "concurrently \"./bin/run.cmd\" \"./bin/build.cmd\""
  },


