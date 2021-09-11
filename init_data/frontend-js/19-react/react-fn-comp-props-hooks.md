# Функциональные компоненты.

## Простой компонент и его рендеринг.

LikeLink.tsx
    
    import * as React from "react";
    import * as ReactDOM from 'react-dom';

    function LikeLink() {
        return (
          <h1>Hello from react!</h1>
        );
    }

    export default LikeLink;

index.tsx

    import LikeLink from './LikeLink';
    import * as ReactDOM from 'react-dom';
    import * as React from 'react';


    ReactDOM.render(
         <LikeLink />, 
         document.getElementById('react-app')
    )

### Рендеринг нескольких элементов по классу.

    var likeLinks = document.querySelectorAll('.bd-like-button');
    likeLinks.forEach((item) => 
    {
      ReactDOM.render(
        <LikeLink />,
        item
      );
    });



## Применение колбека на событие клика.

    var doClick = (evt) => {
        console.log(evt);
    }

    function LikeLink() {
        return (
          <a onClick={doClick}>Click me</a>
        );
    }

## HTTP запросы.

    npm install axios  --save

Класс для GET запроса.

    import axios from "axios";


    export class Request {
        baseUrl = 'http://localhost:7777/v1/';
        async get(url: string) {
            let response = await axios.get(`${this.baseUrl}${url}`)
            return response.data;
        }
    }

Использование класса по событию клика.

    import * as React from "react";
    import * as ReactDOM from 'react-dom';
    import {Request} from '../libs/Request';
    var req = new Request();

    var doClick = async (evt) => {
        req.get('account/user_list').then((data) => {
            console.log(data);
        });
    }

    function LikeLink() {
        return (
          <a onClick={doClick}>Click me</a>
        );
    }
    
Вы можете сделать AJAX-запрос в componentDidMount. 

Когда вы получите данные, вызовем setState, чтобы передать их компоненту.



### Кастомизация заголовков запроса.

    export class Request {
        baseUrl = 'http://localhost:7777/v1/';
        async get(url: string) {
            let response = await axios.get(`${this.baseUrl}${url}`,{
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'blabla'
                }
            })
            return response.data;
        }
    }


## Свойства.

Переменные, объявленные внутри функции становятся доступными в JSX.

    function App() {
        const name = 'Dima';
        return (  
          <h1>Hello {name}!</h1>
        );
    }

Комбинирование компонентов и передача свойств в дочерние.

    function App() {
        const name = 'Dima';
        return (
          <>
          <h1>Hello {name} from react!!!!!!!</h1>
          <Test name={ name } />
          </>
        );
    }

    function Test(props) {
      return (
        <p>{ props.name }</p>
      );
    }

Конструкция <></> служит для создания корневого контейнета т.к. компонент должен рендерить только один тег.

## Вставка компонентов циклом.

    function App() {
        const name = 'Dima';
        const arr = [1,2,3,4];
        return (
          <>
          <h1>Hello {name} from react!!!!!!!</h1>
          {arr.map((el, i) => <Test name={name} key={i} number={i} />)}
          </>
        );
    }

    function Test(props) {
      return (
        <p>{ props.number } { props.name }</p>
      );
    }

key={i} - обязательное условие уникального ключа компонента для реакта.

## Хуки.

Позволяют использовать состояния без написания классов.

Хуки — это функции, с помощью которых вы можете «подцепиться» к состоянию и методам жизненного цикла React из функциональных компонентов. 

Хуки не работают внутри классов — они дают вам возможность использовать React без классов.


Хук состояния useState 

Возвращает 2 вещи (кортеж): начальное состояние и функцию его изменения.

Единственный аргумент useState — это начальное состояние.


Пример.

    const [count, setName] = useState(0);

Теперь мы можем использовать setName везде, чтобы изменить состояние и реакт прересует компоненты, которые его используют.

    function App() {
        const arr = [1,2,3,4];
        const [name, setName] = useState('Dima');
        var doSetName = (val) => {
          setName('Vova');
        }
        return (
          <>
          <h1>Hello {name} from react!!!!!!!</h1>
          {arr.map((el, i) => <Test name={name} key={i} number={i} />)}
          <a onClick={doSetName}>Change name</a>
          </a>
        );
    }

## Хук эффекта useEffect.

Эффект - это какоето изменение за пределами компонента.

Когда вы вызываете useEffect, React получает указание запустить вашу функцию с «эффектом» после того, как он отправил изменения в DOM. 

Поскольку эффекты объявляются внутри компонента, у них есть доступ к его пропсам и состоянию. 

По умолчанию, React запускает эффекты после каждого рендера, включая первый рендер. 


    import { useEffect } from 'react';

    function App() {

        ....

        useEffect(() => {
          // Обновляем заголовок документа, используя API браузера
          document.title = `Вас зовут ${name}`;
        });

