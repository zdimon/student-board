## Openvidu

Установка docker и docker-compose.

    apt install docker-ce docker-compose

Установка openvidu
    
    cd /opt
    curl https://s3-eu-west-1.amazonaws.com/aws.openvidu.io/install_openvidu_latest.sh | bash

Прописываем настройки  DOMAIN_OR_PUBLIC_IP и OPENVIDU_SECRET в .env

Стартуем сервер.


    ./openvidu start

Старт сервера вручную

    docker run -p 4443:4443 --rm -e OPENVIDU_SECRET=MY_SECRET openvidu/openvidu-server-kms:2.18.0


Устанавливаем  пример приложения.

    git clone https://github.com/OpenVidu/openvidu-tutorials.git -b v2.18.0


Подсоединяем клиента.

    <script src="openvidu-browser-2.18.0.js"></script>

Стартуем сессию.

    var myapp = {
        initappSender: (uname) => {
            console.log(`Init sender ${uname}`);
            OV = new OpenVidu();
            session = OV.initSession();
            console.log(session);
        }
    }

Далее создаем сессию на сервере, передав токен пользователя.

    var myapp = {
        OPENVIDU_SERVER_URL: 'https://localhost:4443',
        OPENVIDU_SERVER_SECRET: 'MY_SECRET',
        initappSender: function (uname){
            console.log(`Init sender ${uname}`);
            OV = new OpenVidu();
            session = OV.initSession();
            
            session.on('exception', (exception) => {
                console.warn(exception);
            });
            this.createSession('dimon');
        },

        createSession: function(sessionId) { // See https://docs.openvidu.io/en/stable/reference-docs/REST-API/#post-openviduapisessions
            return new Promise((resolve, reject) => {
                $.ajax({
                    type: "POST",
                    url: this.OPENVIDU_SERVER_URL + "/openvidu/api/sessions",
                    data: JSON.stringify({ customSessionId: sessionId }),
                    headers: {
                        "Authorization": "Basic " + btoa("OPENVIDUAPP:" + this.OPENVIDU_SERVER_SECRET),
                        "Content-Type": "application/json"
                    },
                    success: (response) => { 
                        console.log(response);
                        resolve(response.id)
                    },
                    error: (error) => {
                        if (error.status === 409) {
                            resolve(sessionId);
                        } else {
                            console.warn('No connection to OpenVidu Server. This may be a certificate error at ' + this.OPENVIDU_SERVER_URL);
                            if (window.confirm('No connection to OpenVidu Server. This may be a certificate error at \"' + this.OPENVIDU_SERVER_URL + '\"\n\nClick OK to navigate and accept it. ' +
                                'If no certificate warning is shown, then check that your OpenVidu Server is up and running at "' + this.OPENVIDU_SERVER_URL + '"')) {
                                location.assign(this.OPENVIDU_SERVER_URL + '/accept-certificate');
                            }
                        }
                    }
                });
            });
        }

    }




