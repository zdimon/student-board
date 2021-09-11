# ReactJs начало. Рабочее окружение.

## Быстрый старт проекта (скафолдинг).

    npx create-react-app my-app --template typescript

Запуск сервера

    npm run start

Сборка.

    npm run build

Сборка с отслеживанием изменений.

    npm install npm-watch --save

Добавляем в package.json

    ...
    "watch": {
        "build": {
          "patterns": [
            "src"
          ],
          "extensions": "js,jsx"
        }
      },
      "scripts": {
        "watch": "npm-watch",

      ....

Запуск.

    npm run watch
       
## Ставим реакт в ручную.
    
    npm install react react-dom --save
    npm install @types/react --save

Переименуем index.ts в index.tsx

Добавим опцию jsx в tsconfig.json

    {
        "compilerOptions": {
            "module": "commonjs",
            "target": "ES5",
            "outDir": "dist",
            "rootDir": "src",
            "esModuleInterop": true,
            "jsx": "react"
        },
        "exclude": [
            "node_modules"
        ]
    }

Создадим простейший компонент src/client/index.tsx.

    import * as React from "react";
    import * as ReactDOM from 'react-dom';

    function App() {
        return (
          <h1>Hello from react!</h1>
        );
    }

    ReactDOM.render(
        <App />,
        document.getElementById('react-app')
      );

Установка SystemJs

    npm install systemjs@0.19.22 --save

Подключаем в загрузчике.

    <!DOCTYPE html>
    <html>
        <head><title>TypeScript Greeter</title>
            <script src="node_modules/systemjs/dist/system.js"></script>
            
        </head>
        <body>
           <div id="react-app"></div>
          <script>
                SystemJS.config({
                    defaultJSExtensions: true,
                    map: {
                        'react': 'node_modules/react/umd',
                        'react-dom': 'node_modules/react-dom/umd'
                    },
                    packages: {
                        'react': {
                            main: './react.development.js'
                        },
                        'react-dom': {
                            main: './react-dom.development.js'
                        }
                    }
                });
                SystemJS.import('dist/client/index.js');           
          </script>
        </body>
    </html>

Использование сборщика вместо SystemJs.

Устанавливаем gulp.

    npm install --save gulp

Делаем простую задачу в файле gulp.js.

    var gulp = require('gulp');
    gulp.task('default', () => {
        console.log('Gulp task!!');
    })

Запуск.

    node node_modules/gulp/bin/gulp.js

Так как процесс асинхронный мы должны вернуть событие завершения.

    var gulp = require('gulp');
    gulp.task('default', (done) => {
        console.log('Gulp task!!');
        done();
    })

Установим компилятор gulp-typescript

     npm install --save gulp-typescript
     npm install --save browserify

Откомпилируем в папку dist/prod

    var gulp = require('gulp');
    var browserify = require('browserify');
    var ts = require("gulp-typescript");
    var tsProject = ts.createProject("tsconfig.json");
    gulp.task('default', (done) => {
        return tsProject.src()
            .pipe(tsProject())
            .js.pipe(gulp.dest("dist/prod"));

    })

Теперь нам необходимо собрать все модули в один файл.

Сначала установим browserify, tsify, и vinyl-source-stream. tsify это плагин для Browserify, который, подобно gulp-typescript, предоставляет доступ к компилятору TypeScript. vinyl-source-stream позволяет согласовать файловый вывод Browserify и формат под названием vinyl, который понимает gulp.

    npm install --save-dev browserify tsify vinyl-source-stream

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

Теперь можно включить наш бандл в страницу одним файлом и убрать SystemJs.

    <script src="dist/prod/bundle.js"></script>

bundle получился около 4.1 мб.

Попробуем аглифицировать (обфуркация).

Устоановка

    npm install gulp-uglify --save
    npm install vinyl-buffer --save

Применение.
    ...
    var uglify = require('gulp-uglify');
    var buffer = require('vinyl-buffer');

    gulp.task('default', (done) => {
        return browserify({
            basedir: './src/client',
            debug: true,
            entries: ['index.tsx']
        })
        .plugin(tsify)
        .bundle()
        .pipe(source('bundle.js'))
        .pipe(buffer())
        .pipe(uglify())
        .pipe(gulp.dest("dist/prod"));

    })

Получаем ошибку.

![start page]({path-to-subject}/images/4.png)

Оказывается uglify не поддерживает es6.

Ставим тот что поддерживает.

    npm i gulp-uglify-es --save

Меняем скрипт.

    var uglify = require('gulp-uglify-es').default;

![start page]({path-to-subject}/images/5.png)

Теперь  bundle.js уменьшился до 1.4 мб

Обработка css требует еще одной библиотеки.

    npm install --save css-modulesify
    
Приминение.

    var cssModulesify = require('css-modulesify');
    ....
    gulp.task('default', (done) => {
        return browserify(...)
        .plugin(cssModulesify, {
            rootDir: __dirname,
            output: './dist/main.css',
            generateScopedName: cssModulesify.generateShortName
          })
        ...
        
Отслеживание изменений при помощи nodemon.    

    sudo npm install -g nodemon
    
Команда для запуска.

    nodemon node_modules/gulp/bin/gulp.js -e tsx    
       
Удаление билда перед пересозданием.

Устанавливаем библиотеку.

    npm install --save-dev del

Использование.

    var del = require('del');
    
    gulp.task('default', (done) => {
        del(['../app/static/js/app/**'],{force: true});

Попробуем еще уменьшить компрессором gzip

    npm i compression --save

Вставляем в код сервера.


    const compression = require('compression');
    app.use(compression())

По итогу получили.

![start page]({path-to-subject}/images/6.png)

340 кб - неплохо, учитывая что это все вместе с библиотекой React.

Теперь разберемся как копировать index.html в сборку.

Создадим html для продакшина, который использует бандл src/server/tpl/index_prod.html.

    <!DOCTYPE html>
    <html>
        <head>
          <title>Production</title>
        </head>
        <body>
           <div id="react-app"></div>
          <script src="dist/prod/bundle.js"></script>
        </body>
    </html>

Т.к. мы будем копировать с другим именем установим библиотеку для этого.

    npm i gulp-rename --save

Скопируем index_prod.html как index.html при сборке в каталог dist.

Сделаем это в отдельной задаче

    rename = require('gulp-rename'),
    gulp.task("copy-html", function () {
        return gulp.src('./src/server/tpl/index_prod.html')
            .pipe(rename('index.html'))
            .pipe(gulp.dest("dist/prod"));
    });


Запускаем
    
![start page]({path-to-subject}/images/7.png)

Теперь включим эту задачу в основную сборку.

### Комбинирование задач.

    gulp.task("copy-html", function () {
       ...
    });


    gulp.task('build-app', (done) => {
        ...
    })

    gulp.task('default', gulp.series('copy-html', 'build-app'));





