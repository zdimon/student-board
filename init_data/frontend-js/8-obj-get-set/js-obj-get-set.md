## Дескрипторы свойств.


Мы рассмотрим возможности, которые позволяют очень гибко и мощно управлять всеми свойствами объекта, включая их аспекты – изменяемость, видимость в цикле for..in и даже незаметно делать их функциями.

Основной метод для управления свойствами – **Object.defineProperty**.

Он позволяет объявить свойство объекта и, что самое главное, тонко настроить его особые аспекты, которые никак иначе не изменить.

Синтаксис:

    Object.defineProperty(obj, prop, descriptor)

**obj** - Объект, в котором объявляется свойство.

**prop** - Имя свойства, которое нужно объявить или модифицировать.

**descriptor** - Дескриптор – объект, который описывает поведение свойства.


В нём могут быть следующие поля:

**value** – значение свойства, по умолчанию undefined

**writable** – значение свойства можно менять, если true. По умолчанию false.

**configurable** – если true, то свойство можно удалять, а также менять его в дальнейшем при помощи новых вызовов defineProperty. По умолчанию false.

**enumerable** – если true, то свойство просматривается в цикле for..in и методе Object.keys(). По умолчанию false.

**get** – функция, которая возвращает значение свойства. По умолчанию undefined.

**set** – функция, которая записывает значение свойства. По умолчанию undefined.

Чтобы избежать конфликта, запрещено одновременно указывать значение value и функции get/set.

## Обычное свойство

    var user = {};

    // 1. простое присваивание
    user.name = "Вася";

    // 2. указание значения через дескриптор
    Object.defineProperty(user, "name", { value: "Вася", configurable: true, writable: true, enumerable: true });


Для того, чтобы сделать свойство неизменяемым, изменим его флаги writable и configurable:

    "use strict";

    var user = {};

    Object.defineProperty(user, "name", {
      value: "Вася",
      writable: false, // запретить присвоение "user.name="
      configurable: false // запретить удаление "delete user.name"
    });

    // Теперь попытаемся изменить это свойство.

    // в strict mode присвоение "user.name=" вызовет ошибку
    user.name = "Петя";


Свойство-функция
Дескриптор позволяет задать свойство, которое на самом деле работает как функция. Для этого в нём нужно указать эту функцию в get.


    var user = {
      firstName: "Вася",
      surname: "Петров"
    }

    Object.defineProperty(user, "fullName", {
      get: function() {
        return this.firstName + ' ' + this.surname;
      }
    });

    alert(user.fullName); // Вася Петров

Также можно указать функцию, которая используется для записи значения, при помощи дескриптора set.

    var user = {
      firstName: "Вася",
      surname: "Петров"
    }

    Object.defineProperty(user, "fullName", {

      get: function() {
        return this.firstName + ' ' + this.surname;
      },

      set: function(value) {
          var split = value.split(' ');
          this.firstName = split[0];
          this.surname = split[1];
        }
    });

    user.fullName = "Петя Иванов";
    alert( user.firstName ); // Петя
    alert( user.surname ); // Иванов


## Указание get/set в литералах

Если мы создаём объект при помощи синтаксиса { ... }, то задать свойства-функции можно прямо в его определении.

Для этого используется особый синтаксис: get свойство или set свойство.


    var user = {
      firstName: "Вася",
      surname: "Петров",

      get fullName() {
        return this.firstName + ' ' + this.surname;
      },

      set fullName(value) {
        var split = value.split(' ');
        this.firstName = split[0];
        this.surname = split[1];
      }
    };

    alert( user.fullName ); // Вася Петров (из геттера)

    user.fullName = "Петя Иванов";
    alert( user.firstName ); // Петя  (поставил сеттер)
    alert( user.surname ); // Иванов (поставил сеттер)





