## Фронтенд. Приложение "Викторина" на ReactJs.

Клонируем шаблон.

    git clone git@github.com:zdimon/marafon-js-quiz-template.git

Создаем приложение.

    npx create-react-app my-app --template typescript
    
Эта команда создаст простейшее приложение и установит в него все зависимости.

Запуск веб сервера приложения.

    npm run start
    
Копируем все из шаблона в папку public c заменой index.html.

![start page]({path-to-subject}/images/2.png)

Ошибка появляется из за того, что теперь в index.html отсутствует элемент, к которому привязывается React.

Закоментарим запуск приложения по умолчанию.

    // ReactDOM.render(
    //   <React.StrictMode>
    //     <App />
    //   </React.StrictMode>,
    //   document.getElementById('root')
    // );


Запускаем сервер

    npm run startу
    
В React все состоит из программных компонентов, которые привязываются к тегам страницы. 
    
Создаем компонент Question в новой папке components.

### Question.tsx

    import React from 'react';


    export function Question() {
      return (
        <div className="question">
          Test question
        </div>
      );
    }


Привяжем компонент к диву в index.tsx.

    import {Question} from './components/Question';

    ReactDOM.render(
      <React.StrictMode>
        <Question />
      </React.StrictMode>,
      document.getElementById('#currentQuestionBlock')
    );
    

Создадим компонент формы.

### components/LoginForm.tsx


    import React from 'react';


    export function LoginForm() {
      return (
        <div className="chat-start">
          Как вас зовут?
          <input type="text" className="round" />
          <button id="chat-start" className="btn bg-white mt-3">Начать!</button>
        </div>
      );
    }

Привяжем к элементу.

    ...
    import {LoginForm} from './components/LoginForm';

    ...

    ReactDOM.render(
        <React.StrictMode>
          <LoginForm />
        </React.StrictMode>,
        document.getElementById('#loginForm')
      );
  
Создадим условие, где проверим залогиненность.

    if(sessionStorage.getItem('username')) { 
        ReactDOM.render(
            <React.StrictMode>
              <Question />
            </React.StrictMode>,
            document.getElementById('#currentQuestionBlock')
          );
    } else {
        ReactDOM.render(
            <React.StrictMode>
              <LoginForm />
            </React.StrictMode>,
            document.getElementById('#loginForm')
          );
    }

Создадим сервис, генерирующий запросы на сервер.

Установим библиотеку для http запросов.

    npm install axios  --save

Создаем класс в Request.ts

    import axios from "axios";

    const serverUrl = 'http://localhost:7777/v1/quiz/';

    export class Request {

        async get(url: string) {
            let response = await axios.get(`${serverUrl}${url}`)
            return response.data;
        }
    }

axios в своей работе использует промисы.
  
Существует специальный синтаксис для работы с промисами, который называется «async/await».

У слова async один простой смысл: эта функция всегда возвращает промис. Значения других типов оборачиваются в завершившийся успешно промис автоматически.

**await axios.get()** - запустит запрос и не пойдет дальше по коду пока он не завершится.
    
## Используем в компоненте формы LoginForm.

Сделаем AJAX-запрос в событии компонента componentDidMount. 

В компоненте могут присуствовать состояния - это те данные, которые меняются по мере событий приложения.

Для того, чтобы эти данные определить и менять, есть функция useState.

Эта функция возвращает переменную состояния и функцию для его изменения (т.к. состояние никогда не меняется напрямую через переменную присвоением).

Т.е. когда получим данные с сервера мы должны вызвать setState, чтобы передать их компоненту.

При получении данных с сервера мы должны убедится что на этот момент компонент существует в DOM.

Для того, чтобы подвязатся к моменту монтирования компонента используем хук useEffect

Хук useEffect представляет собой совокупность методов componentDidMount, componentDidUpdate, и componentWillUnmount.

### Создание компонента одного стикера.

Так как мы планируем выводить стикеры в цикле удобней под них создать отдельный компонент и передать в него стикер свойством (props).

    import React from 'react';
    import { useState } from 'react';

    export function Sticker(props: any) {
        const [current, setCurrent] = useState(0);
        return (
            <img 
            width="50" 
            alt=""
            src={props.item.get_url}
            />
        )

    }
    
** Sticker(props: any)** - тут мы говорим о том что в компонент зайдут данные.

Отработаем клик на стикере и установим текущий стикер в виде переменной-состояния current.

    import React from 'react';
    import { useState } from 'react';

    export function Sticker(props: any) {
        const [current, setCurrent] = useState(0);
        const select = (id: number) => {
            setCurrent(id);
        }
        return (
            <img 
            width="50" 
            className={` ${props.item.id===current ? 'sticker-active': ''} `}
            alt=""
            onClick={() => select(props.item.id)}
            src={props.item.get_url}
            />
        )

    }

