# Подвязываем REST API интерфейс.

Устанавливаем библиотеки.

    djangorestframework
    drf-yasg

## Установка swagger.

Добавляем прилагу drf_yasg в settings.py.

    INSTALLED_APPS = [
        ....
        'drf_yasg',
     ...
    ]

Пропишем роутинг в urls.py.

    from rest_framework import permissions
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi

    schema_view = get_schema_view(
        openapi.Info(
            title="API",
            default_version='v1',
            description=''' Documentation
            The `ReDoc` view can be found [here](/doc).
            ''',
            terms_of_service="https://www.google.com/policies/terms/",
            contact=openapi.Contact(email="zdimon77@gmail.com"),
            license=openapi.License(name="BSD License"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )


    urlpatterns = [
        path('test', index),
        path('admin/', admin.site.urls),
        path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('doc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-doc'),
    ]

![start page]({path-to-subject}/images/6.png)

Создадим модели для передачи SDP и ICE сообщений.

На этой диаграмме показан процесс общения двух клиентов через сигнальный сервер.

![start page]({path-to-subject}/images/7.png)

В качестве сигнального сервера мы используем веб-сокет сервер.

Создадим классы модели проведем миграцию.

    class Sdp(models.Model):
        sdp = models.TextField(verbose_name=_('Sdp'))
        conn = models.ForeignKey(UserConnection, on_delete=models.CASCADE)


    class Ice(models.Model):
        ice = models.TextField(verbose_name=_('Ice'))
        sdp = models.ForeignKey(Sdp, on_delete=models.CASCADE)


Админка.


    @admin.register(Sdp)
    class SdpAdmin(admin.ModelAdmin):
        list_display = ['conn', 'sdp']


    @admin.register(Ice)
    class IceAdmin(admin.ModelAdmin):
        list_display = ['sdp', 'ice']


## Фронтенд

Теперь на стороне клиента запросим информацию с веб камеры.

     <p>
        <video autoplay="true" width="200" id="myVideo"></video>
        <button id="getMedia">Get user media</button>
    </p>
    <script>

        

        $('#getMedia').on('click', (e) => {
            init(e);
        })

        const constraints = window.constraints = {
            audio: false,
            video: true
        };

        async function init(e) {
            try {
                const stream = await navigator.mediaDevices.getUserMedia(constraints);
                console.log(stream);
                handleSuccess(stream);
            } catch (e) {
                console.log(e);
            }
        }

        function handleSuccess(stream) {
            const video = document.querySelector('#myVideo');
            const videoTracks = stream.getVideoTracks();
            console.log('Got stream with constraints:', constraints);
            console.log(`Using video device: ${videoTracks[0].label}`);
            window.stream = stream; // make variable available to browser console
            video.srcObject = stream;
        }

    </script>

Так как функция navigator.mediaDevices.getUserMedia работает в асинхронном режиме мы ее вызываем через async/await.

stream.getVideoTracks() - получает видео-дорожки т.к. на одной странице могут быть подключено несколько камер на устройстве пользователя.

Результат.

![start page]({path-to-subject}/images/8.png)

Теперь нам нужно создать Sdp или Offer с настойками нашего видеопотока.

    <button id="createOffer">Create offer</button>

    $('#createOffer').on('click', (e) => {
        offer(e);
    })

    const offerOptions = {
        offerToReceiveAudio: 0,
        offerToReceiveVideo: 1,
        iceRestart: 1,
        voiceActivityDetection: 0
    };

    async function offer(e) {
       const peerConnection = window.peerConnection = new RTCPeerConnection(null);
       const offer = await peerConnection.createOffer(offerOptions);
       console.log(offer);
    }

![start page]({path-to-subject}/images/9.png)

Далее, когда мы испекли объект Offer (SDP) мы можем передать его на сервер.

Для этого на сервере сделаем запрос, который по HTTP примет эти данные и запишет в базу.

    from django.shortcuts import render
    from rest_framework.permissions import AllowAny
    from rest_framework.response import Response
    from rest_framework.views import APIView
    from drf_yasg.utils import swagger_auto_schema
    from .serializers.offer_request import OfferRequestSerializer


    @swagger_auto_schema(
        request_body=OfferRequestSerializer
    )
    class OfferView(APIView):
        """
           Get offer from abonent after click Show cam button.

        """
        permission_classes = (AllowAny,)

        @swagger_auto_schema(
            request_body=OfferRequestSerializer
        )
        def post(self, request, format=None):
            print(request.data)
            return Response({'offer': 'ok'})

Создадим простой серилизатор.

    from rest_framework import serializers


    class OfferRequestSerializer(serializers.Serializer):
        sid = serializers.CharField()
        offer = serializers.CharField()

Включим запрос в роутинг.
    
    from webrtc.views import OfferView
    ...

    urlpatterns = [
        path('offer', OfferView.as_view()),

    ...

![start page]({path-to-subject}/images/10.png)

Теперь на клиенте можно попробовать отправить запрос и передать всю информацию об Offer на сервер.

       $.ajax({
        type: "POST",
        url: url,
        data: {
            'sid': window.sessionStorage.getItem('sid'),
            'offer': JSON.stringify(offer)
        },
        });

Однако мы получаем ошибку защиты формы специальной подписью, которая отсутствует.

![start page]({path-to-subject}/images/11.png)

Поэтому можно создать промежуточный класс, который отключает эту защиту и включить его в список MIDDLEWARE в настройках.

Вот как выглядит этот класс.


    class DisableCSRFMiddleware(object):

        def __init__(self, get_response):
            self.get_response = get_response

        def __call__(self, request):
            setattr(request, '_dont_enforce_csrf_checks', True)
            response = self.get_response(request)
            return response

Где мы устанавливаем в запросе флаг _dont_enforce_csrf_checks в True и передаем его дальше по цепочке классов Middleware в объекте response.


    MIDDLEWARE = [
        ...
        # 'django.middleware.csrf.CsrfViewMiddleware',
        'app.csrf_middleware.DisableCSRFMiddleware',
        ...
    ]

Теперь сохраним поступившую информацию в базу.

    class OfferView(APIView):
        ...
        def post(self, request, format=None):
            conn = UserConnection.objects.get(sid=request.data['sid'])
            offer = Sdp()
            offer.sdp = request.data['offer']
            offer.conn = conn
            offer.save()
            return Response({'offer': 'ok'})

![start page]({path-to-subject}/images/12.png)


