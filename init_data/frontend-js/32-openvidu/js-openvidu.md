# Передача видео аудио потока с Openvidu.
      
Библиотека Openvidu предоставляет набор инструментов для обеспечения передачи видео и аудиопотока между браузерами, шаринга рабочего стола, их записи на стороне сервера, а также обслуживания IP камер.

Процесс постороен на технологии WebRTC.

Эта технология достаточно сложная и включает передачу информации о сетевых и видео настройках между двумя точками по веб-сокетам.

Эта информация передается в виде SDP (описание кодеков, частоты кадров и пр.) и ICE кандидатов (сетевая конфигурация).


Openvidu нам позволяет не вникать в тонкости этого взаимодействия коих достаточно много, т.к. в разных сетях соединить два браузера бывает ой как не просто.

Сама  библиотека включает несколько процессов-серверов.

**KMS** - бесплатный Karentoo медиа сервер, который обрабатывает видео и пропускает его через себя кодируя и записывая (опционально), затем он может его передать и браузер будет думать что он работает с другим браузером но на самом деле будет отдавать и принимать поток из медиа-сервера. Портты 40000 - 57000 TCP+UDP

**Coturn** - TURN сервер для определения IP адресов клиентов и нахождения дырок сети через которые проводить видео. 3478 порт для определения IP и 57001 - 65535 TCP+UDP для построения моста с KMS.

**Openvidu** - сокет сервер c REST API для обмена сообщениями между браузером и KMS. Порт 4443.

**Redis** - база данных

Схема взаимодействия.

![start page]({path-to-subject}/images/2.png)

Имеем 3-х игроков.

**openvidu-browser** JavaScript библиотека для установки соединения.

**openvidu-server** - Java приложение, которое управляет KMS медиа сервером. 

**Kurento Media Server** - низкоуровневый сервер для операций с медиа-потоком и его передачей.

Запуск и установка включает следующие шаги.

Установка docker и docker-compose.

    apt install docker-ce docker-compose

Установка openvidu
    
    cd /opt
    curl https://s3-eu-west-1.amazonaws.com/aws.openvidu.io/install_openvidu_latest.sh | bash

Прописываем настройки  DOMAIN_OR_PUBLIC_IP и OPENVIDU_SECRET в .env.

    DOMAIN_OR_PUBLIC_IP=localhost

Стартуем сервер.

    ./openvidu start

Старт сервера вручную

    docker run -p 4443:4443 --rm -e OPENVIDU_SECRET=MY_SECRET openvidu/openvidu-server-kms:2.18.0

При этом мы открываем 4443 порт прокидывая его из контейнера наружу.

Устанавливаем  пример приложения.

    git clone https://github.com/OpenVidu/openvidu-tutorials.git -b v2.18.0

Заходим в любой пример и запускаем там статический вебсервер. Например.

    python3 -m http.server 8080

## Разработка фронтенд приложения.

Подсоединяем клиента.

    <script src="openvidu-browser-2.18.0.js"></script>

Стартуем сессию.

    OV = new OpenVidu();

OV - объект-точка входа в библиотеку.

Через нее создаем остальные объекты.

## Сессия

    session = OV.initSession();

Представляет собой комнату пользователя, в которую можно добавлять соединения.

Сессия имеет ряд событий.

**streamCreated** - срабатывает когда в сессию добавляется новый поток. В этом событии мы подписываемся на поток и потом мы можем добавлять видеотег в произвольный HTML элемент по ID.

    session.on('streamCreated', event => {
        var subscriber = session.subscribe(event.stream, 'video-container');
    })

**videoElementCreated** - это событие подписчика в котором мы можем что то сделать после того, как добавлен видео тег и пошло видео.


**streamDestroyed** - событие сессии, срабатывает при покидании комнаты и удалении каждого видеопотока.  

**exception** - событие сесии при ошибках выполнения асинхронных операций.

## Соединение