### LoginForm запрос стикеров с сервера.

    import React, { useState, useEffect } from 'react';

    import { Request } from '../Request';
    import {Sticker} from './Sticker';
     

    export function LoginForm() {
      const [stickers, setStickers] = useState([]);
      useEffect(() => {
        let req = new Request();
        req.get('sticker/list').then((data) => {
           setStickers(data);
        })
       },[]);
      return (
        <div className="login-form">
          <p>Как вас зовут?</p>
          <p><input type="text" className="round" /></p>
          <div className="stickers" >
              { stickers.map((el,index) =>  <Sticker key={index} item={el} />) }
          </div>
          <button id="chat-start" className="btn bg-white mt-3">Начать!</button>
        </div>
      );
    }
    
При использовании useEffect нужно передать пустой массив вторым параметром для избежания рекурсии т.к. иначе это будет срабатывать при каждых изменениях стейта.

    useEffect(() => {},[]);
    
Добавим запрос на сервер для получения текущего вопроса в компоненте Question.tsx

    import React from 'react';
    import { Request } from '../Request';
    import { useState, useEffect } from 'react';

    export function Question() {
      const req = new Request();
      const [question, setQuestion] = useState({
        question: '',
        answers: ''
      });
      useEffect(() => {
        req.get('get_current_question').then((data) => {
          setQuestion(data);
        })
      },[]);
      return (
        <div className="question">
          {question.question} ({question.answers})
        </div>
      );
    }

TODO: Формат сообщения тут неплхо оформить в виде интерфейса.

    useState({
            question: '',
            answers: ''
          });

![start page]({path-to-subject}/images/3.png)


Далее нам нужно отработать клик по стикеру и передать его из компонента Sticker в компонент LoginForm.

Для этого определим обработчик клика в Sticker.ts

    import React from 'react';


    export function Sticker(props:any) {

      var select = (id: number) => {
        props.onSelectSticker(id); 
      }
      return (
        <img width="50" 
        onClick={() => select(props.item.id)} 
        src={props.item.get_url} />
      );
    }

