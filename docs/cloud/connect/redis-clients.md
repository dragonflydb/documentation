---
sidebar_position: 1
---

import PageTitle from '@site/src/components/PageTitle';

# Redis Clients

<PageTitle title="Connecting with Redis Clients | Dragonfly Cloud" />

Once a data store's **Status** is **Active**, you can connect to it with any Redis client by following the **Connection Details**
section in the data store details drawer.
Here are a few popular client libraries and code snippets to connect to the data store.

### Notes

- Unless otherwise specified, you should use the connection details found for each data store
  to replace those placeholders in the code snippets below, where we use public endpoints with the `default` user and TLS disabled.
- **For production, we strongly recommend using private [networks](../networks.md) and [connections](../connections.md).**

---

## Redis CLI

- Install [`redis-cli`](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/).
- With the **Connection URI** from the data store drawer, run `redis-cli` in the terminal:

```shell
$> redis-cli -u <CONNECTION_URI> PING
```

- If you are running a **Dragonfly Swarm** multi-shard cluster in Dragonfly Cloud, make sure to use the cluster-aware flag:

```shell
# The '-c' flag enables client-side cluster mode, which follows '-ASK' and '-MOVED' redirections.
$> redis-cli -c -u <CONNECTION_URI> PING
```

---

## TypeScript & JavaScript

- Install the [`ioredis`](https://github.com/redis/ioredis) package.
- Use the following code snippet to connect to the data store:

```javascript
import { Redis as Dragonfly } from "ioredis";

// Connection details can be found in your Dragonfly Cloud console.
const client = new Dragonfly({
  host: "<URL>",
  port: 6385,
  username: "default",
  password: "<KEY>",
});

client.ping().then((resp) => console.log(resp));
```

- While running a **Dragonfly Swarm** cluster, make sure to use the cluster-aware version of the client as shown below.
- If your application can tolerate potentially stale reads, you can further scale read throughput by leveraging read replicas, available by default when you deploy Dragonfly Swarm with replicas.

```javascript
import { Redis as Dragonfly } from "ioredis";

// Connection details can be found in your Dragonfly Cloud console.
//
// For the 'scaleReads' option:
//  - 'master': All queries, including reads, are sent to primary nodes.
//  - 'all': Write to primary nodes, read from either primary nodes or replicas.
//  - 'slave': Write to primary nodes, read from replicas exclusively.
import { Redis as Dragonfly } from "ioredis";

const client = new Dragonfly.Cluster(
  [{ host: "<URL>", port: 6385 }],
  {
    redisOptions: {
      username: "default",
      password: "<KEY>",
    },
    scaleReads: "slave",
  },
);

client.ping().then((resp) => console.log(resp));
```

---

## Python

- Install the [redis-py](https://github.com/redis/redis-py) package.
- Use the following code snippet to connect to the data store:

```python
import redis

# Connection details can be found in your Dragonfly Cloud console.
client = redis.Redis.from_url("<CONNECTION_URI>")
client.ping()
```

- While running a **Dragonfly Swarm** cluster, make sure to use the cluster-aware version of the client as shown below.
- If your application can tolerate potentially stale reads, you can further scale read throughput by leveraging read replicas, available by default when you deploy Dragonfly Swarm with replicas.

```python
from redis import RedisCluster as DragonflySwarm

# Connection details can be found in your Dragonfly Cloud console.
client = DragonflySwarm(
    host="<URL>",
    port=6385,
    username="default",
    password="<KEY>",
    read_from_replicas=True,  # Enables read-only commands on replicas.
)

client.ping()
```

---

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
    // Connection details can be found in your Dragonfly Cloud console.
    client := redis.NewClient(&redis.Options{
		Addr:     "<URL>:<PORT>",
		Username: "default",
		Password: "<KEY>",
	})

    pong, err := client.Ping(context.Background()).Result()
    if err != nil {
        fmt.Println(err)
    }

    fmt.Println(pong)
}
```

- While running a **Dragonfly Swarm** cluster, make sure to use the cluster-aware version of the client as shown below.
- If your application can tolerate potentially stale reads, you can further scale read throughput by leveraging read replicas, available by default when you deploy Dragonfly Swarm with replicas.

```go
package main

import (
	"context"
	"fmt"

	"github.com/redis/go-redis/v9"
)

func main() {
	// Connection details can be found in your Dragonfly Cloud console.
	client := redis.NewClusterClient(
		&redis.ClusterOptions{
			Addrs: []string{
				"<URL>:<PORT>",
			},
			Username: "default",
			Password: "<KEY>",
			ReadOnly: true, // Enables read-only commands on replicas.
		},
	)

	pong, err := client.Ping(context.Background()).Result()
	if err != nil {
		fmt.Println(err)
	}

	fmt.Println(pong)
}
```
