---
sidebar_position: 1
slug: /
---

# Getting Started

Starting with `docker run` is the simplest way to get up and running with DragonflyDB.

If you do not have docker on your machine, [Install Docker](https://docs.docker.com/get-docker/) before continuing.

## Step  1

```sh
docker run --network=host --ulimit memlock=-1 docker.dragonflydb.io/dragonflydb/dragonfly
```

Dragonfly DB will answer to both `http` and `redis` requests out of the box!

You can use `redis-cli` to connect to `localhost:6379` or open a browser and visit `http://localhost:6379`

:::info

On some configurations, running with the `docker run --privileged ...` flag can fix some initialization errors.
:::

## Step 2

Connect with a redis client

```sh
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
