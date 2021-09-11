# Вызов пользователя в чат.
     
Для эмуляции вызова одним пользователем другого сделаем еще одну страницу для пользователя, принимающего вызов.

Он будет иметь форму для установки соединения под заданным логином.

Вызывающий должен будет ввести имя вызываемого в отдельном поле input.

Формируем запрос на сервер при нажатии кнопки.

        <div>
            <input type="text" id="CallUsername" />
            <button value="woman" id="callButton">Calling</button>
        </div>

        <script>

        $('#callButton').on('click', (e) => {
            let url = 'http://localhost:8181/call';
            $.ajax({
                url: url,
                type: "POST",
                data: JSON.stringify({
                    "login": $('#CallUsername').val(),
                    "sid": window.sessionStorage.getItem('sid')
                }),
                contentType: "application/json",
                success: (data) => {
                    console.log(data);
                },
            });
        });

        ...

## Использование с Typescript

    import { config } from './config';
    ...
     

    export default class App {

       ...

        callUser() {
            const url = `${config.serverURL}/call`;
            $.ajax({
                url,
                type: "POST",
                data: JSON.stringify({
                    login: $('#CallUsername').val(),
                    sid: window.sessionStorage.getItem('sid')
                }),
                contentType: "application/json",
                success: (response: any) => {
                    console.log(response);
                }
            }); 
        }

Файл настроек config.ts

    export const config = {
        serverURL: 'http:/localhost:8888/'
    }


Запрос уходит на 404 Not Found

Создадим вьюху под него.


    @swagger_auto_schema(
        request_body=CallRequestSerializer
    )
    class CallView(APIView):
        """
           Call request.

        """
        permission_classes = (AllowAny,)

        @swagger_auto_schema(
            request_body=CallRequestSerializer
        )
        def post(self, request, format=None):
            return Response({'call': 'ok'})

Простенький класс серилизатора.

    from rest_framework import serializers


    class CallRequestSerializer(serializers.Serializer):
        login = serializers.CharField()
        sid = serializers.CharField()

И подвяжем к роутингу в app/urls.py.

    ...
    path('call', CallView.as_view()),
    ...

Класс для отключения проверки подписи

    class DisableCSRFMiddleware(object):

        def __init__(self, get_response):
            self.get_response = get_response

        def __call__(self, request):
            setattr(request, '_dont_enforce_csrf_checks', True)
            response = self.get_response(request)
            return response

Использование.

    MIDDLEWARE = [
        ...
        # 'django.middleware.csrf.CsrfViewMiddleware',
        'dj_app.csrf_middleware.DisableCSRFMiddleware',
        ...
    ]


Первым делом проверим, если ли такие пользователи у нас в БД.

Будем проверять вызываемого по логину и вызывающего по идентификатору веб-сокет соединения (SID).

    ....

    def post(self, request, format=None):
        data = json.loads(request.body)
        try:
            callee = UserProfile.objects.get(login=data['login'])
            print(callee)
        except ObjectDoesNotExist:
            return Response({'status': 1, 'message': 'User does not connected!'})

        try:
            conn = UserConnection.objects.get(sid=data['sid'])
            caller = conn.user
            print(caller)
        except ObjectDoesNotExist:
            return Response({'status': 1, 'message': 'You are not connected!'})

        return Response({'call': 'ok'})

Результат.

![start page]({path-to-subject}/images/13.png)

Далее создадим задачу для celery в которой потом будем рассылать веб-сокет сообщение на все соединения того, которого вызывают.

Задачу создадим в новом вайле tasks.py


    from celery.decorators import task


    @task()
    def call_task(caller_id,callee_id):
        print('----Calling----- %s to %s' % (caller_id,callee_id))

Тут мы декорируем функцию как задачу и принимаем два индентификатора вызывающего и вызываемого пользователя.


Теперь положим эту задачу в очередь селери из нашей вьюхи при помощи функции delay().

    class CallView(APIView):
        ...
        def post(self, request, format=None):
            ...

            call_task.delay(caller.id,callee.id)


![start page]({path-to-subject}/images/14.png)

Таким образом задача перейдет на исполнение в отдельный поток и не будет тормозить HTTP запрос.

Не нужно забывать перезапускать процесс селери при каждом изменении кода задач.

В случае использования докер контейнеров их необходимо перезапустить.

Теперь в задаче пошлем сообщения вызываемому на его сокет соединения.

    from celery.decorators import task
    import socketio   
    from django.conf import settings
    from .models import UserConnection, UserProfile
    mgr = socketio.RedisManager(f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0')

    @task()
    def call_task(caller_id, callee_id):
        caller = UserProfile.objects.get(pk=caller_id)
        callee = UserProfile.objects.get(pk=callee_id)
        for con in UserConnection.objects.filter(user=callee):
            payload = {"login": caller.login}
            mgr.emit('calling', data=payload, room=con.sid)

Отреагируем на приход на клиентском js.

        socket.on('calling', (msg) => {
            $('#calleeName').val(msg.login);
            $('#acceptDiv').show();
        });

Мы отображаем div с кнопками принятия или отказа.

Так же заполняем поле input с логином вызывающего чтобы потом передать на сервер.

    <div id="acceptDiv" style="display: none">
        Reciever login:<input type="text" id="calleeName" />
        <video autoplay="true" width="200" id="myVideo"></video>
        <button id="acceptButton">Accept</button>
        <button id="declineButton">Decline</button>
    </div>

Создадим два ендпоинта для принятия и отклонения запроса.


    @swagger_auto_schema(
        request_body=CallRequestSerializer
    )
    class AcceptView(APIView):
        """
           Accept a call.

        """
        permission_classes = (AllowAny,)

        @swagger_auto_schema(
            request_body=AcceptDeclineRequestSerializer
        )
        def post(self, request, format=None):
            data = json.loads(request.body)
            return Response({'call': 'ok'})


    @swagger_auto_schema(
        request_body=CallRequestSerializer
    )
    class DeclineView(APIView):
        """
           Decline a call.

        """
        permission_classes = (AllowAny,)

        @swagger_auto_schema(
            request_body=AcceptDeclineRequestSerializer
        )
        def post(self, request, format=None):
            data = json.loads(request.body)
            return Response({'call': 'ok'})


И серилизатор для входных данных с одним логином.


    class AcceptDeclineRequestSerializer(serializers.Serializer):
        login = serializers.CharField()

### Отработка согласия на соединение.

При согласии мы должны передать объект Offer на сервер и сохранить его в таблице Sdp.

Изменим модель таблицы следующим образом.

    class Sdp(models.Model):
        from_user = models.ForeignKey(UserProfile, 
                                      on_delete=models.CASCADE, 
                                      related_name='from_user',
                                      null= True,
                                      blank=True)
        from_user_sdp = models.TextField(verbose_name=_('Broadcast Offer'))

        to_user = models.ForeignKey(UserProfile, 
                                    on_delete=models.CASCADE, 
                                    related_name='to_user',
                                    null=True,
                                    blank=True)
        to_user_sdp = models.TextField(verbose_name=_('Recieve Offer'))


В этой таблице мы будем хранить ссылки на 2-х пользователей, того кто транслирует видео и того кто его принимает.

Соответственно для каждого так же будем хранить объект offer.

В процессе установки соединения каждый из пользователей должен будет установить свой и чужой Offer в js объект соединения, но позиции будут разными в зависимости от того кто транслирует видео, а кто принимает.

Условно их можно назвать RemoteOffer и LocalOffer.

Поэтому в серилизаторе мы определим поле type.


    from rest_framework import serializers


    class OfferRequestSerializer(serializers.Serializer):
        sid = serializers.CharField()
        type = serializers.CharField()
        offer = serializers.CharField()


В этом поле будем передавать значения request или response в зависимости от того, кто его запрашивает.

request - когда запрашивает передающая видео сторона и передает свой Offer, который у нее установлен в LocalOffer

response - когда принимающая сторона уже получила от передающей Offer, поставила его в RemoteOffer, сформировала свой Offer, поставила в позицию  LocalOffer и посылает свой обратно для того чтобы передающая видео сторона установила его в свой  RemoteOffer.


По сути класс Sdp будет содержать один видеопоток, передающийся между двумя пользователями.

У одного from_user_sdp будет в LocalOffer а to_user_sdp в RemoteOffer, у другого - наоботот.

Перепишем запрос сохранения Offer с учетом того, кто этот запрос вызывает.

    class OfferView(APIView):
        """
           Get offer from abonent after click Show cam button.

        """
        permission_classes = (AllowAny,)

        @swagger_auto_schema(
            request_body=OfferRequestSerializer
        )
        def post(self, request, format=None):
            payload = request.data
            conn = UserConnection.objects.get(sid=payload['sid'])
            offer = Sdp()
            # устанавливаем Offer для передающего и уведомляем принимающую сторону
            if payload['type'] == 'sender':
                # найдем принимающего по переданному логину
                try:
                    reciever = UserProfile.objects.get(login=payload['reciever_login'])
                except ObjectDoesNotExist:
                    Response({'status': 1, 'message': f'Reciever does not exist!'})

                offer.from_user = conn.user
                offer.from_user_sdp = payload['offer']
                offer.to_user = reciever
                # уведомляем принимающую сторону через задачу для celery
                sender_offer_task(conn.user.id, reciever.id, payload['offer'])
            # устанавливаем Offer для принимающего
            else:
                offer.to_user = conn.user
                offer.to_user_sdp = payload['offer']
            offer.save()
            return Response({'offer': 'ok'})



На фронтенде при подтверждении звонка на стороне передающего поток мы выполняем следующие действия.

1. Посылаем запрос на сервер о том что абонент принял предложение.

        $('#acceptButton').on('click', accept);
        function accept(e) {
          
           let url = '{{server_name}}/accept';
           $.ajax({
                type: "POST",
                url: url,
                data: JSON.stringify({
                    'login': window.sessionStorage.getItem('sid'),
                }),
                contentType: "application/json",
                success: (data) => {
                    console.log(data);
                    initVideoStream();
                }
            });

        }

2. После чего вызываем функцию initVideoStream() для захвата видео в асинхронном режиме.

        const constraints = window.constraints = {
            audio: false,
            video: true
        };


        async function initVideoStream(e) {
            try {
                const stream = await navigator.mediaDevices.getUserMedia(constraints);
                handleSuccessInitVideo(stream);
            } catch (e) {
                console.log(e);
            }
        }

3. После захвата вызываем  handleSuccessInitVideo(stream) где присоединаяем видеопоток к html элементу video и потом вызываем offer() и передаем ему поток и дорожки.


        function handleSuccessInitVideo(stream) {
            const video = document.querySelector('#myVideo');
            const videoTracks = stream.getVideoTracks();
            console.log('Got stream with constraints:', constraints);
            console.log(`Using video device: ${videoTracks[0].label}`);
            window.stream = stream; // make variable available to browser console
            video.srcObject = stream;
            offer(videoTracks, stream);
        }

4. Формируем объект Offer, устанавливаем его в setLocalDescription  и передаем на сервер.

        const offerOptions = {
            offerToReceiveAudio: 0,
            offerToReceiveVideo: 1,
            iceRestart: 1,
            voiceActivityDetection: 0
        };

        async function offer(tracks,localStream) {
           const peerConnection = window.peerConnection = new RTCPeerConnection(null);
           tracks.forEach(track => window.peerConnection.addTrack(track, localStream));

           const offer = await peerConnection.createOffer(offerOptions);
           await peerConnection.setLocalDescription(offer);
           let url = '{{server_name}}:{{server_port}}/offer';
           $.ajax({
            type: "POST",
            url: url,
            contentType: "application/json",
            data: JSON.stringify({
                'sid': window.sessionStorage.getItem('sid'),
                'offer': JSON.stringify(offer),
                'reciever_login': $('#calleeName').val(),
                'type': 'sender'
            }),
                success: (data) => {
                    console.log(data);
                },
            });

        }

Так же мы добавляем все видеодорожки в обьект соединения.

    window.peerConnection.addTrack(track, localStream)

которые должны быть переданы клиенту на удаленный peer. Дело в том, что по сети передаются не потоки stream, а медиадорожки. Вы вправе добавить несколько дорожек из разных stream-объектов (в случае если у вас много камер и микрофонов). Функция addTrack служит для их группировки и последующей синхронизации. В нашем случае мы оперируем одним объектом stream и и группируем в нем его же дорожки. Получить текущие дорожки можно из объекта stream stream.getTracks(). 



Результат видим в админке.

![start page]({path-to-subject}/images/15.png)

И на экране.

![start page]({path-to-subject}/images/16.png)

Следующим шагом нужно уведомить принимающего поток и передать ему на клиент Offer по веб-сокету.

Для этого мы вызываем функцию celery 

    sender_offer_task(conn.user.id, reciever.id, payload['offer'])

Но в данном случае мы ее вызываем напрямую для тестирования и не предеаем celery (чтобы при разработке не перегружать постоянно контейнера).

В реальной ситуации мы бы вызвали через delay().

    sender_offer_task.delay(conn.user.id, reciever.id, payload['offer'])

Результат видим в консоле

![start page]({path-to-subject}/images/17.png)

Организуем отправку уведомления на клиентскую сторону принимающего поток - того кто вызвал в чат.

    @task()
    def sender_offer_task(sender_id, reciever_id, sender_offer):
        reciever = UserProfile.objects.get(pk=reciever_id)
        sender = UserProfile.objects.get(pk=sender_id)
        # Находим все соединения по принимающей стороне
        for conn in UserConnection.objects.filter(user=reciever):
            # отсылаем сообщения на сокет
            payload = {"sender_login": sender.login,
                       "sender_offer": sender_offer}
            mgr.emit('sender_offer', data=payload, room=conn.sid)

Отработаем приход сообщения на его клиентской стороне.

        socket.on('sender_offer', (msg) => {
            console.log('Request accepted!!!!')
            console.log(msg);
        });

![start page]({path-to-subject}/images/18.png)

