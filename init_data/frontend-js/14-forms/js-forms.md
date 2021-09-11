# Работа с формами на JQuery.

Чтобы понимать роль и место форм, особенности их
атрибутов и элементов, давайте рассмотрим общую схему
организации интернет-ресурса.

![start page]({path-to-subject}/images/1.png)

Обычно в организации ресурса выделяют три уровня:
пользователь, клиент и сервер.

**Уровень пользователя** — это визуальный интерфейс
ресурса. Именно его, как правило, и называют сайтом.
Это то, что мы видим на экране браузера после успешной
загрузки ресурса. Для создания интерфейса применяется
язык разметки HTML.


**Уровень клиента** — это программное обеспечение,
которое создает и прорисовывает интерфейс. Оно также
их истории посещений и сообщений, и многое другое.


Особую роль в обмене играет канал связи как средство
передачи данных от клиента серверу и обратно. Как прави-
ло, это обобщается словом «сеть» — кабели, коммутаторы,
Wi-Fi-модули и т. д. Однако канал связи накладывает опре-
деленные ограничения на взаимодействие клиента и сервера.
Например, канал не позволяет передавать произвольные
символы, а требует их преобразования в специальный
вид — транспортную кодировку.

Если ввести в гугл слово на кирилице, то в адресной строке можно увидеть следующее:

    https://www.google.com.ua/?q=%D0%B0%D0%BA%D0%B0%....

Это и есть транспортное кодирование, необходимое
для канала связи. Обычно, кодирование совершает сам
браузер и нам дополнительных действий для кодирования совершать не нужно. Тем не менее, помнить об этом
надо тогда, когда мы встраиваем ссылки в наш сайт. Их
желательно сразу создавать в кодированной форме, чтобы
упредить возможные ошибки передачи данных.

## Что такое форма.

Это механизм автоматизированной отправки данных,
введенных пользователем, на серверную сторону сайта.

Группа элементов интерфейса может быть привязана
к форме при помощи средств разметки HTML и отправлена на сервер, будучи обработанной и декодированной
автоматически, без необходимости вмешательства в эти
процессы со стороны разработчика.
Создается форма тегом <form>, закрывающий тег
</form> обязателен.

### Атрибуты формы

Соответственно своему предназначению, форма должна обеспечивать отправку данных на сервер.\

Имя адресата задается атрибутом формы action:


    <form action="add_user.php">

Вторым важным атрибутом формы является метод
(или способ) отправки сообщения серверу.

Существует несколько методов HEAD OPTIONS PUT POST PATCH GET DELETE.

Поскольку формы являются упрощенным способом
автоматизированной доставки данных на сервер, для них
доступны лишь два метода запроса — GET и POST. Для
реализации других методов необходимо создавать собственные функции для отправки сообщений на серверы.

С указанием метода, объявление формы будет выглядеть как 

    <form action="add_user.php"method="GET">

Если action оставить пустым (action=''). В таком случае данные будут передаваться по тому же адресу, по которому создана форма.

Согласно спецификации желательно большими буквами, хотя HTML к регистру равнодушен.

Различие между методами GET и POST заключается
в следующем. 

Метод GET включает данные в состав URI (в адресную строку).

И выглядит как

    example.itstep.org?А=1&В=2

Данные, передаваемые POST, включаются в тело сообщения и адресная строка в браузере не меняется.

Передача параметров пользователю непосредственно не
видна. Однако, если страница построена с применением
POST-данных, то есть страница появилась после отправки
формы, то обновление страницы потребует повторной
передачи тех же параметров. Пользователь получит предупреждение: 


![start page]({path-to-subject}/images/2.png)

С GET-данными такой проблемы не возникает, т.к.
данные автоматически передаются из самой адресной
строки.

Форм на одной странице может быть несколько. У каждой может быть свой метод и свой адресат. Для работы
с формами при помощи JavaScript, объект document имеет
специальную коллекцию (массив) document.forms.

Например, если на
данной HTML-странице размещено две формы, то в коллекции document.forms будет два элемента (document.
forms[0] и document.forms[1])

Порядок форм в коллекции соответствует
порядку из объявления в HTML-коде.
	
Следует отметить, что не все то, что содержит форма,
считается ее элементами. К ним не относятся «статические»
объекты HTML — надписи, рисунки, блоки и т.д. Поэтому чтобы их отличать есть две коллекции.

- коллекция elements содержит только элементы формы;

- коллекция children — все дочерние объекты.

Большинство элементов формы создаются тегом input
и отличаются различными значениями атрибута type.

**button** - кнопка

**text** - текстовое поле

**checkbox** - флажок выбора

**radio** - радио-кнопка

**file** - диалог открытия файла

**submit** - кнопка отправки формы

**password** - ввод пароля

**number** - ввод числа

**select**  - выпадающий список

**textarea** - многострочный текст

