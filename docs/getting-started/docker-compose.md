---
sidebar_position: 1
---

# Install with Docker Compose


This guide will have you up running Dragonfly with `docker-compose` in just a few minutes.

If you do not have `docker` and `docker-compose` installed on your machine, before continuing install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/).

## Step 1

```bash
# Download Official Dragonfly Docker Compose File
wget https://raw.githubusercontent.com/dragonflydb/dragonfly/main/contrib/docker/docker-compose.yml

# Launch the Dragonfly Instance
docker compose up -d

# Confirm image is up
docker ps | grep dragonfly
# ac94b5ba30a0   docker.dragonflydb.io/dragonflydb/dragonfly   "entrypoint.sh drago…"   45 seconds ago   Up 31 seconds         0.0.0.0:6379->6379/tcp, :::6379->6379/tcp   docker_dragonfly_1

# Log follow the dragonfly container
docker logs -f docker_dragonfly_1
```

Dragonfly will respond to both `http` and `redis` requests out of the box!

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

Continue being great and build your app with the power of Dragonfly!  

## Tuning Dragonfly
If you are attempting to tune Dragonfly for performance, consider `NAT` performance costs associated with containerization.  

### Performance Tuning

In `docker compose`, there is a significant difference between using an `overlay` network (which relies on docker `NAT` traversal for every request) and the `host` network (see [`docker-compose.yml`](https://github.com/dragonflydb/dragonfly/blob/main/contrib/docker/docker-compose.yml)).

For more information, see the Docker compose file [network_mode docs](https://docs.docker.com/compose/compose-file/compose-file-v3/#network_mode).
