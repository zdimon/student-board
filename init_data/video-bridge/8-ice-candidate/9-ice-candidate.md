# Обмен ICE кандидатами.
      
Эти кандидаты содержат информацию о сетевом соединении и их будет много для каждого клиента.

В процессе обмена ими система подберет самые подходящие 2 по одному из набора каждой из сторон.

Система начинает автоматически их генерировать в момент установки всех SDP (setRemoteDescription и setLocalDescription) и делает это в событии  icecandidate на которое можно подписать функцию.

    function onIceCandidate(e) {
        console.log(e);
    }

    async function offer(e) {
       const peerConnection = window.peerConnection = new RTCPeerConnection(null);
       window.peerConnection.addEventListener('icecandidate', e => onIceCandidate(e));

    ...

Как они выглядят

![start page]({path-to-subject}/images/23.png)

Как видим они содержат реальный IP адрес за пределами роутера в локальной сети (за NAT).

Передадим этих кандидатов на сервер.


        function onIceCandidate(e) {
            console.log(e);
           let url = '{{server_name}}:{{server_port}}/ice';
           $.ajax({
            type: "POST",
            url: url,
            contentType: "application/json",
            data: JSON.stringify({
                'sid': window.sessionStorage.getItem('sid'),
                'ice': JSON.stringify(e.candidate),
            }),
                success: (data) => {
                    console.log(data);
                },
            });
        }

Создадим вьюшку под прием на сервере где по переданному sid найдем нужный нам объект Sdp.

    class IceView(APIView):
        """
           Get ice candidates.

        """
        permission_classes = (AllowAny,)

        @swagger_auto_schema(
            request_body=IceRequestSerializer
        )
        def post(self, request, format=None):
            payload = request.data
            # поищем соединение
            try:
                conn = UserConnection.objects.get(sid=payload['sid'])
            except ObjectDoesNotExist:
                return Response({'status': 1, 'message': 'Connection does not exist!'})

            # поищем SDP для передающей стороны
            try:
                sdp = Sdp.objects.get(from_user=conn.user)
            except ObjectDoesNotExist:
                print('Sdp for sender not found')

            # поищем SDP для принимающей стороны
            try:
                sdp = Sdp.objects.get(to_user=conn.user)
            except ObjectDoesNotExist:
                print('Sdp for reciever not found')

            print(sdp)

            return Response({'ice': payload})


Серилизатор.

    from rest_framework import serializers


    class IceRequestSerializer(serializers.Serializer):
        sid = serializers.CharField()
        ice = serializers.CharField()

Теперь создадим функцию для рассылки ICE кандидатов.

    @task()
    def send_ice_task(user_id, ice):
        sender = UserProfile.objects.get(pk=user_id)
        # Находим все соединения цели
        for conn in UserConnection.objects.filter(user=sender):
            # отсылаем сообщения на сокет
            payload = {"ice": ice}
            mgr.emit('ice_candidate', data=payload, room=conn.sid)

И используем ее.

          ...
            # поищем SDP для передающей стороны
            try:
                sdp = Sdp.objects.get(from_user=conn.user)
                send_ice_task(sdp.to_user.id, payload['ice'])
            except ObjectDoesNotExist:
                print('Sdp for sender not found')

            # поищем SDP для принимающей стороны
            try:
                sdp = Sdp.objects.get(to_user=conn.user)
                send_ice_task(sdp.from_user.id, payload['ice'])
            except ObjectDoesNotExist:
                print('Sdp for reciever not found')
          ...


При попытке добавить кандидата в соединение 

        socket.on('ice_candidate', (msg) => {
            console.log('get Ice candidate...')
            const ice = JSON.parse(msg.ice);
            onIceCandidate(ice);
        });


    })

    async function onIceCandidate(ice) { 
         await window.peerConnection.addIceCandidate(ice);
         console.log(window.peerConnection);
    }

получили ошибку

    Candidate missing values for both sdpMid and sdpMLineIndex

Поставим условие на null

        socket.on('ice_candidate', (msg) => {
            console.log('get Ice candidate...')
            console.log(msg)
            const ice = JSON.parse(msg.ice);
            if (ice !== null) {
                onIceCandidate(ice);
            }
        });

Теперь необходимо отработать такое событие 

    window.peerConnection.addEventListener('track', gotRemoteStream);

Которое сработает когда мы получим видео на стороне принимающего.

    function gotRemoteStream(e) {
        const video = document.querySelector('#myVideo');
        video.srcObject = e.streams[0];
    }

Теперь создадим обработчик создания ICE кандидатов на принимающей стороне и отправим их на сервер.

        function onIceCandidate(e) {
            console.log('Generating ICE candidates');
            console.log(e);
           let url = '{{server_name}}:{{server_port}}/ice';
           $.ajax({
            type: "POST",
            url: url,
            contentType: "application/json",
            data: JSON.stringify({
                'sid': window.sessionStorage.getItem('sid'),
                'ice': JSON.stringify(e.candidate),
            }),
                success: (data) => {
                    console.log(data);
                },
            });
        }

Получим на передающей стороне.


    ...
        socket.on('ice_candidate', (msg) => {
            console.log('get Ice candidate...')
            const ice = JSON.parse(msg.ice);
            if (ice !== null) {
                reciveIceCandidate(ice);
            }
        });

    })


    async function reciveIceCandidate(ice) { 
            await window.peerConnection.addIceCandidate(ice);
    }

    ...

![start page]({path-to-subject}/images/24.png)

## Полный пример на Typescript.

