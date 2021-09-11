# Vue.js. Начало работы.

Vue не поддерживает IE8 и ниже


Старт проекта на чистом vue.

Создаем index.html

    <!DOCTYPE html>
    <html>
        <head><title>Vue start</title>
            <script src="https://cdn.jsdelivr.net/npm/vue@2/dist/vue.js"></script>
        </head>
        <body>
            <div id="app">
                {{ message }}
              </div>
            <script>
               var app = new Vue({
                el: '#app',
                data: {
                  message: 'Hello Vue!'
                }
              })
            </script>
        </body>
    </html>

Связывание атрибута тега с переменной.

        <div id="app">
            <span v-bind:title="message">
                Hover your mouse over me for a few seconds
                to see my dynamically bound title!
              </span>
          </div>
        <script>
           var app = new Vue({
            el: '#app',
            data: {
              message: 'Hello Vue!'
            }
          })
        </script>

### Двухстороннее связывание

    <input v-model="message">

### Условия

    <span v-if="seen">Now you see me</span>


### Циклы

    <li v-for="todo in todos">
      {{ todo.text }}
    </li>

### Управление событиями

    <button v-on:click="reverseMessage">Reverse Message</button>
    ...
    var app5 = new Vue({
      ...
      methods: {
        reverseMessage: function () {
          this.message = this.message.split('').reverse().join('')
        }
      }
    })

или

    @click="triggerReadMore($event)"

Старт проекта при помощи cli.

Установка.

    npm install -g @vue/cli

Старт проекта.

    vue create hello-world

Старт проекта на nuxt.

    npm init nuxt-app <project-name>

