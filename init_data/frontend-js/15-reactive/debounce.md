## Debounce

Отменяет герерируемые элементы потока если время между ними менее указанного значения.

Сигнатура.

    signature: debounce(durationSelector: function): Observable

Пример.

    Login: <input id="inputBox" name="login" />

Привяжем поток к отпусканию клавиши.

   var box = $('#inputBox');

   var stream = Rx.Observable.fromEvent(box,'keyup');

   stream.subscribe((e) => {
       console.log(e);
   })

Отсеим те нажатия, которые возникают чаще чем раз в секунду.

   var box = $('#inputBox');

   var stream = Rx.Observable.fromEvent(box,'keyup').debounce(1000);

   stream.subscribe((e) => {
       console.log($(e.target).val());
   })



