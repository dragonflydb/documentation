---
sidebar_position: 2
---

# Docker Compose

This guide will have you up running DragonflyDB with `docker-compose` in just a few minutes.

:::info
This guide assumes you have `docker` and `docker-compose` installed on your machine. 

If not, [Install Docker](https://docs.docker.com/get-docker/) and [Install Docker Compose](https://docs.docker.com/compose/install/) before continuing.
:::

## Step 1

Download the official Dragonfly DB Docker Compose file with the following bash command,


```bash
wget https://raw.githubusercontent.com/dragonflydb/dragonfly/main/contrib/docker/docker-compose.yml
```
Launch the Dragonfly DB instance on your machine,

```bash
docker-compose up -d
```

Confirm the image is up by running,

```bash
docker ps | grep dragonfly
```

You will see the following output:

```
# ac94b5ba30a0   docker.dragonflydb.io/dragonflydb/dragonfly   "entrypoint.sh drago…"   45 seconds ago   Up 31 seconds         0.0.0.0:6379->6379/tcp, :::6379->6379/tcp   docker_dragonfly_1
```

Log follow the Dragonfly container

```bash
docker logs -f docker_dragonfly_1
```

Dragonfly DB will answer to both `http` and `redis` requests out of the box!

You can use `redis-cli` to connect to `localhost:6379` or open a browser and visit `http://localhost:6379`

## Step 2

Connect with a redis client.

From a new terminal:

```bash
redis-cli
127.0.0.1:6379> set hello world
OK
127.0.0.1:6379> keys *
1) "hello"
127.0.0.1:6379> get hello
"world"
127.0.0.1:6379> 
```

## Step 3

Continue being great and build your app with the power of DragonflyDB!  

## Tuning Dragonfly DB
If you are attempting to tune Dragonfly DB for performance, consider `NAT` performance costs associated with containerization.  
## Performance Tuning
---
In `docker-compose`, there is a meaningful difference between an `overlay` network(which relies on docker `NAT` traversal on every request) and using the `host` network(see [`docker-compose.yml`](https://github.com/dragonflydb/dragonfly/blob/main/contrib/docker/docker-compose.yml)).  
&nbsp;  
Fore more information, see the [official docker-compose network_mode Docs](https://docs.docker.com/compose/compose-file/compose-file-v3/#network_mode)  
&nbsp;  


```yml
version: '3.8'
services:
  dragonfly:
    image: 'docker.dragonflydb.io/dragonflydb/dragonfly'
    ulimits:
      memlock: -1
    ports:
      - "6379:6379"
    # For better performance, consider `host` mode instead `port` to avoid docker NAT.
    # `host` mode is NOT currently supported in Swarm Mode.
    # https://docs.docker.com/compose/compose-file/compose-file-v3/#network_mode
    # network_mode: "host"
    volumes:
      - dragonflydata:/data
volumes:
  dragonflydata:
```
