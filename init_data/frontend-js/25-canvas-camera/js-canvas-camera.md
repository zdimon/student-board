# Работа с веб камерой и холстом.
    
В начале необходимо добавить элемент video на страницу.

	<video autoplay="true" id="videoElement"></video>

[ссылка на документацию элемента](http://htmlbook.ru/html/video)

В коде получаем элемент.

    var video = document.querySelector("#videoElement");

Этот элемент имеет такое свойство video.srcObject в которое можно положить видеопоток камеры.

Существует такой метод 

    navigator.mediaDevices.getUserMedia({ video: true })

Он нам возвращает промис, который может запустить колбек, который мы впихнем в then и передаст в него поток с камеры. 

[ссылка на документацию](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia)

Захватываем видео.

    if (navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
          video.srcObject = stream;
        })
        .catch(function (err0r) {
          console.log("Something went wrong!");
        });
    }

У элемента video есть одно полезное событие, которое происходит в момент доступности видео, т.к. процесс инициализации может занимать время, это бывает полезно.

    video.addEventListener('canplay', function(ev){...})


## Приостановка трансляции.

Поток может содержать много треков (например брать звук с нескольких мкрофонов).

Поэтому при останове, мы по ним должны пробегать и каждого стопать.

    function stop(e) {
      var stream = video.srcObject;
      var tracks = stream.getTracks();

      for (var i = 0; i < tracks.length; i++) {
        var track = tracks[i];
        track.stop();
      }

      video.srcObject = null;
    }

# Забираем картинку с камеры и пишем в канвас.

Ставим на страницу канвас и элемент картинки.

      <canvas id="canvas"> </canvas>
      <img id="photo" alt="The screen capture will appear in this box.">

Получаем элементы.

    canvas = document.getElementById('canvas');
    photo = document.getElementById('photo');

Прикол канваса в том, что в его контекст можно запихнуть то, что в данный момент в элементе video так:

    context.drawImage(video, 0, 0, width, height);

Но сперва этот контекст нужно получить.

     var context = canvas.getContext('2d');

Конвертировать то что на холсте в формат, доступный элементу img.

    var data = canvas.toDataURL('image/png');

Кинуть данные в img.

    photo.setAttribute('src', data);

[ссылка на статью с работой с инструментом webcam-easy](https://medium.com/swlh/how-to-access-webcam-and-take-picture-with-javascript-b9116a983d78)

## Рисование примитивов.

Сетка.

![start page]({path-to-subject}/images/1.png)

### Прямоугольники.

Холст поддерживает только одну примитивную фигуру: прямоугольник. 

Все другие фигуры должны быть созданы комбинацией одного или большего количества контуров (paths), набором точек, соединенных в линии. К счастью в ассортименте рисования контуров у нас есть  функции, которые делают возможным составление очень сложных фигур.

Функции для рисования.

**fillRect(x, y, width, height)** - Рисование заполненного прямоугольника.

**strokeRect(x, y, width, height)** - Рисование прямоугольного контура.

**clearRect(x, y, width, height)** - Очистка  прямоугольной области, делая содержимое совершенно прозрачным.

## Рисование контуров (path)

[ссылка на источник](https://developer.mozilla.org/ru/docs/Web/API/Canvas_API/Tutorial/%D0%A0%D0%B8%D1%81%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5_%D1%84%D0%B8%D0%B3%D1%83%D1%80)

Остальные примитивные фигуры создаются контурами. Контур - это набор точек, которые, соединяясь в отрезки линий, могут образовывать различные фигуры, изогнутые или нет, разной ширины и разного цвета. Контур (или субконтур) может быть закрытым.

Создание фигур используя контуры происходит в несколько важных шагов:

Сначала вы создаете контур.

Затем, используя команды рисования, рисуете контур.

Потом закрываете контур (чтобы вернуться в контекст).

Созданный контур вы можете обвести или залить для его отображения.

### Функции

**beginPath()** - Создает новый контур. После создания используется в дальнейшем командами рисования при построении контуров.

**closePath()** - Закрывает контур, так что будущие команды рисования вновь направлены контекст.

**stroke()** - Рисует фигуру с внешней обводкой.

**fill()** - Рисует фигуру с заливкой внутренней области.

Пример рисования треугольника.


    function draw() {
      var canvas = document.getElementById('canvas');
      if (canvas.getContext){
        var ctx = canvas.getContext('2d');

        ctx.beginPath();
        ctx.moveTo(75,50);
        ctx.lineTo(100,75);
        ctx.lineTo(100,25);
        ctx.fill();
      }
    }

moveTo - передвижение пера.

## Дуги

Для рисования дуг и окружностей, используем методы arc() и arcTo().

    arc(x, y, radius, startAngle, endAngle, anticlockwise)

Рисуем дугу с центром в точке (x,y) радиусом radius, начиная с угла startAngle и заканчивая в endAngle в направлении против часовой стрелки anticlockwise (по умолчанию по ходу движения часовой стрелки).


    arcTo(x1, y1, x2, y2, radius)

Рисуем дугу с заданными контрольными точками и радиусом, соединяя эти точки прямой линией.