**date**  - дата

![start page]({path-to-subject}/images/3.png)

Пример формы.

    <!DOCTYPE HTML>
    <html>
        <head>
            <meta http-equiv="Content-Type"
            content="text/html; charset=UTF-8">
            <title>Phone book</title>
            <style>
            body{font-family:"Courier New",
            Courier, monospace;}
            </style>
        </head>
    <body>
        <h2>Add new contact</h2>
            <form method='GET'>
                <b>Name</b>
                <input type="text" placeholder="Enter name"/>
                <br/><br/>
                <input type="submit" value="Save"/>
                <input type="button" value="One more phone"
                onclick="add_click()"
                style="margin-left:50px" />
                <br/><br/>
                Phone number
                <input type="text" name="phone" id="ph"
                placeholder="Enter phone number" />
                Phone type
                <select name="type">
                    <option value="1" selected>Cellular</option>
                    <option value="2">Home</option>
                    <option value="3">Work</option>
                </select>
                Priority
                <input type="radio" name="main"
                value="1" checked />
            </form>
        </body>
    </html>

![start page]({path-to-subject}/images/4.png)

Создадим базу данных с вопросами db.json в корне проекта.

    [

            {
                "question": "Как вас зовут?",
                "type": "text",
                "name": "question1"
            },

            {
                "question": "Кто победил в ВОВ?",
                "type": "radio",
                "name": "question2",
                "answers": [
                              {"text": "CCCР", "is_valid": true },
                              {"text": "США", "is_valid": false }
                           ]
            },
            {
                "question": "Есть ли бог на свете?",
                "type": "select",
                "name": "question3",
                "answers": [
                              {"text": "Да", "is_valid": true },
                              {"text": "Нет", "is_valid": false },
                              {"text": "Наука не в курсе дела", "is_valid": false }
                           ]
            },

            {
                "question": "Любимое животное",
                "type": "checkbox",
                "name": "question4",
                "answers": [
                              {"text": "Кот" },
                              {"text": "Собака барабака"},
                              {"text": "Конь"}
                           ]
            }


        ]

Затащим базу запросом в приложении.

## AJAX запросы в JQuery

[способ 1](https://api.jquery.com/jquery.ajax/)

    $.ajax({
        url: "bd.json",
        complete: (responce)=>{
            console.log(responce);
        }
      });


![start page]({path-to-subject}/images/5.png)

Заберем текст ответа и конвертируем его в объект массива.


    $.ajax({
        url: "bd.json",
        complete: (responce)=>{
            
            var data = JSON.parse(responce.responseText);
            console.log(data);

        }
    });

Создадим обьект приложения и переместим туда базу данных.



    app = {
        db: null,
        init: function() {
            $.ajax({
                url: "bd.json",
                complete: (responce)=>{
                    
                    var data = JSON.parse(responce.responseText);
                    this.db = data
                    console.log(this);
            
                }
            });
        }
    }

    app.init();

Обратите внимания, что внутри объекта в методе init мы не используем стрелочную функцию чтобы не потерять контекст this.

Создадим в шабоне тег для содержимого приложения.

    <div id="appTag"></div>

Добавим в метод init получение этого элемента.

    ...
    appTag: null,
    init: function() {
        this.appTag = $('#appTag');
    ...

Добавим текстовое поле.

        for (let item of this.db) {
            if(item.type === 'text') {
                this.appTag.append($('<input type="text" name="text" />'))
            }
        }

Добавим вопрос и сделаем переменную наборного поля.

        if(item.type === 'text') {
            let field = $('<div class="field"></div>');
            field.append($(`<span>${item.question}</span>`));
            field.append($('<input type="text" name="text" />'));
            this.appTag.append(field);
        }

Добавим поле radio.

        if(item.type === 'radio') {
            let field = $('<div class="field"></div>');
            field.append($(`<span>${item.question}</span>`));
            for (let r of item.answers) {
                field.append($(`<span>${r.text}</span>`))
                field.append($(`<input type="radio" name="${item.name}" />`));
            }
            this.appTag.append(field);
        }

Добавим поле select.

            if(item.type === 'select') {
                let field = $('<div class="field"></div>');
                field.append($(`<span>${item.question}</span>`));
                let select = $(`<select name="${item.name}">${item.question}</select>`);

                for (let r of item.answers) {
                    select.append($(`<option>${r.text}</option>`))
                   
                }
                field.append(select);
                this.appTag.append(field);
            }

Добавим поле checkbox.

            if(item.type === 'checkbox') {
                let field = $('<div class="field"></div>');
                field.append($(`<span>${item.question}</span>`));
                for (let r of item.answers) {
                    field.append($(`<span>${r.text}</span>`))
                    field.append($(`<input type="checkbox" name="${item.name}" />`));
                }
                this.appTag.append(field);
            }

![start page]({path-to-subject}/images/6.png)


