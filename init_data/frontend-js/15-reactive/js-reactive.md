# Реактивное программирование с RxJs.

## Эволюция в программировании асинхронных процессов.

### Колбеки.

    jQuery(() => {

        function B(callback) {
            callback('Done!');
        }

        function A() {
            console.log('Hello from calback');
        }

        B(A);
    })

Коллбек - это функция A, передаваемая в качестве параметра другой функции B, которая осуществляет асинхронную операцию. Когда B закончит выполнение, она обратно вызовет A.

Колбеки используются для обработки таких операций как передача по сети, доступ к БД, обработка пользовательского ввода.

Колбеки имеют следующие недостатки.

1. Колбековый ад. Множество вложенных колбеков.

    firstFunction(args, function() {
      secondFunction(args, function() {
        thirdFunction(args, function() {
          // And so on…
        });
      });
    });

2. Колбеки могут быть вызваны более одного раза и нет гарантии их одноразового выполнения.
При множественном задействовании могут приводить к трудностям выявления ошибок.


3. Колбеки меняют семантику работы с ошибками. При этом отхотят от механизма try/catch и возлагают на программиста ответственность проверки ошибок и передача их по цепочке вызовов.

    var num = '5';

    myFunction(num, function callback(err, result) {
      if (err) {
        // handle error
      }

      // handle result
    });

4. При необходимости обеспечения многопотокового выполнения, программирование становится крайне сложным. Когда, к примеру, нам необходимо скомбинировать данные, из разных независимых асинхронных вызовов. При этом возникает необходимость отслеживать состояние каждого из них во временных переменных перед комбинацией а потом передачу их функции-комбинатора в нужной последовательности.

### Промисы.

Промисы представляют собой результат выполнения асинхронной операции.
В коде, основанном на промисах, вызов асинхронной операции вернет специальный объект-промис, который может находится в следующих состояниях: 

- быть выполененным (resolved) 

- отвергнутым (rejected) в случае ошибок 

- выполнятся (pending)

Таким образом код становится более похож на синхронный и исключает вложенные блоки.

Определение промиса.

    var promise = new Promise(function(resolve, reject) {
        // do a thing, possibly async, then…

        
  
        if (true === true) {
          resolve("Stuff worked!");
        }
        else {
          reject(Error("It broke"));
        }
      })
  
      promise.then(function(result) {
        console.log(result); // "Stuff worked!"
      }, function(err) {
        console.log(err); // Error: "It broke"
      }).then()
        .then()
        .then();

      promise.then(function(result) {
        console.log(result); // "Stuff worked!"
      }, function(err) {
        console.log(err); // Error: "It broke"
      });

К сожалению, промисы являются лишь особым образом работы с колбеками и так же как они способны возвращать единственный результат за раз. Это делает их бесполезными в повторяющихся процессах, таких как клики мышью или потоках данных, приходящих от удаленного источника.
В таких случаях мы вынуждены создавать для каждого события в потоке отдельный промис.

## Генератор событий Event Emitter.

Суть - мы генерируем событие и подписываем на него обработчика (слушателя). 
Это прекрасный способ разделить функциональность и ослабить связи между элементами логики.

Однако это имеет свои проблемы.

1. Слушатели порождают побочные эффекты т.к. не учитывают то, что возвращают и вынуждены изменять то, что находится за их пределами в окружающем пространстве имен.

2. События - это не простые объекты первого класса. Например серия кликов мышью не может быть передана в качестве массива что само по себе массив. Мы должны обрабатывать кажндое событие индивидуально.


3. Очень просто пропустить событие, если мы опоздали со слушателем. В ситуации когда событие воздикает до того момента как мы добавляем слушателя.

## Что такое реактивное программирование?

По простому - это механизмы создания, изменения и реагирования на потоки данных.

Эти механизмы описываются следующими диаграммами.

![start page]({path-to-subject}/images/2.png)

## Что такое RxJS?

Это имплементация принципов реактивного программирования (RX) для языка JS.

Основано на применении 2 паттернов - итератор и наблюдатель.

