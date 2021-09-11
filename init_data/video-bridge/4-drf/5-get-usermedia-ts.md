# Получение видеопотока.
    
Создадим класс PeerConnction


    export class PeerConnction {

        async getmedia() {
            const constraints = {
                audio: false,
                video: true
            };
            try {

                const stream = await navigator.mediaDevices.getUserMedia(constraints);
                console.log(stream);

            } catch(e) {
                console.log(e);
            }
        }

    }

Вызовем функцию из App.ts.

    import { PeerConnction } from './PeerConnection';
    import SocketConnection from './SocketConnection';
     

    export default class App {
        
        pcon: PeerConnction;
        scon: SocketConnection;

        initapp(username: string) {
            this.scon = new SocketConnection();
            this.scon.connect(username);
            this.pcon = new PeerConnction();
            this.pcon.getmedia();
        }

    }

![start page]({path-to-subject}/images/25.png)

Работа в асинхронностью через async/await

    import { PeerConnection } from './PeerConnection';
    import SocketConnection from './SocketConnection';
     

    export default class App {

        pcon: PeerConnection;
        scon: SocketConnection;
        tracks: any;
        stream: any;
        videotag: any;

        async initapp(username: string) {
            this.scon = new SocketConnection();
            this.scon.connect(username);
            this.pcon = new PeerConnection();
            this.stream = await this.pcon.getmedia();
            this.attachVideo();
        }

        attachVideo() {
            this.videotag = document.querySelector('#myVideo');
            this.tracks = this.stream.getVideoTracks();
            this.videotag.srcObject = this.stream;
        }


    }