Представляет конкретный видеопоток пользователя который может быть добавлен в сессию.

Сессия имеет уникальный идентификатор как и соединения имеет уникальный токен.

### Создание сессии на сервере.

Для того, чтобы на сервере создать сессию, необходимо послать POST запрос на адрес /openvidu/api/sessions и передать придуманное имя сессии.

    function createSession(sessionId) { 
    // See https://docs.openvidu.io/en/stable/reference-docs/REST-API/#post-openviduapisessions
            return new Promise((resolve, reject) => {
                $.ajax({
                    type: "POST",
                    url: this.OPENVIDU_SERVER_URL + "/openvidu/api/sessions",
                    data: JSON.stringify({ customSessionId: sessionId }),
                    headers: {
                        "Authorization": "Basic " + btoa("OPENVIDUAPP:" + this.OPENVIDU_SERVER_SECRET),
                        "Content-Type": "application/json"
                    },
                    success: (response) => { 
                        return resolve(response.id)
                    },
                    error: (error) => {
                       
                        if (error.status === 409) {
                            resolve(sessionId);
                        } else {
                            console.warn('Error');
                            }
                        }
                    }
                });
            });
        },

При этом запрос может возвратить статус 409 в случае существования сессии с таким именем. При этом ничего страшного не происходит а результат игнорируется и передается дальше по цепочке асинхронных промисов.

### Создание соединения.

POST запрос на /openvidu/api/sessions/' + sessionId + '/connection'

Возвратит токен соединения. 

    function createToken(sessionId) { 
    // See https://docs.openvidu.io/en/stable/reference-docs/REST-API/#post-openviduapisessionsltsession_idgtconnection
            return new Promise((resolve, reject) => {
                $.ajax({
                    type: 'POST',
                    url: this.OPENVIDU_SERVER_URL + '/openvidu/api/sessions/' + sessionId + '/connection',
                    data: JSON.stringify({}),
                    headers: {
                        'Authorization': 'Basic ' + btoa('OPENVIDUAPP:' + this.OPENVIDU_SERVER_SECRET),
                        'Content-Type': 'application/json',
                    },
                    success: (response) => {
                        return resolve(response.token)
                    },
                    error: (error) => reject(error)
                });
            });
        },

Функция, объеденяющая 2 запроса в цепочку.

    function getToken(mySessionId) {
        return createSession(mySessionId).then(sessionId =>     createToken(sessionId));
    }


Т.к. это запросы имеют секреты, их следует выполнять на стороне сервера и не светить в js.

Разметка страницы.

    <!doctype html>
    <html lang="en">
        <head>
            <meta charset="utf-8">
            <title>Openvidu sender</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
            <script src="/static/openvidu.js"></script>
           
        </head>

        <body>
            <h1>Openvidu Sender page</h1>

            <div id="senderCam"></div>

            <a id="start">Start video translation</a>
            

            <script src="/static/ov/index.js"></script>
            <script>
            $('#start').on('click', () => {
                window.myapp.initappSender('woman');
            })
                
                
            </script>

        </body>
    </html>


openvidu.js - браузерная библиотека, можно скопировать из любого из примеров.     


Создаем объект приложения и функцию инициализации для транслирующего видео.

    var ovapp = {
        OPENVIDU_SERVER_URL: 'https//localhost:4443',
        OPENVIDU_SERVER_SECRET: 'MY_SECRET',


        initappSender: function(uname) {
            OV = new OpenVidu();
            session = OV.initSession();
        }

    }

