## Многопроектное приложение.

### Инструмент create-react-app

Глобальная установка.

    sudo yarn global add create-react-app

## Старт приложения React   

    npx create-react-app my-app

или 

    create-react-app my-app

если установили глобально

### Иструмен storybook

Позволяет изолировать компоненты и вести работу над каждым независимо.

Установка глобально командного менеджера

    yarn global add @storybook/cli

Теперь внутри my-app запускаем инициализацию storybook

    getstorybook init

Эта команда определяет тип проекта, делает необходимые проверки и устанавливает зависимости.

## Запуск сервера.

    yarn storybook

или

    npm run storybook

Эта штука будет отслеживать все изменения в файлах компонентов и пересобирать их.

Сборка под продакшин.

    yarn build-storybook

или

    npm run build-storybook



