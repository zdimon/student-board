# Библиотека JQuery.

JSON (JavaScript Object Notation) — текстовый формат
для хранения и передачи данных по сети. JSON — это
представление объектов JavaScript в текстовом
формате.

Для работы с JSON форматом в JavaScript есть объект
JSON. 

Основные функции это серилиазация и десериализации.

## Сериализация.

stringify() сериализует объекты в строку

В сериализованном объекте не должно быть циклических ссылок.

Синтаксис.

JSON.stringify(value [, replacer[, space]])

Replacer — параметр, который позволяет влиять
на сериализацию объекта. Значением параметра может
быть функция, массив или null, если параметр не нужен.

Функция в параметре replace используется, если нам
необходимо определить значения, которые не будут
включаться в сериализацию по определенному условию. 


	function checkAge(key, value) {
	
		 if (key === "age" && value >= 18) {
		 	return undefined;
		 }
		return value;
	 }
 
И третий параметр в функции JSON.stringify(value,
replacer, space) — это space, который принимает строку
или число и позволяет придать более читаемый вид строке
JSON, добавляя отступы.

	alert(JSON.stringify(person, null, 2));

## Десериализация.

Чтобы строку JSON преобразовать в объект, нужно
выполнить над ней метод парсинга. Парсинг, в данном
случае, означает процесс десериализации строки в объект.
Функция parse() — функция, которая десериализирует
JSON строку и возвращает объект JavaScript.

Синтаксис.

	JSON.parse(str, [reviver]) 
	
Также есть еще необязательный параметр reviver,
с ним все практически то же, что и в функции stringify()


## toJSON

Метод toJSON() может быть методом любого объекта.
Он позволяет определить собственное представление
объекта в JSON. 

Таким образом, можно заменить стандартное поведение сериализации на собственное. 
	 
	 
	let model = {
	 name: "BMW",
	 autopilot : undefined,
	 toJSON(){
			 let jsonStr = '{"name": "${this.name}",
			 "autopilot": ';
			 if(this.autopilot === undefined){
			 jsonStr += '"Not"}'
		 }
			 else{
			 jsonStr += '"${this.autopilot}"}'
		 }
		 return jsonStr;
	 }
	}
	
	
## Синхронные и асинхронные запросы	
 
Синхронные запросы — запросы, при отправке
которых нужно дождаться ответа с сервера. 
Например, при авторизации на сайте, пользователю не нужно выполнять другие действия
на странице, и в этом случае можно использовать синхронный запрос.

Асинхронные запросы — запросы, которые позволяют не дожидаться ответа с сервера. Результат запроса
будет обработан в момент, как только ответ будет принят
с сервера. 

Ajax — технология для взаимодействия с сервером
без перезагрузки страницы.

Для использования Ajax в JavaSctript есть специальный объект  XMLHttpRequest. 

Для того чтобы послать запрос, нужно использовать его
методы open() и send(). 

## Объект FormData

FormData — позволяет формировать данные из форм
в пары ключ-значение автоматически.

     let form = document.getElementById("form");
     let formData = new FormData(form)
     formData.append("date", new Date().toLocaleString());
 
Пример низкоуровневой отправки формы.

    let subbliBtn = document.getElementById("submit-btm");
    subbliBtn.onclick = function () {
         let form = document.getElementById("form");
         let formData = new FormData(form)
         formData.append("date", new Date().toLocaleString());
         let request;
         if (window.XMLHttpRequest) {
            request = new XMLHttpRequest();
         }
         else {
            request = new ActiveXObject("Microsoft.XMLHTTP");
         }
         request.open("POST", "server.php");
         request.onreadystatechange = function () {
             if (request.readyState ==
             4 && request.status == 200) {
                 alert("Здравствуйте " + nameValue +
                 "! Мы перезвоним вам через 1 минуту");
             }
        }
         request.setRequestHeader('Content-Type',
         'multipart/form-data');
         request.send(formData);
     }
     
## Методы AJAX в JQuery.

Все они возвращают обертку вокруг объекта XMLHTTPRequest (jqXHR), используя промисы.

### jQuery.ajax()

Низкоуровневый запрос с тонкой конфигурацией.

    $.ajax({
      method: "POST",
      url: "some.php",
      data: { name: "John", location: "Boston" }
    })
      .done(function( msg ) {
        alert( "Data Saved: " + msg );
      });
      
Это позволяет делать запросы синхронно.

    var result = $.ajax({
                    type: "GET",
                    url: remote_url,
                    async: false
                }).responseText
    
    

### Запрос GET

    jQuery.get( url [, data ] [, success ] [, dataType ] )