Добавим функции создания сессии и соединения.


    var ovapp = {
        OPENVIDU_SERVER_URL: 'https://localhost:4443',
        OPENVIDU_SERVER_SECRET: 'MY_SECRET',


        initappSender: function(uname) {
            OV = new OpenVidu();
            session = OV.initSession();
            this.getToken('woman').then(
                (token) => {
                    console.log(`we got token ${token}!!!`)
                }
            );
        },


        createSession: function (sessionId) { 
            return new Promise((resolve, reject) => {
                $.ajax({
                    type: "POST",
                    url: this.OPENVIDU_SERVER_URL + "/openvidu/api/sessions",
                    data: JSON.stringify({ customSessionId: sessionId }),
                    headers: {
                        "Authorization": "Basic " + btoa("OPENVIDUAPP:" + this.OPENVIDU_SERVER_SECRET),
                        "Content-Type": "application/json"
                    },
                    success: response => resolve(response.id),
                    error: (error) => {
                        if (error.status === 409) {
                            resolve(sessionId);
                        } else {
                            console.warn('No connection to OpenVidu Server. This may be a certificate error at ' + this.OPENVIDU_SERVER_URL);
                            if (window.confirm('No connection to OpenVidu Server. This may be a certificate error at \"' + this.OPENVIDU_SERVER_URL + '\"\n\nClick OK to navigate and accept it. ' +
                                'If no certificate warning is shown, then check that your OpenVidu Server is up and running at "' + this.OPENVIDU_SERVER_URL + '"')) {
                                location.assign(this.OPENVIDU_SERVER_URL + '/accept-certificate');
                            }
                        }
                    }
                });
            });
        },
        


        createToken: function (sessionId) { 
            return new Promise((resolve, reject) => {
                $.ajax({
                    type: 'POST',
                    url: this.OPENVIDU_SERVER_URL + '/openvidu/api/sessions/' + sessionId + '/connection',
                    data: JSON.stringify({}),
                    headers: {
                        'Authorization': 'Basic ' + btoa('OPENVIDUAPP:' + this.OPENVIDU_SERVER_SECRET),
                        'Content-Type': 'application/json',
                    },
                    success: (response) => resolve(response.token),
                    error: (error) => reject(error)
                });
            });
        },

        getToken: function(mySessionId) {
            return this.createSession(mySessionId).then(sessionId =>     this.createToken(sessionId));
        }

    }


Результат.

![start page]({path-to-subject}/images/3.png)

Создадим сокет-соединение для приема сообщений о запросе на передачу видео.

Установим клиент.

    npm install socket.io-client --save

Скопируем из папки dist и подключим библиотеку на странице.

    <script src="/static/socket.io.min.js"></script>

