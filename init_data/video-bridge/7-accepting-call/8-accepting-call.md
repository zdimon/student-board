# Принимаем вызов в видео-чат на принимающей сотороне.
        
При приеме сообщения о согласии на видео-чат нам приходят следующие данные 

    { 
        sender_login: "woman", 
        sender_offer: "sring" 
    }

При этом срабатывает событие sender_offer.

Вызовем в нем функцию offer и передадим туда Offer.

        socket.on('sender_offer', (msg) => {
            console.log('Request accepted!!!!')
            console.log(msg);
            offer(JSON.parse(msg.sender_offer));
        });

Далее установим этот Offer в качестве setRemoteDescription

    async function offer(sender_offer) {
       const peerConnection = window.peerConnection = new RTCPeerConnection(null);
       const offer = await peerConnection.createOffer(offerOptions);
       window.peerConnection.setRemoteDescription(sender_offer)
       console.log(window.peerConnection)

    ...

Результат.

![start page]({path-to-subject}/images/19.png)

Теперь время создать объек Answer на стороне принимающего

    const answer = await window.peerConnection.createAnswer();
    console.log(answer);

![start page]({path-to-subject}/images/20.png)

И передать на сервер.

       const answer = await window.peerConnection.createAnswer();

       let url = '{{server_name}}:{{server_port}}/offer';
       $.ajax({
        type: "POST",
        url: url,
        data: {
            'sid': window.sessionStorage.getItem('sid'),
            'answer': JSON.stringify(answer),
            'type': 'reciever'
        },
            success: (data) => {
                console.log(data);
            },
        });

Итак что происходит при приходе Offer от передающей стороны у принимающей.

1. Создается объект RTCPeerConnection

    const peerConnection = window.peerConnection = new RTCPeerConnection(null);

2. Привязываемся к его событиям (реализуем позже).

    // window.peerConnection.addEventListener('icecandidate', e => onIceCandidate(e));
    // window.peerConnection.addEventListener('track', gotRemoteStream);

3. Устанавливаем пришедший Offer

        try {
            await window.peerConnection.setRemoteDescription(sender_offer);
        } catch (e) {
            console.log(e);
        }

4. Создаем объект ответа и устанавливаем его в setLocalDescription.

        const answer = await window.peerConnection.createAnswer();
        await window.peerConnection.setLocalDescription(answer);

5. Посылаем ответ на сервер.

       let url = '{{server_name}}:{{server_port}}/offer';
       $.ajax({
        type: "POST",
        url: url,
        data: {
            'sid': window.sessionStorage.getItem('sid'),
            'answer': JSON.stringify(answer),
            'type': 'reciever'
        },
            success: (data) => {
                console.log(data);
            },
        });

Теперь на сервере отработаем 2 ситуации, когда к нам приходит offer и когда answer


        def post(self, request, format=None):
            payload = request.data
            conn = UserConnection.objects.get(sid=payload['sid'])
            offer = Sdp()
            # найдем существующее Sdp или создадим новое
            if payload['type'] == 'sender':
                try:
                    offer = Sdp.objects.get(from_user=conn.user)
                except ObjectDoesNotExist:
                    offer = Sdp()
            else:
                try:
                    offer = Sdp.objects.get(to_user=conn.user)
                except ObjectDoesNotExist:
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
            # устанавливаем Offer (answer) для принимающего
            else:
                offer.to_user = conn.user
                offer.to_user_sdp = payload['answer']
            offer.save()
            return Response({'offer': 'ok'})

В результате получаем в базе все данные по соединению.

![start page]({path-to-subject}/images/21.png)

Теперь нам необходимо передать answer на передающую сторону.


    def post(self, request, format=None):
        ...
        if payload['type'] == 'sender':
           ...
        else:
            offer.to_user = conn.user
            offer.to_user_sdp = payload['answer']
            # уведомляем передающую сторону через задачу для celery
            sender_answer_task(offer.from_user.id, payload['answer'])

Создадим функцию sender_answer_task


    @task()
    def sender_answer_task(sender_id, reciever_answer):
        sender = UserProfile.objects.get(pk=sender_id)
        # Находим все соединения по принимающей стороне
        for conn in UserConnection.objects.filter(user=sender):
            # отсылаем сообщения на сокет
            payload = {"reciever_answer": reciever_answer}
            mgr.emit('reciever_answer', data=payload, room=conn.sid)

Принимаем сообщение на стороне клиента передающей стороны и устанавливаем setRemoteDescription.

        ...
            socket.on('reciever_answer', (msg) => {
                 console.log('Answer from reciecer!');
                 setAnswer(msg);
            });

        })

        async function setAnswer(msg) {
            await window.peerConnection.setRemoteDescription(
                JSON.parse(msg.reciever_answer));
            console.log(window.peerConnection);
        }
        ...

![start page]({path-to-subject}/images/22.png)


