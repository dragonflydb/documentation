---
sidebar_position: 1
---

import PageTitle from '@site/src/components/PageTitle';

# Redis Clients

<PageTitle title="Connecting with Redis Clients | Dragonfly Cloud" />

Once a data store's **Status** is **Active**, you can connect to it with any Redis client using the **Connection URI**
provided in the data store drawer (e.g., `rediss://default:XXXXX@abcde.dragonflydb.cloud:6385`).
Here are a few popular client libraries and code snippets to connect to the data store.

## Redis CLI

- Install [`redis-cli`](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/).
- With the **Connection URI** from the data store drawer, execute `redis-cli` in the terminal:

```shell
$> redis-cli -u <CONNECTION_URI> PING
```

## JavaScript | Typescript | Node.js

- Install the [`ioredis`](https://github.com/redis/ioredis) package.
- Use the following code snippet to connect to the data store:

```javascript
const Redis = require("ioredis");

// Replace <CONNECTION_URI> with the actual Dragonfly Cloud connection URI.
const client = new Redis("<CONNECTION_URI>");
client.ping().then(resp => console.log(resp));
```

## Python

- Install the [redis-py](https://github.com/redis/redis-py) package.
- Use the following code snippet to connect to the data store:

```python
import redis

# Replace <CONNECTION_URI> with the actual Dragonfly Cloud connection URI.
client = redis.Redis.from_url("<CONNECTION_URI>")
client.ping()
```

## Go

- Install the [go-redis](https://github.com/redis/go-redis) package.
- Use the following code snippet to connect to the data store:

```go
package main

import (
    "context"
    "fmt"

    "github.com/redis/go-redis/v9"
)

func main() {
    // Replace <CONNECTION_URI> with the actual Dragonfly Cloud connection URI.
    // Note that <db> is the database number, and its default value is 0.

    opts, err := redis.ParseURL("<CONNECTION_URI>/<db>")
    if err != nil {
        panic(err)
    }

    client := redis.NewClient(opts)

    pong, err := client.Ping(context.Background()).Result()
    if err != nil {
        fmt.Println(err)
    }

    fmt.Println(pong)
}
```
