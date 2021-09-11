# Старт проекта c jQuery и Typescript.

В качестве сборщика будем использовать gulp.

Создадим скрипт настройек компиляции из typescript в js.

Файл tsconfig.json.

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

Инициализируем npm репозиторий.

    npm init
    
Устанавливаем компилятор Typescript

    npm install --save tsc
    
Создаем в папке src файл index.ts

    console.log('Test!!!');
    
Пробуем компилировать.

    ./node_modules/tsc/bin/tsc
    
В итоге компиляция работает и в папке dist создается js файл.



Создадим простой сервер для отдачи index.html

    const baseDir = 'dist';
    const express = require('express')
    const path = require('path')
    const port = 3000;
    const app = express();
    app.use(express.static(path.join(__dirname, baseDir)));
    app.get('*', (req, res) => {
        res.sendFile(path.join(__dirname,'/index.html'));
    });
    app.listen(port);
    console.log('Server started on 3000 port')
      
Установим express.

    npm i express --save
    
Создадим index.html.

    <!doctype html>
    <html lang="en">
        <head>
            <meta charset="utf-8">
            <title>Test page</title>
            <meta name="name" content="TODO: name">
            <meta name="description" content="TODO: description">
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>

        <body>
            <div id="root"> Hello World </div>
            <script src="index.js"></script>
        </body>
    </html>

Запускаем сервер.

    node server.js
    
![start page]({path-to-subject}/images/25.png)

Установим jQuery.

    npm i jquery @types/jquery --save
    
Пробуем импортировать.

    import $ from "jquery";
    console.log($);

Получаем ошибку.

    Module '"/home/zdimon/Desktop/work/ts-gulp/node_modules/@types/jquery/index"' can only be default-imported using the 'esModuleInterop' flagts(1259)


Изменим импорт.

    import * as $ from "jquery";
    
Или выставим esModuleInterop флаг в True в tsconfig.json

После компиляции получаем ошибку.

![start page]({path-to-subject}/images/26.png)

Наш браузер не знает такой конструкции из модульной системы commonjs как require.

А откомпилированный файл ее содержит.

    var $ = require("jquery");
    console.log($);

Поэтому при компиляции необходимо использовать такой инструмент как browserify.

Он умеет преобразовывать ES6 в совместимый ES5.

Для компиляции удобно использовать менеджер задач gulp.

Устанавливаем gulp.

    npm install --save gulp

Делаем простую задачу в файле gulpfile.js.

    var gulp = require('gulp');
    gulp.task('default', (done) => {
        console.log('Gulp task!!');
        done();
    })
    
    
Запуск.

    node node_modules/gulp/bin/gulp.js

Результат работы.

![start page]({path-to-subject}/images/27.png)

Все API gulp сосоит из нескольких функций:

**gulp.src** - выбирает все файлы по маске из указанной директории

**gulp.dest** - создает поток для записи "ванильного" js объекта в папку

**gulp.task** - создает задачу

**gulp.watch** - отслеживает изменения в файлах

**gulp.series** - мы можем перечислять несколько функций, которые будут вызваны одна за другой.


Для последующей работы нам понадобятся следующие инструменты.

browserify - для исключение require из сборки (см. выше);

typescript - компилятор typescript

tsify - подобно аналогу gulp-typescript, предоставляет доступ к компилятору TypeScript;

vinyl-source-stream - преобразовывает "ванильный" вывод browserify в потоковый формат для последующей записи при помощи gulp.dest.

Устанавливаем.

    npm install --save-dev browserify tsify vinyl-source-stream typescript   

Скрипт сборки.

    var gulp = require('gulp');
    var browserify = require('browserify');
    var source = require('vinyl-source-stream');
    var tsify = require("tsify");

    gulp.task('default', (done) => {
        return browserify({
            basedir: './src/client',
            debug: true,
            entries: ['index.tsx']
        })
        .plugin(tsify)
        .bundle()
        .pipe(source('bundle.js'))
        .pipe(gulp.dest("dist/prod"));

    })

У нас сборка содержит библиотеку jquery, однако мы может ее импортировать вручную.

    <script src="https://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>

И так как мы установили прежде 

    npm install --save @types/jquery
    
Переменная $ у нас доступна глобально в скриптах и мы можем явно ее не импортировать и не включать jquery в сборку.

## Обновление страницы браузера после компиляции.

Установим инструмент browser-sync

    npm i browser-sync --save

Определим переменную.

    const browserSync = require('browser-sync').create();

Вынесем компиляцию в отдельную функцию.

    function compileTS() {

	    return browserify({
		    basedir: './src',
		    debug: true,
		    entries: ['index.ts']
	    })
	    .plugin(tsify)
	    .bundle()
	    .pipe(source('index.js'))
	    .pipe(gulp.dest('dist'));
    }

Вызовем ее вот так.

    exports.default = gulp.series(
            compileTS
        );

В gulp.series мы можем перечислять несколько функций, которые будут вызваны одна за другой.

Определим функцию запуска сервера.

    function startBrowserSync() {
	    browserSync.init({
		    server : {
			    baseDir : '.'
		    },
	    });
    }

Функцию перезагрузки.

    function reload(cb) {
	    browserSync.reload();
	    cb();
    }

Функцию отслеживания изменений.

    function watch() {
	    gulp.watch('src', gulp.series(compileTS,reload));
    }

Объеденим все вместе.

    exports.default = gulp.series(
            compileTS,
            gulp.parallel(startBrowserSync, watch)
        );

