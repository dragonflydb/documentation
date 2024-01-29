---
sidebar_position: 0
---

# Install with Docker

Starting with `docker run` is the simplest way to get up and running with Dragonfly.

If you do not have docker on your machine, [Install Docker](https://docs.docker.com/get-docker/) before continuing.

## Prerequisites

- Minimum 4GB of RAM to get the benefits of Dragonfly
- Minimum 1 CPU Core
- Linux Kernel 4.19 or higher

## Step 1

### On linux

```bash
docker run --network=host --ulimit memlock=-1 docker.dragonflydb.io/dragonflydb/dragonfly
```

### On macOS

_`network=host` doesn't work well on macOS, see [this issue](https://github.com/docker/for-mac/issues/1031)_

```bash
docker run -p 6379:6379 --ulimit memlock=-1 docker.dragonflydb.io/dragonflydb/dragonfly
```

Dragonfly will respond to both `http` and `redis` requests out of the box!

You can use the `redis-cli` to connect to `localhost:6379` or open a browser and visit `http://localhost:6379`

**Note:** On some configurations, running with the `docker run --privileged ...` flag can fix some
initialization errors.

## Step 2

Connect with a redis client

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
