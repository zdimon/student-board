# Portainer. Начало работы.
     
Программа, предоставляющая веб-интерфейс для работы с Docker.

## Установка и запуск.

    docker volume create portainer_data

    docker run -d -p 8000:8000 -p 9000:9000 --name=portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce

Или так

    docker run -d -p 9000:9000 -p 8000:8000 --name portainer --restart always -v /var/run/docker.sock:/var/run/docker.sock -v /home/zdimon/web/portainer_data:/data portainer/portainer-ce

При этом создается volume директория portainer_data.

Такой командой можно постмотреть список всех volume.

    docker volume ls

Или посмотреть настройки конкретной volume.

    docker volume inspect portainer_data 

![start page]({path-to-subject}/images/2.png)

Как видим данные программы примонтированы в локальную папку 

    "Mountpoint": "/var/lib/docker/volumes/portainer_data/_data",

### Ошибка запуска демона докера

Иногда требуется запустить такую команду чтоб включить демон докера в автозагрузку

    sudo systemctl enable docker


### Установка swarm Edge Agent агента на удаленный хост

Запускаем такую команду на удаленной машине.

    docker network create \
      --driver overlay \
      portainer_agent_network;

    docker service create \
      --name portainer_edge_agent \
      --network portainer_agent_network \
      -e AGENT_CLUSTER_ADDR=tasks.portainer_edge_agent \
      -e EDGE=1 \
      -e EDGE_ID=949de264-f63e-44df-b850-6c846d11dea9 \
      -e EDGE_KEY=aHR0cDovLzE5Mi4xNjguOS4yNDB8MTkyLjE2OC45LjI0MDo4MDAwfDcxOjllOjIyOmRmOmYxOjViOjg0OjkyOjM2OmEyOjBhOjFhOjNhOmZkOmY0OjMxfDEz \
      -e CAP_HOST_MANAGEMENT=1 \
      --mode global \
      --constraint 'node.platform.os == linux' \
      --mount type=bind,src=//var/run/docker.sock,dst=/var/run/docker.sock \
      --mount type=bind,src=//var/lib/docker/volumes,dst=/var/lib/docker/volumes \
      --mount type=bind,src=//,dst=/host \
      --mount type=volume,src=portainer_agent_data,dst=/data \
      portainer/agent





