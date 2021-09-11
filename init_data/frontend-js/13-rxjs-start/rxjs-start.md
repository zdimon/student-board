## Начало работы с rxjs.

rxjs - одня из наиболее новых и популярных библиотек для функционального и реактивного программирования.

Она включает около 50 функций (операторов) и имеет имплементации для всех популярных языков.

### Основные положения.

Все данные представляются потоками событий с началом, цепью событий и концом.

Реактивное программирование - это приемы оперирования этим потоком событий.

Вот как представляеся поток, в котором сгенерированы 3 элемента и поток завершен удачно.

![start page]({path-to-subject}/images/3.png)

Вот как представляеся поток, в котором сгенерированы 3 элемента и поток завершен неудачно.

![start page]({path-to-subject}/images/34png)


Вот как представляеся поток, в котором сгенерированы 3 элемента (события) и поток не завершен.

![start page]({path-to-subject}/images/2.png)


Включаем на страницу в загрузчик SystemJS.

    <!DOCTYPE html>
    <html>
        <head><title>TypeScript Greeter</title>
            <script src="node_modules/systemjs/dist/system.js"></script>
        </head>
        <body>
            <script>
                SystemJS.config({
                    defaultJSExtensions: true,
                    map: {
                        'rxjs': '../node_modules/rxjs'
                    },
                    packages: {
                        'rxjs': {
                            main: './index.js'
                        }
                    }
                });
                SystemJS.import('dist/app.js');        
            </script>
        </body>
    </html>

## Оператор of.

[ссылка на документацию](https://www.learnrxjs.io/learn-rxjs/operators/creation/of)

Создает наблюдаемый объект из любой коллекции.


    import {of} from 'rxjs';

    const source = [1,2,3,4,5];

    of(source).subscribe((el) => {
        console.log(el);
    })

Так же можно из событий.

## fromEvent

[ссылка на документацию](https://www.learnrxjs.io/learn-rxjs/operators/creation/fromevent)


    const move$ = fromEvent(document, 'mousemove');

    move$.subscribe((e)=>{
        console.log(e);
    })