И прокинем обработчик через props из родительского компонента в Sticker.

    ...
    export function LoginForm() {
      ...
      const [sticker, setSticker] = useState(0);
      ...
       var handleSelectSticker = (id: number) => {
          setSticker(id);
       }
      return (
        ...
          <div className="stickers">        
          { 
           stickers.map((el, key) => 
          <Sticker 
             onSelectSticker={handleSelectSticker} 
             item={el} 
             key={key}
          />)
         }
         ...

Добавим state для имени пользователя и привяжем его к изменению input-а при помощи обработчика handleChangeUsername.

    export function LoginForm() {
      ...
      const [username, setUsername] = useState('');

      var handleChangeUsername = (evt:any) => {
        setUsername(evt.target.value);
      }

       ...
      
      <input onChange={handleChangeUsername} type="text" className="round" />
      
      
## Отправляем сообщение на сервер.

Создадим компонент формы отправки MessageForm.ts.



    import React, {useState} from 'react';
    import { Request } from '../Request';

    export function MessageForm() {
      const req = new Request();
      const [message, setMessage] = useState('');
      var handleChangeMessage = (evt:any) => {
        setMessage(evt.target.value);
      }

      var submit = () => {
          let data = {
              message: message,
              playername: localStorage.getItem('username')
          }
          req.post('save_message', data).then((data) => {
            setMessage('');
         })
      }
      return (
        <>
        <input 
            type="text" 
            className="form-control mr-3" 
            placeholder="Введите ответ на вопрос"
            defaultValue={message}
            onChange={handleChangeMessage}
        />
        <button onClick={submit} type="submit" className="btn btn-primary d-flex align-items-center p-2"><i className="fa fa-paper-plane-o" aria-hidden="true"></i><span className="d-none d-lg-block ml-1">Send</span></button>
        </>
      );
    }



## Сокет соединение.

Нам теперь необходимо установить сокет-соединение.

Для этого создадим класс соединения SocketConnection.ts и определим обработчики основных событий в его конструкторе.


    export class SocketConnection {
       timer:any = null;
       websocket:any = null;
       constructor() {
        
        this.wsConnect();
       }

       wsConnect() {
        clearInterval(this.timer);
        this.websocket = new WebSocket('ws://quizapi.webmonstr.com:7777/quiz/');

        this.websocket.onerror = (evt: any) => {
            this.timer = setTimeout(() => this.wsConnect(),2000);
        }

        this.websocket.onmessage = (message: any) => {
            var message = JSON.parse(message.data)
            console.log(message);
        }

        this.websocket.onclose =  (event: any) => {
            console.log('Close connection');
            this.timer = setTimeout(() => this.wsConnect(),2000);
        };
       }
    }

## События.

Нам необходимо отслеживать приход сообщений по сокетам в разных компонентах.

Для этого удобней всего генерировать события и подписываться на них в компонентах.

В этом класе мы будем использовать библиотеку RxJS и ее изструмен Subject.

[ссылка на документацию](https://www.learnrxjs.io/learn-rxjs/subjects/subject)

Установим 

    npm install rxjs @types/rx --save
    
Применим и запустим событие при приходе сообщения.

    ...
    import { Subject } from 'rxjs';
    ...
    export class SocketConnection {
       ...
       newMessage$ = new Subject();
       ...

        this.websocket.onmessage = (message: any) => {
            var message = JSON.parse(message.data)
            this.newMessage$.next(message);
        }
        
Однкако теперь нужно решить проблебу множественных экземпляров этого класса.

Применим паттерн singletone.

    export class SocketConnection {
       private static instance: SocketConnection;
       ...
       public static getInstance(): SocketConnection {
            if (!SocketConnection.instance) {
                SocketConnection.instance = new SocketConnection();
            }
            return SocketConnection.instance;
        }

Теперь будем создавать этот объект через метод getInstance и он будет всегда в единственном экземпляре.

    import { SocketConnection } from '../SocketConnection';

    const socket = SocketConnection.getInstance();

Подпишемся на это событие в компоненте Question.

      
    import { SocketConnection } from '../SocketConnection';


    export function Question() {
      const req = new Request();
      const socket = SocketConnection.getInstance();
      socket.newMessage$.subscribe((data: any) => {
        console.log(data);
      });

Однако при этом мы наблюдаем 4 реакции на одно событие.

![start page]({path-to-subject}/images/4.png)

Проблема в том, что функция реакт компонента запускается по многу раз.

Чтобы что то выстрелило один раз, нужно завернуть это в хук useEffect.

Сделаем это и запросим новый вопрос с сервера.

    ...
    export function Question(props: any) {
      useEffect(() => {
        socket.sendMessage$.subscribe((data: any) => {
          if(data.is_right) {
              let req = new Request();
              req.get('get_current_question').then((data) => {
                setQuestion(data);
                console.log(data);
                });
              }
          });
      },[])
      ...
      
Создадим компонент сообщения Message.tsx.

    import React from 'react';

    export function Message(props: any) {

      return (

        <div className={`chat ${props.message.is_right ? "chat-left" : ""}`}>
        <div className="chat-user">
           <a className="avatar m-0">
              <img src="images/user/1.jpg" alt="avatar" className="avatar-35 " />
           </a>
      <span className="chat-time mt-1">{props.message.playername}</span>
        </div>
        <div className="chat-detail">
           <div className="chat-message">
              <p>{ props.message.text } {props.message.is_right}</p>
           </div>
        </div>
      </div>
      );
    }

      
Создадим компонент списка сообщений MessageBox.tsx.

Отработаем сообщение прихода нового ответа.

    import React from 'react';
    import { Request } from '../Request';
    import { useState, useEffect } from 'react';
    import { SocketConnection } from '../SocketConnection';
    import { Message } from './Message';


    const socket = SocketConnection.getInstance();

    export function MessageBox(props: any) {
      useEffect(() => {
        socket.newMessage$.subscribe((payload: any) => {
            // const msg = [...messages] as any;
            // msg.push(payload);
            // setMessages(msg);
            const req = new Request();
            req.get('message/list').then((data) => {
                setMessages(data);
            })
          });
      },[])

      const [messages, setMessages] = useState([]);
      useEffect(() => {
        const req = new Request();
        req.get('message/list').then((data) => {
            setMessages(data);
            console.log(data);
        })
      },[]);
      return (
        <div className="messages">
          { messages.map((el, key) => <Message key={key} message={el} />) }
        </div>
      );
    }

Компонент текущего пользователя CurrentPlayer.tsx.

        import React from 'react';
        import { useState, useEffect } from 'react';


        export function CurrentPlayer(props: any) {
          const [image, setImage] = useState('');
          useEffect(() => {
            setImage(localStorage.getItem('image') as string);
          },[]);
          return (
            <>
            <div className="avatar chat-user-profile m-0 mr-3">
                <img 
                src={image}
                alt="avatar" 
                className="avatar-50 " />
            </div>
          <h5 className="mb-0">{localStorage.getItem('username')}</h5>
          &nbsp;<h5 className="player-account"> Правильных ответов: {localStorage.getItem('account')}</h5>
            </>
          );
    }

Компонент списка участников PlayerList.tsx.



   





