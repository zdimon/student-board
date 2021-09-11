# Фронтенд. Чат-викторина. JQuery

## Установка готового шаблона.

    git clone git@github.com:zdimon/marafon-js-quiz-template.git

Скопируем его в папку public проекта.

## Сервер разработки.

Поставим простенький сервер.

    npm install lite-server

Запуск.

    cd public
    ../node_modules/lite-server/bin/lite-server 

Работать будем внутри файла app.js.

## Пишем плагин.

Нам вначале необходимо создать изолированную область видимости переменных.

    (function( $ ) {
        $.fn.quizPlugin = function() {
        
            console.log('my plugin');

        };
    })(jQuery);

В jQuery fn - это псевдоним прототипа.

Ключевое слово jQuery (или $) - это всего лишь функция-конструктор, и все объекты, создаваемые этим конструктором будут наследовать все свойства и методы его прототипа.

    $.fn.quizPlugin = function() {..}

Так мы создаём новое свойство-функцию для объекта jQuery, где именем нового свойства будет имя нашего плагина.

Для того, чтобы небыло конфликтов со знаком $ рекомендуется «обернуть» объект jQuery в непосредственно выполняемую функцию-выражение.

Применяем плагин.

    <script>
          var app = $('#myapp').quizPlugin();
    </script>

## Проверяем залогиненность.

        app.start = function() {

            if(sessionStorage.getItem('username')) { 
                this.initRoom();
            } else {
                this.loginForm()
            }
        }

        app.loginForm = function() {

        }

        app.initRoom = function() {

        }

Тут мы предполагаем, что в случае авторизованного пользователя у нас будет существовать переменная username в локальном хранилище браузера.

### Функция вывода формы логина с запросом и вставкой стикеров.

        app.loginForm = function() {
            let form = $('#loginForm').show();
            let url = 'http://quizapi.webmonstr.com/v1/quiz/sticker/list';
            $.get( url, function( data ) {
                data.forEach((el) => {
                    let img_tag = `<img width="50" src="${el.get_url}" />`;
                    let parent = $('#stickers').append(img_tag);
                 })
              });
        }

**$.get** - функция jQuery отсылающая http запрос.

**data.forEach((el) => {})** - функция, перебирающая список.

**$('#stickers').append()** - добавление html в выбранный элемент.

### Привязываем колбек к клику на стикер, убирая класс активности.


     let img_tag = `<img data-id="${el.id}" class="sticker" width="50" src="${el.get_url}" />`;
    ...
     $('.sticker').on('click',(event)=>{
         $('.sticker').each((indx,el)=>{
             $(el).removeClass('active-sticker');
         })
         $(event.target).addClass('active-sticker');
     })

![start page]({path-to-subject}/images/2.png)

**$('.sticker').on('click',(event)=>{})** - привязка событий к коллбеку в jQuery.

Тут мы набрасывае класс sticker на элемент img чтобы далее по ним пройтись циклом и убрать класс active-sticker. Далее мы устанавливаем класс active-sticker на том изображении, на которое кликнул пользователь.

### Стилизируем класс.

    .active-sticker {
        border: 1px solid red;
    }


### Сабмитим форму логина.


Создадим функцию отправки данных методом post с передачей json в теле запроса.


        app.submitLogin = function() {
            let data = {
                name: $('#userName').val(),
                sticker_id: this.sticker
            };
            let url = 'http://quizapi.webmonstr.com/v1/quiz/player/join';
            $.post( url, data, ( response ) => {
                sessionStorage.setItem('username',response.name);
                let form = $('#loginForm').hide();
            });
        }

**$('#userName').val()** - получение данных, вводимых пользователем в элемент input.

**$.post( url, data, ( response ) => {})** - передача данных POST в jQuery.

Привяжем функцию к нажатию кнопки с id = "chat-start".

        app.loginForm = function() {
            ...
              $('#chat-start').on('click',() => {this.submitLogin()});
        }


### Получение и отображение текущего вопроса.

        app.getCurrentQuestion = function() {
            let url = 'http://quizapi.webmonstr.com/v1/quiz/get_current_question';
            $.get( url, ( response ) => {
                $('#currentQuestionBlock').html(response.question);
            });

        }

**$('...').html(content)** - забрасываение html внутрь полученного элемента.


### Отображение списка ответов.

        app.getMessages = function() {
            let url = 'http://quizapi.webmonstr.com/v1/quiz/message/list';
            $.get( url, ( response ) => {
                response.forEach((el)=> {
                    let tpl = `                                             <div class="chat">
                    <div class="chat-user">
                       <a class="avatar m-0">
                       <img src="${el.playerimage}" alt="avatar" class="avatar-35 ">
                       </a>
                       <span class="chat-time mt-1">${el.playername}</span>
                    </div>
                    <div class="chat-detail">
                       <div class="chat-message">
                          <p>${el.text}</p>
                       </div>
                    </div>
                 </div>`;
                 $('#chatContent').append(tpl);
                })
            });
        };


## Веб-сокет соединение.


        ... 

        app.socketConnection = function() {
            let webSocket = new WebSocket('ws://quizapi.webmonstr.com:7777/quiz/');
    
            webSocket.onerror = (evt) => {
                
            }
    
            webSocket.onmessage = (event) => {
                var payload = JSON.parse(event.data)
                console.log(payload);
            }
    
            webSocket.onclose =  (event) => {
                console.log('Close connection');
            };
    
            webSocket.onopen =  (event) => {
                console.log('Connection established');
            };
        }


При создании объекта соединения нам необходимо определить несколько обработчиков.

**onerror** - при ошибке

**onmessage** - приход нового сообщения

**onopen, onclose** - открытие и закрытие соединения.

### Отправка ответа на сервер.

        app.sendMessage = function() {
            let data = {
                message: $('#messageBox').val(),
                playername: sessionStorage.getItem('username')
            }
            let url = 'http://quizapi.webmonstr.com/v1/quiz/save_message';
            $.post( url, data, ( response ) => {
                $('#messageBox').val('');
            });
        };

**$('#messageBox').val('')** - очищение input-а.

### Реагируем на приход сообщения по веб-сокету.

        ....

        webSocket.onmessage = (event) => {
            var payload = JSON.parse(event.data)
            if(payload.type === 'message'){
                this.getMessages();
            }
        }

        ...

### Отображаем список игроков.

        ...
        app.getUserList = function() {
            $('#playerListBlock').empty();
            let url = 'http://quizapi.webmonstr.com/v1/quiz/player/list';
            $.get( url, ( response ) => {
                response.forEach((el) => {
                    let tpl = `<div class="media-height p-3">
                    <div class="media align-items-center mb-4">
                       <div class="iq-profile-avatar status-online">
                          <img class="rounded-circle avatar-50" src="${el.sticker.get_url}" alt="">
                       </div>
                       <div class="media-body ml-3">
                          <h6 class="mb-0"><a href="#">${el.name}</a></h6>
                          <p class="mb-0">${el.account}</p>
                       </div>
                    </div>
                 </div>`;
                    $('#playerListBlock').append(tpl);
                });
            });
        };


### Полная версия инициализации комнаты.

        app.initRoom = function() {
            this.setCurrentUser();
            this.getUserList();
            this.getCurrentQuestion();
            this.getMessages();
            this.socketConnection();
            $('#sendButton').on('click',()=>{
                this.sendMessage();
            });
        }