Создадим соединение с сервером по сокетам.

    var ovapp = {
        ...
        SOCKET_URL: 'http://localhost:5001',

        socketConnect: function(login) {
            socket = io(`${this.SOCKET_URL}`, {transports:['websocket']});
            socket.on('connect', () => {
                console.log('Connection was established');
                window.sessionStorage.setItem('sid',socket.id);
                socket.emit('login',{login});
            })            
        },

При этом мы по событию соединения дополнительно уведомляем сервер о логине человека, который подсоеденился чтобы сервер это зафиксировал в БД и знал кто в онлайне.

        initappSender: function(username) {
            ...
            this.socketConnect(username);
        ...

Отреагируем на сообщение на прием видео от принимающей стороны.

При этом отобразим диалоговое окно с кнопками согласия или отказа, а также с видео тегом.

        socket.on('calling', (msg) => {

            const tpl = `<div id="responseBox">
                <h1 id="callerName">${msg.login} is calling you!<h1>
                <input type="text" id="recieverLogin" value="${msg.login}">
                <video autoplay="true" width="200" id="myVideo"></video>  
                <div style="text-align: center">              
                <a class="btn" id="acceptOffer">Accept</a>
                <a class="btn" id="declineOffer">Decline</a>
                <a class="btn" style="display:none" id="stopVideo">Stop video</a>
                </div>
            </div>`;
            $('#senderCam').html(tpl);
            $('#senderCam').show();
        });

Оформим страницу для принимающей стороне.

    <!doctype html>
    <html lang="en">
        <head>
            <meta charset="utf-8">
            <title>Openvidu reciever</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
            <script src="/static/openvidu.js"></script>
            <script src="/static/socket.io.min.js"></script>
            <link rel="stylesheet" href="/static/video.css">
        </head>
        <body>
            <h1>Openvidu Reciever page</h1>
            <div id="recieverCam"></div>
            <button id="VideoCall" data-username="woman">Video call</button>
            <script src="/static/ov/index.js"></script>
            <script>
                window.ovapp.initappReciever('man');
            </script>
        </body>
    </html>


**window.myapp.initappReciever('man')** - тут мы инициализируем приложение для принимающего и передаем его логин, для дальнейшей передачи его на сторону передающего чтобы вывести его на диалоговом окне вызова.

В кнопку вызова закладывем информацию о логине вызываемого.

Оформим функцию initappReciever.


    var ovapp = {
       ...
        initappReciever: function(username){
            console.log('Init sender app');
            socket = io(`${this.SOCKET_URL}`, {transports:['websocket']});
            
            $('#VideoCall').on('click', (e) => {
                this.callUser();
            })
        },

    ...

Теперь в функции callUser мы должны послать сообщение в браузер передающего.

    callUser: function() {
        const url = `${this.SERVER_URL}/call`;
        const username =  $('#VideoCall').attr( "data-username" );
        $.ajax({
            url: url,
            type: "POST",
            data: JSON.stringify({
                login: username,
                sid: window.sessionStorage.getItem('sid')
            }),
            contentType: "application/json",
            success: (response) => {
                if(response.status === 0) {
                    $('#VideoCall').html(response.message);
                } else {
                    alert(response.message);
                }
                
            }
        }); 
    },

Для этого пошлем HTTP запрос на сервер и он перредаст его через сокет на сторону передающего.

Результат.

![start page]({path-to-subject}/images/4.png)

Отработаем отказ, послав на сервер уведомление по ресту.

       socket.on('calling', (msg) => {

           ...
            $('#senderCam').show();
            $('#declineOffer').on('click', async (e) => {
                const url = `${this.SERVER_URL}/decline`;
                $.ajax({
                    type: "POST",
                    url: url,
                    contentType: "application/json",
                    data: JSON.stringify({
                        'sid': window.sessionStorage.getItem('sid'),
                        'reciever_login': $('#recieverLogin').val()
                    }),
                        success: (data) => {
                            console.log(data);
                            $('#senderCam').html('');
                        },
                });
            }) 
        });

Теперь принятие приглашения.

            $('#acceptOffer').on('click', async (e) => {
                $('#acceptOffer').hide();
                $('#declineOffer').hide();
                $('#stopVideo').show();
                $('#callerName').html('Click here to move');
                
                const url = `${this.SERVER_URL}/status`;
                $.ajax({
                    type: "POST",
                    url: url,
                    contentType: "application/json",
                    data: JSON.stringify({
                        'sid': window.sessionStorage.getItem('sid'),
                        'status':'beasy'
                    }),
                        success: (data) => {

                        },
                });
            });

Где мы скрываем и отображаем соответствующие кнопки и посылаем уведомление на сервер о том что пользователь занят.

Далее нам необходимо отобразить камеру на передающей строне.

    $('#acceptOffer').on('click', async (e) => {
        $('#acceptOffer').hide();
        $('#declineOffer').hide();
        $('#stopVideo').show();
        $('#callerName').html('Click here to move');

        OV = new OpenVidu();
        session = OV.initSession();
        this.getToken(this.USERNAME).then(function(token) {
            session.connect(token, { })
            .then(() => {
                var publisher = OV.initPublisher('video-container', {
                    audioSource: undefined, 
                    videoSource: undefined, 
                    publishAudio: true, 
                    publishVideo: true, 
                    resolution: '640x480', 
                    frameRate: 30,
                    insertMode: 'APPEND',
                    mirror: false
                });
                session.publish(publisher);

            })
        });
        ...

Отобразим ее и на принимающей.