Загружает данные с сервера используя запрос GET.

data - объект или стока, отправляемая серверу.

success - колбек, принимающий результат.

dataType - тип данных, ожидаемых от сервера.

    $.get( "ajax/test.html", function( data ) {
      $( ".result" ).html( data );
      alert( "Load was performed." );
    });

Т.к. jqXHR использует промисы, это позволяет строить цепочки (конвееры) и выполнять дополнительные действия после запроса.

    var jqxhr = $.get( "example.php", function() {
      alert( "success" );
    })
      .done(function() {
        alert( "second success" );
      })
      .fail(function() {
        alert( "error" );
      })
      .always(function() {
        alert( "finished" );
      });
     
Примеры.

Простой тест страницы с игнорированием результата.

    $.get( "test.php" );
    
С передачей параметров.

    $.get( "test.php", { name: "John", time: "2pm" } );
    

Вывод результата.

    $.get( "test.php", function( data ) {
      alert( "Data Loaded: " + data );
    });
        
    $.get( "test.cgi", { name: "John", time: "2pm" } )
      .done(function( data ) {
        alert( "Data Loaded: " + data );
      });

### $.post()

    $.post(URL,data,callback);

Пример отправки запроса по клику на кнопку.

    $("button").click(function(){
      $.post("demo_test_post.asp",
      {
        name: "Donald Duck",
        city: "Duckburg"
      },
      function(data, status){
        alert("Data: " + data + "\nStatus: " + status);
      });
    });

### Анимация.

Часто используемые эффекты встроены в jQuery как методы, которые вы можете вызвать для любого объекта jQuery:

.show() — показать выбранные элементы;

.hide() — скрыть выбранные элементы;

.fadeIn() — анимация прозрачности выбранных элементов до 0%;

.fadeOut() — анимация прозрачности выбранных элементов до 100%;

.slideDown() — отображение выбранных элементов с помощью вертикального скользящего движения;

.slideUp() — сокрытие выбранные элементы с помощью вертикального скользящего движения;

.slideToggle() — показать или скрыть выбранные элементы с вертикальным скользящим движением в зависимости от того, видны элементы в данный момент или нет.

Можно использовать предопределенные аргументы например скорости.

    $( '.hidden' ).show( 'slow' );

Можно переустановить предопределенную скорость.

    jQuery.fx.speeds.fast = 50;
    
Вы можете предоставить функцию обратного вызова для методов анимации, если желаете указать, что должно произойти после завершения эффекта. 


    $( 'p.old' ).fadeOut( 300, function() {
      $( this ).remove();
    });
    
### Произвольные эффекты с .animate()

    .animate(properties, [duration], [easing], [callback]):jQuery

У метода .animate() есть несколько аргумента:

- объект, определяющий свойства для анимации;

- продолжительность анимации в миллисекундах;

- easing — изменение скорости анимации (будет ли она замедляется к концу выполнения или наоборот ускорится).

- функция обратного вызова, которая будет вызываться после окончания анимации.
    
Метод .animate() может анимировать до указанного конечного значения или увеличить существующее значение.

    $( '.funtimes' ).animate({
        left: '+=50', // увеличить на 50
        opacity: 0.25,
        fontSize: '12px'
      },
      300,
      function() {
        // выполняется, когда анимация завершена
      }
    );
    
jQuery предлагает два важных метода для управления анимацией.

.stop() — останавливает выполняемую в данное время анимацию для выбранных элементов.

.delay() — пауза перед выполнением следующей анимации. В качестве аргумента передаётся желаемое время ожидания в миллисекундах.

Пример.

    <!DOCTYPE html>
    <html>
    <head>
      <style>
        div { 
          background-color:#bca; 
          width:100px; 
          border:1px solid green;
        }
      </style>
      <script src="http://code.jquery.com/jquery-latest.min.js"></script>
    </head>
    <body>
      <button id="go">» Съешь пирожок</button>

      <div id="block">Алиса</div>
      <script>
        // Произведем изменение нескольких css-величин в ходе одной анимации.
        $("#go").click(function(){
          $("#block").animate({ 
            width: "70%",         // ширина станет 70%
            opacity: 0.4,         // прозрачность будет 40%
            marginLeft: "0.6in",  // отступ от левого края элемента станет равным 6 дюймам
            fontSize: "3em",      // размер шрифта увеличится в 3 раза
            borderWidth: "10px"   // толщина рамки станет 10 пикселей
          }, 1500);               // анимация будет происходить 1,5 секунды
        });
      </script>
    </body>
    </html>

### JQuery плагины

https://www.jqueryscript.net/slider/nivo-slider.html





