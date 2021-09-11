
## Роутинг в реакте.

Добавим библиотеку history.

[ссылка на доку](https://github.com/ReactTraining/history/blob/28c89f4091ae9e1b0001341ea60c629674e83627/docs/navigation.md)

    npm install history @types/history --save

Добавим импорт в index.js

    import {createBrowserHistory} from 'history';

    ReactDOM.render(
      <React.StrictMode>
        <App />
      </React.StrictMode>,
      document.getElementById('root')
    );

## Библиотека react-router

[ссылка на источник](https://habr.com/ru/post/329996/)

Мы будем создавать сайт который будет отображаться в браузере, поэтому нам следует использовать react-router-dom. react-router-dom экспортирует из react-router все функции поэтому нам можно установить только react-router-dom.

Установка.

    npm install react-router @types/react-router --save
    npm install react-router-dom @types/react-router-dom --save


[ссылка на документацию](https://reactrouter.com/web/guides/quick-start)


Библиотека предоставляет такие компоненты:

Навигация по клику **(компонент <Link>)**

Перенаправление **(компонент <Redirect>)**

Маршрутизация **(компонент Route)**


Заворачиваем приложение в компонент роутера.

    // импорт компонента роутера
    import { BrowserRouter } from 'react-router-dom';

    ReactDOM.render(
      <React.StrictMode>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </React.StrictMode>,
      document.getElementById('root')
    );

Если появляется такая ошибка

![start page]({path-to-subject}/images/7.png)

Это происходит из за порядка импорта, необходимо поднять как можно выше по коду импорт.

    // импорт компонента роутера
    import { Router } from "react-router-dom"
    import {createBrowserHistory} from 'history';

Разделим приложение на ldf компонента Head и Main

    import Header from './Header';
    import Main from './Main';

    function App(props: any) {
     
      return (
        <div className="App">
          <Header />
          <Main />
        </div>
      );
    }

    export default App;

Создадим компоненты страниц Home и Chat

pages/Chat.tsx

    import React from 'react';

    function Chat(props: any) {
        
      
        return (
          <div className="Home">
              <h1>Chat component</h1>
          </div>
        );
      }

    export default Chat;

pages/Home.tsx

    import React from 'react';

    function Home(props: any) {
        
      
        return (
          <div className="Home">
              <h1>Home component</h1>
          </div>
        );
      }

    export default Home;



В Main определим маршруты.

    import React from 'react';
    import { Switch, Route, Redirect } from 'react-router-dom';

    import Home from './pages/Home';
    import Chat from './pages/Chat';

    function Main(props: any) {
        
      
        return (
          <div className="Header">
         
              <h1>Main component</h1>
              <Switch>
                <Route exact path='/home' component={Home}/>
                <Route path='/chat' component={Chat}/>
                <Redirect from='/' to='/home'/>
                </Switch>
          </div>
        );
      }

    export default Main;

Осталось создать ссылки в Head компоненте.

    import React from 'react';
    import { Link } from "react-router-dom";
    function Header(props: any) {
        
      
        return (
          <div className="Header">
                <Link className='SectionNavigation-Item Section' to='/home'>
                            Home
                </Link>
                <Link className='SectionNavigation-Item Section' to='/chat'>
                            Chat
                </Link>
          </div>
        );
      }

    export default Header;

В пропсы компонента маршрутизатор забрасывает 3 объекта.

    console.log(props);

![start page]({path-to-subject}/images/9.png)

## Дочерний роутинг.


    import ChatMain from './ChatMain';
    import ChatRoom from './ChatRoom';
    import { Link } from "react-router-dom";

    function Chat(props: any) {
        
      
        return (
          <div className="Home">
              <h1>Chat component</h1>
              <Link className='SectionNavigation-Item Section' to='/chat/main'>
                            Main
                </Link>
                <Link className='SectionNavigation-Item Section' to='/chat/room/3'>
                            Room
                </Link>
              <Switch>
                <Route exact path='/chat/main' component={ChatMain}/>
                <Route path='/chat/room/:number' component={ChatRoom}/>
                <Redirect from='/chat' to='/chat/main'/>
            </Switch>
          </div>
        );
      }

## Параметры роутинга.

Параметры можно получать из пропсов того компонента, что привязан к роуту с параметром.

![start page]({path-to-subject}/images/10.png)







