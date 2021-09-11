## Typescript. Начало работы.

## Инициализация npm проекта.

    npm init

## Установка транспилятора

    sudo npm install -g typescript

    
## Установка и обновление nodejs и npm.

    npm install npm@latest -g
    sudo npm cache clean -f
    sudo npm install -g n
    sudo n stable

Проверка версии.

    node -v   

## Создание конфигурационного файла.

## Первая программа app.ts.

    function greeter(person) {
        return "Hello, " + person;
    }

    greeter('Dima')

Компиляция.

    tsc app.ts

Либо указывая полный путь.

    ./node_modules/.bin/tsc

Стартовая страница

    <!DOCTYPE html>
    <html>
        <head><title>TypeScript Greeter</title></head>
        <body>
            <script src="app.js"></script>
        </body>
    </html>

Добавление веб сервера.

    npm install lite-server --save
    
*Иногда возникает ошибка permission denied, mkdir '/home/user/.npm для устранения удалите папку .npm*

## Запуск веб сервера.

    ./node_modules/.bin/lite-server
    
## Создание конфигурационного файла tsconfig.json

В этом файле определяются:

- входная (корневая) директория проекта;

- выходная директория;

- опции компилятора;

- определяются какие файлы включать и выключать из компиляции.

    {
        "compilerOptions": {
            "emitDecoratorMetadata": true,
            "experimentalDecorators": true,
            "module": "commonjs",
            "target": "ES5",
            "outDir": "built",
            "rootDir": "src"
        }
    }


**если вы указываете файл для компиляции явно то конфигурационный файл игнорируется!**

[Список всех настроек typescript](https://www.typescriptlang.org/docs/handbook/compiler-options.html)

Перенесем app.ts файл в папку src.

### Запуск транспилятора в режиме отслеживания изменений (watch).

    tsc -w
    
## Исключение и включение каталогов из процесса слежения (tsconfig.json).    

    {
    "compilerOptions": {
        ....
    },
    "include": [
        "**/*"
    ],
    "exclude": [
        "node_modules",
        "**/*.spec.ts"
    ]}
        
При этом приняты следующие условные обозначения.

* - любое кол-во символов, исключая разделитель каталогов

? - один любой символ, исключая разделитель каталогов

**/ - все подкаталоги       
        
Полная версия

    {
        "compilerOptions": {
            "module": "commonjs",
            "esModuleInterop": true,
            "target": "es6",
            "noImplicitAny": false,
            "moduleResolution": "node",
            "sourceMap": true,
            "outDir": "dist",
            "baseUrl": ".",
            "paths": {
                "*": [
                    "node_modules/*"
                ]
            }
        },
        "include": [
            "src/**/*"
        ],
        "exclude": [
            "node_modules"
        ]
    }


## Определение типа передаваемого значения.

    function greeter(person: string) {
    
## Попытка передать неверный тип.

    let user = [0, 1, 2];
    document.body.innerHTML = greeter(user);
    
    src/app.ts:7:35 - error TS2345: Argument of type 'number[]' is not assignable to parameter of type 'string'.
  
## Определение типа возвращаемого значения.

    function greeter(person: string): number {
        return "Hello, " + person;
    }   
    src/app.ts:8:1 - error TS2322: Type 'number' is not assignable to type 'string'.
 
## Модульность

Определим библиотечную функцию src/lib/function.ts.

    export function sayHello( name ) {
        return `Hello {$name}`;
    };    
    
Импортируем ее в главном модуле app.js.

    import { sayHello } from './lib/function';

    console.log(sayHello());

Получаем ошибку в консоле.    
    
    app.js:2 Uncaught ReferenceError: exports is not defined
    
Это значит что js не знает конструкцию exports и для этого необходимо использовать загрузчик модулей, например SystemJS.

Установка.

    npm install systemjs@0.19.22 --save

Шаблон

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

При компиляции на лету (внутри браузера без запуска tsc).

    <!DOCTYPE html>
    <html>
        <head><title>TypeScript Greeter</title>
            <script src="node_modules/systemjs/dist/system.js"></script>
            <script src="node_modules/typescript/lib/typescript.js"></script>
        </head>
        <body>
            <script>
                SystemJS.config({
                    transpiler: 'typescript',
                        packages: {
                        src: {
                              defaultExtension: 'ts'
                            }
                        }
                });
                SystemJS.import('src/index.ts');      
                           
            </script>
        </body>
    </html>







 