класс App.ts


    import { config } from './config';
    import { PeerConnection } from './PeerConnection';
    import SocketConnection from './SocketConnection';
     

    export default class App {

        pcon: PeerConnection;
        scon: SocketConnection;
        tracks: any;
        stream: any;
        videotag: any;

        async initappSender(username: string) {
            this.scon = new SocketConnection();
            this.scon.connect(username);
            this.pcon = new PeerConnection();
            this.stream = await this.pcon.getmedia();
                   
            $('#SendOffer').on('click', (e) => {
                this.attachVideo();
                // console.log(this.tracks);
                this.pcon.offer(this.tracks,this.stream);
            })  

            this.scon.socket.on('reciever_answer', async (msg) => {
                // console.log('Answer from reciever');
                // console.log(msg);
                this.pcon.rtcConnection.setRemoteDescription(JSON.parse(msg.reciever_answer));
                // console.log(this.pcon);
            })

            this.scon.socket.on('ice_candidate', async (msg) => {
               await this.pcon.addIceCandidate(msg.ice);
            })

        }

        initappReciever(username: string){
            this.scon = new SocketConnection();
            this.scon.connect(username);
            this.pcon = new PeerConnection();
            $('#callButton').on('click', (e) => {
                this.callUser();
            })
            this.scon.socket.on('sender_offer', async (msg) => {
                // console.log(msg);
                this.pcon.setRemoteDescription(JSON.parse(msg.sender_offer))
                const answer = await this.pcon.createAnwer();
                this.pcon.setLocalDescription(answer);
                // console.log(answer);
                const url = `${config.serverURL}offer`;
                $.ajax({
                    type: "POST",
                    url: url,
                    contentType: "application/json",
                    data: JSON.stringify({
                        'sid': window.sessionStorage.getItem('sid'),
                        'answer': JSON.stringify(answer),
                        'reciever_login': 'man',
                        'type': 'reciever'
                    }),
                        success: (data) => {
                            console.log(data);
                        },
                    });
                
            });

            this.scon.socket.on('ice_candidate', async (msg) => {
                await this.pcon.addIceCandidate(msg.ice);
            })

            this.pcon.rtcConnection.addEventListener('track', (e) => {
                console.log('We have got the video!!!');
                // console.log(e);
                this.videotag = document.querySelector('#myVideo');
                this.videotag.srcObject = e.streams[0];
            })

        }

        attachVideo() {
            this.videotag = document.querySelector('#myVideo');
            this.tracks = this.stream.getVideoTracks();
            this.videotag.srcObject = this.stream;
        }

        callUser() {
            const url = `${config.serverURL}call`;
            // console.log(url);
            $.ajax({
                url: url,
                type: "POST",
                data: JSON.stringify({
                    login: $('#CallUsername').val(),
                    sid: window.sessionStorage.getItem('sid')
                }),
                contentType: "application/json",
                success: (response: any) => {
                    // console.log(response);
                }
            }); 
        }


    }

Класс PeerConnection.ts

    import { config } from './config';


    export class PeerConnection {

        rtcConnection: any;

        constructor() {
            this.rtcConnection = new RTCPeerConnection(null);
            this.rtcConnection.addEventListener('icecandidate', (e) => { this.onIceCandidate(e) })
        }

        async addIceCandidate(ice: string){
            const allice = JSON.parse(ice);
            if(allice !== null) {
                await this.rtcConnection.addIceCandidate(allice);
            }
            
        }

        onIceCandidate(e) {
            console.log(e);
            const url = `${config.serverURL}ice`;
            $.ajax({
                type: "POST",
                url: url,
                contentType: "application/json",
                data: JSON.stringify({
                    'sid': window.sessionStorage.getItem('sid'),
                    'ice': JSON.stringify(e.candidate)
                }),
                    success: (data) => {
                        console.log(data);
                    },
                });
        }

        setRemoteDescription(offer){
            this.rtcConnection.setRemoteDescription(offer);
        }

        setLocalDescription(offer){
            this.rtcConnection.setLocalDescription(offer);
        }

        async createAnwer(){
            return await this.rtcConnection.createAnswer();
        }

        async getmedia(): Promise<any>  {
            const constraints = {
                audio: false,
                video: true
            };
            try {

                const stream = await navigator.mediaDevices.getUserMedia(constraints);
                return stream;

            } catch(e) {
                console.log(e);
            }
        }

        async offer(tracks: any, localStream: any) {

            const offerOptions = {
                offerToReceiveAudio: 0,
                offerToReceiveVideo: 1,
                iceRestart: 1,
                voiceActivityDetection: 0
            };

            
            tracks.forEach((track) => this.rtcConnection.addTrack(track,localStream) );
            console.log('Creating offer!');
            const offer = await this.rtcConnection.createOffer(offerOptions);
            await this.rtcConnection.setLocalDescription(offer);

            const url = `${config.serverURL}offer`;
            $.ajax({
                type: "POST",
                url: url,
                contentType: "application/json",
                data: JSON.stringify({
                    'sid': window.sessionStorage.getItem('sid'),
                    'offer': JSON.stringify(offer),
                    'reciever_login': 'man',
                    'type': 'sender'
                }),
                    success: (data) => {
                        console.log(data);
                    },
                });

                
        }

    }

Класс SocketConnection.ts.

    import  io  from "socket.io-client";

    export default class SocketConnection {
        socket: any;
        connect(login: string) {
            this.socket = io('http://localhost:5001', {transports:['websocket']});

            this.socket.on('connect', () => {
                console.log('Connection was established');
                window.sessionStorage.setItem('sid',this.socket.id);
                this.socket.emit('login',{login});
            })    
            
            this.socket.on('calling', (msg) => {
                $('#responseBox').show();
                $('#callerName').html(msg.login);
                console.log(msg);
            });



        }

    }


config.ts

    export const config = {
        serverURL: 'http://localhost:8888/'
    }