### Наблюдатель.

    function Producer() {
        this.listeners = [];
    }
    Producer.prototype.add = function(listener) {
        this.listeners.push(listener);
    };
    Producer.prototype.remove = function(listener) {
        var index = this.listeners.indexOf(listener);
        this.listeners.splice(index, 1);
    };
    Producer.prototype.notify = function(message) {
        this.listeners.forEach(function(listener) {
        listener.update(message);
    });

Применение в клиентском коде.

    var listener1 = {
        update: function(message) {
        console.log('Listener 1 received:', message);
    }
    };
    var listener2 = {
        update: function(message) {
        console.log('Listener 2 received:', message);
    }
    };

    var notifier = new Producer();
    notifier.add(listener1);
    notifier.add(listener2);
    notifier.notify('Hello there!');


### Итератор.

    function iterateOnMultiples(arr, divisor) {
        this.cursor = 0;
        this.array = arr;
        this.divisor = divisor || 1;

    }

    iterateOnMultiples.prototype.next = function() {
        while (this.cursor < this.array.length) {
            var value = this.array[this.cursor++];
                if (value % this.divisor === 0) {
                return value;
            }
        }
    };

    iterateOnMultiples.prototype.hasNext = function() {
        var cur = this.cursor;
        while (cur < this.array.length) {
            if (this.array[cur++] % this.divisor === 0) {
                return true;
            }
        }
        return false;
    };


    var consumer = new iterateOnMultiples([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 3);
    console.log(consumer.next(), consumer.hasNext()); // 3 true
    console.log(consumer.next(), consumer.hasNext()); // 6 true
    console.log(consumer.next(), consumer.hasNext()); // 9 false


Возьмем поток клика мышью.

![start page]({path-to-subject}/images/3.png)

Программа для отслеживания может иметь следующий вид.


    $(document).on('click', (evt) => {
        console.log(evt);
    })

Проблема тут в том что работать с событиями не так просто как с массивами.

К примеру если мы хотим отследить первые 5 нажатий.


    var clicks = 0;
    var registerClicks = $(document).on('click', (evt) => {
        if (clicks < 5) {
            clicks++;
            console.log(clicks);
        } else {
            $(document).off('click', registerClicks);
        }
    })

Мы вынуждены вводить внешнюю переменную состояния clicks и дополнительные проверки.

Все это называется побочными эффектами.

Как это выглядит в RxJs.

    Rx.Observable.fromEvent(document, 'click')
    .take(5)
    .subscribe(function(c) { console.log(c.clientX, c.clientY) })

## Установка Rx.

    npm install rx --save

Включение.

    <script src="node_modules/rx/dist/rx.all.js"></script>

    npm install rxjs --save

## Установка RxJs.

Простого включения не достаточно и нужно пользоваться загрузчиком.

    
    <script src="node_modules/rxjs/Rx.js"></script>

![start page]({path-to-subject}/images/4.png)

RxJs отличается от Rx большей производительностью, поддержкой модульности и иструментами для дебага.

Если мы хотим добавить условие и отслеживать клик в области то это делается так:


    Rx.Observable.fromEvent(document, 'click')
    .filter(function(c) { return c.clientX > window.innerWidth / 2; })
    .take(5)
    .subscribe(function(c) { console.log(c.clientX, c.clientY) })

Таким образом Observable (отслеживаемость) генерирует события на манер итератора, и проталкивает данные внутрь подписчика (потребителя), это называется механизмом push. В отличие от механизма pull при котором подписчик бы запрашивал данные.

## Ручное создание отслеживаемого потока (ОП).


    var observable = Rx.Observable.create(function(observer) {
        observer.onNext('Simon');
        observer.onNext('Jen');
        observer.onNext('Sergi');
        observer.onCompleted(); // We are done
    });

    observable.subscribe((val) => {
        console.log(val);
    })

![start page]({path-to-subject}/images/5.png)


В большинстве случаев создавать такие отслеживаемые потоки не приходится т.к. существует много инструментов по их созданию из всевозможных событий.


## Из массива.

    Rx.Observable
    .from(['1', '2', '3'])
    .subscribe(
        function(x) { console.log('Next: ' + x); }
    );

## Из события.

    var allMoves = Rx.Observable.fromEvent(document, 'mousemove');

    allMoves.subscribe(function(e) {
        console.log(e.clientX, e.clientY);
    });

Отследим перемещение в разных областях экрана.

    var movesOnTheRight = allMoves.filter(function(e) {
        return e.clientX > window.innerWidth / 2;
    });
    var movesOnTheLeft = allMoves.filter(function(e) {
        return e.clientX < window.innerWidth / 2;
    });

    movesOnTheRight.subscribe(function(e) {
        console.log('Mouse is on the right:', e.clientX);
    });
        movesOnTheLeft.subscribe(function(e) {
        console.log('Mouse is on the left:', e.clientX);
    })

## Комбинаторика потоков.

[ссылка на полезную статью](https://indepth.dev/learn-to-combine-rxjs-sequences-with-super-intuitive-interactive-diagrams/)

[ссылка на основные операторы](http://stepansuvorov.com/blog/2017/03/rxjs-6-%D0%BE%D0%BF%D0%B5%D1%80%D0%B0%D1%82%D0%BE%D1%80%D0%BE%D0%B2-%D0%BA%D0%BE%D1%82%D0%BE%D1%80%D1%8B%D0%B5-%D0%B2%D1%8B-%D0%B4%D0%BE%D0%BB%D0%B6%D0%BD%D1%8B-%D0%B7%D0%BD%D0%B0%D1%82%D1%8C/)

Общие обозначения

![start page]({path-to-subject}/images/1.gif)

### Merge

    const a = stream('a', 200, 3, 'partial');
    const b = stream('b', 200, 3, 'partial');
    merge(a, b).subscribe(fullObserver('merge'));
    // can also be used as an instance operator
    a.pipe(merge(b)).subscribe(fullObserver('merge'));


![start page]({path-to-subject}/images/6.png)
 

![start page]({path-to-subject}/images/2.gif)

### Drad and drop

Создадим два блока.


    <div id="out">
      <div id="in"></div>
    </div>

Стили

    #out {
        width: 200px;
        height: 200px;
        position: relative;
        border: 1px solid red;
    }

    #in {
        position: absolute;
        border-radius: 50%;
        background-color: red;
        width: 30px;
        height: 30px;
    }

Определим 3 потока и привяжем их к элементам.

    var box = $('#in');
    var document = $('#out');
    const mousedown$ = Rx.Observable.fromEvent(box, 'mousedown');
    const mousemove$ = Rx.Observable.fromEvent(document, 'mousemove');
    const mouseup$ = Rx.Observable.fromEvent(document, 'mouseup');


Переключимся с потока mousedown$ на mousemove$.

    mousedown$.switchMap((evt) => mousemove$).subscribe((e) => {
        console.log(`${e.clientX}-${e.clientY}`);
    })

Переключимся с mousemove$ на mouseup$.


    mousedown$.switchMap((evtup) => 
        mousemove$.switchMap((evtdwn) => mouseup$))
    .subscribe((e) => {
        console.log(`${e.clientX}-${e.clientY}`);
    })

Передвинем блок.

    mousedown$.switchMap((evtup) => 
        mousemove$.switchMap((evtdwn) => mouseup$))
    .subscribe((e) => {
        console.log(`${e.clientX}-${e.clientY}`);
        box.css({ top: e.offsetY+'px' });
        box.css({ left: e.offsetX+'px' });
      
    })

Передвигаем в момент движения.

    mousedown$.switchMap((evtup) => mousemove$)
    .subscribe((e) => {
        console.log(`${e.clientX}-${e.clientY}`);
        box.css({ top: e.offsetY+'px' });
        box.css({ left: e.offsetX+'px' });
      
    })

Прекращаем передвигать при mouseup при помощи takeUntil.

    mousedown$.switchMap((evtup) => mousemove$.takeUntil(mouseup$))
    .subscribe((e) => {
        console.log(`${e.clientX}-${e.clientY}`);
        box.css({ top: e.offsetY+'px' });
        box.css({ left: e.offsetX+'px' });
    }) 

Обращаем внимание что takeUntil применяется к отслеживаемому потоку mousemove$ т.к. если его применить к тому что возвращает switchMap, например так:


    mousedown$.switchMap((evtup) => mousemove$)
    .takeUntil(mouseup$)
    .subscribe((e) => {
        console.log(`${e.clientX}-${e.clientY}`);
        box.css({ top: e.offsetY+'px' });
        box.css({ left: e.offsetX+'px' });

    })       

То объект будет передвинут но после этого произойдет отписка от потока mousedown$ и больше передвигать станет невозможно. 

### Игра звездные войны.

Создадим канвас.

    var canvas = document.createElement('canvas');
    var ctx = canvas.getContext("2d");
    document.body.appendChild(canvas);
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

Создадим масив из случайных звезд

    var SPEED = 40;
    var STAR_NUMBER = 250;
    var StarStream = Rx.Observable.range(1, STAR_NUMBER)
    .map(function() {
        return {
            x: parseInt(Math.random() * canvas.width),
            y: parseInt(Math.random() * canvas.height),
            size: Math.random() * 3 + 1
        };
    })

    StarStream.subscribe((evt) => {
        console.log(evt);
    })

Преобразуем в массив .toArray();.

    var StarStream = Rx.Observable.range(1, STAR_NUMBER)
    .map(...).toArray();


Закрасим небо в черный и включим это в подписку.

    StarStream.subscribe((evt) => {
        paintStars();
    })

    function paintStars() {
        ctx.fillStyle = '#000000';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    }

## Операторы flatMap/mergeMap и switchMap

Используется когда нужно объединить данные из внутреннего отслеживаемого потока (ОП) но хотите контролировать число внутренних подписчиков.
Например когда мы используем switchMap каждый внутренний подписчик завершается при генерации данных новым ОП. Таки образо в каждый момент времени активен один ОП (источник данных). 

Тогда как mergeMap позволяет быть активным многим подписчикам одновременно из разных ОП.

![start page]({path-to-subject}/images/3.gif)

![start page]({path-to-subject}/images/4.gif)

Создадим новый ОП в операторе switchMap с заданным интервалом, в котором будем пересчитывать координаты каждой звезды.

    var StarStream = Rx.Observable.range(1, STAR_NUMBER)
    .map(function() {
        return {
            x: parseInt(Math.random() * canvas.width),
            y: parseInt(Math.random() * canvas.height),
            size: Math.random() * 3 + 1
        };
    })
    .toArray()
    .switchMap((starArray) => {
        return Rx.Observable.interval(SPEED).map(function() {
            starArray.forEach(function(star) {
                if (star.y >= canvas.height) {
                    star.y = 0; // Reset star to top of the screen
                }
                star.y += 3; // Move star
            });
            return starArray;
        });
    });

Изменим подписку т.к. теперь в нее будет попадать масив звезд 40 раз в секунду. 

    StarStream.subscribe((starsArray) => {
        paintStars(starsArray);
    })


Вводим массив звезд аргументом в функцию paintStars и отрисовываем в цикле.

    function paintStars(stars) {
        ctx.fillStyle = '#000000';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#ffffff';
        stars.forEach(function(star) {
            ctx.fillRect(star.x, star.y, star.size, star.size);
        });
    }

Добавляем ОП (отслеживаемый поток) космического корабля.

    var HERO_Y = canvas.height - 30;
    var mouseMove = Rx.Observable.fromEvent(canvas, 'mousemove');

    var SpaceShip = mouseMove
    .map(function(event) {
        return {
            x: event.clientX,
            y: HERO_Y
        };
    })
    .startWith({
        x: canvas.width / 2,
        y: HERO_Y
    });


    SpaceShip.subscribe((obj) => console.log(obj))

Добавим функции отрисовки трехугольника и включим ее в подписку.


    function drawTriangle(x, y, width, color, direction) {
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.moveTo(x - width, y);
        ctx.lineTo(x, direction === 'up' ? y - width : y + width);
        ctx.lineTo(x + width, y);
        ctx.lineTo(x - width,y);
        ctx.fill();
    }

    function paintSpaceShip(obj) {
        drawTriangle(obj.x, obj.y, 20, '#ff0000', 'up');
    }

    SpaceShip.subscribe((obj) => paintSpaceShip(obj))


Проблема в том что отрисовка звезд стирает корабль. Нам необходимо обьеденить эти два потока и сначало отрисовывать звезды, а потом корабль.

Обьеденим отрисовки в отдельной функции, которая получит обьект с персонажами.



    function renderScene(actors) {
        paintStars(actors.stars);
        paintSpaceShip(actors.spaceship);
    }

Создадим новый поток игры.

    var Game = Rx.Observable
    .combineLatest(
    StarStream, SpaceShip,
    function(stars, spaceship) {
        return { stars: stars, spaceship: spaceship };
    });

Работа функции combineLatest

![start page]({path-to-subject}/images/5.gif)

Подпишем renderScene к потоку Game.

    Game.subscribe(renderScene);

Уберем

    // StarStream.subscribe((starsArray) => {
    //     paintStars(starsArray);
    // })

Генерация врагов.

Будем создавать массив раз в 1.5 сек.

    var ENEMY_FREQ = 1500;
    var Enemies = Rx.Observable.interval(ENEMY_FREQ)
    .scan((enemyArray) => {
        var enemy = {
        x: parseInt(Math.random() * canvas.width),
        y: -30,
    };
    enemyArray.push(enemy);
    return enemyArray;
    }, []);

    Enemies.subscribe((val) => console.log(val))

Функция scan применяет заданную функцию к каждому элементу потока, причем второй аргумет использует в качестве начального значения.

Добавляем третий поток в combineLatest.

    var Game = Rx.Observable
    .combineLatest(
    StarStream, SpaceShip, Enemies,
    function(stars, spaceship, enemies) {
        return { stars: stars, spaceship: spaceship, enemies: enemies };
    });

![start page]({path-to-subject}/images/7.png)

Создадим функцию генерации случайных координат.


    function getRandomInt(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }

Отрисовываем со сдвигом.

    function paintEnemies(enemies) {
        enemies.forEach(function(enemy) {
            enemy.y += 5;
            enemy.x += getRandomInt(-15, 15);
            drawTriangle(enemy.x, enemy.y, 20, '#00ff00', 'down');
        });
    }

Включаем в прорисовку.

    function renderScene(actors) {
        paintStars(actors.stars);
        paintSpaceShip(actors.spaceship);
        paintEnemies(actors.enemies);
    }

Добавим sample(SPEED) в combineLatest тем самым скажем "никогда не отдавай данные чаще 40 раз в секунду" 

    var Game = Rx.Observable
    .combineLatest(
    StarStream, SpaceShip, Enemies,
    function(stars, spaceship, enemies) {
        return { stars: stars, spaceship: spaceship, enemies: enemies };
    }).sample(SPEED);

## Стрельба.

Смержим два события в поток не чаще 5 раз в сек.

    var playerFiring = Rx.Observable.fromEvent(canvas, 'click')
    .sample(200)
    .timestamp();

Соединим ОП корабля и стрельбы чтобы начать стрелять из координат текущего корабля.

    var HeroShots = Rx.Observable
    .combineLatest(
        playerFiring,
        SpaceShip,
        function(shotEvents, spaceShip) {
            return { x: spaceShip.x };
        })
    .scan(function(shotArray, shot) {
        shotArray.push({x: shot.x, y: HERO_Y});
        return shotArray;
    }, []);

Создадим функцию отрисовки пулек.

    var SHOOTING_SPEED = 15;
    function paintHeroShots(heroShots) {
        heroShots.forEach(function(shot) {
            shot.y -= SHOOTING_SPEED;
            drawTriangle(shot.x, shot.y, 5, '#ffff00', 'up');
        });
    }

Включим ее в renderScene

    function renderScene(actors) {
        paintStars(actors.stars);
        paintSpaceShip(actors.spaceship);
        paintEnemies(actors.enemies);
        paintHeroShots(actors.heroShots);
    }


Добавим пульки в сцену.

    var Game = Rx.Observable
    .combineLatest(
    StarStream, SpaceShip, Enemies, HeroShots,
    function(stars, spaceship, enemies, heroShots) {
        return { 
            stars: stars, 
            spaceship: spaceship, 
            enemies: enemies,
            heroShots: heroShots
        };
    }).sample(SPEED);

Изменим генерацию пуль исходя из timestamp.

    var HeroShots = Rx.Observable
    .combineLatest(
        playerFiring,
        SpaceShip,
        function(shotEvents, spaceShip) {
            return { x: spaceShip.x, timestamp: shotEvents.timestamp,};
        })
    .distinctUntilChanged(function(shot) { return shot.timestamp; })
    .scan(function(shotArray, shot) {
        shotArray.push({x: shot.x, y: HERO_Y});
        return shotArray;
    }, []);

![start page]({path-to-subject}/images/8.png)


