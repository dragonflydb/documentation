---
sidebar_position: 1
description: Redlock
---

# Redlock

## Introduction

[Redlock](https://redis.io/docs/manual/patterns/distributed-locks/) is a recognized algorithm based on Redis for
distributed locks, ensuring consistent operation and protection against failures such as network partitions and Redis crashes.
It operates by having a client application send lock requests, using [`SET`](../command-reference/strings/set.md) commands, to **multiple primary Redis instances**.
The lock is successfully acquired when more than half of these instances agree on the lock acquisition.
To release the lock, the client application uses a Lua script, which involves the [`GET`](../command-reference/strings/get.md) command
and the [`DEL`](../command-reference/generic/del.md) command, to perform compare-and-delete operations on all the instances involved.
Redlock also takes into account the lock validity time, retry on failure, lock extension, and many other aspects, which makes it a robust and reliable solution for distributed locking.

Since Dragonfly is highly compatible with Redis, Redlock implementations can be easily used with Dragonfly.

## Implementations

The following is a list of Redlock implementations in various languages, ordered by the language used:

- [redis-plus-plus](https://github.com/sewenew/redis-plus-plus/?tab=readme-ov-file#redlock) (C++)
- [RedLock.net](https://github.com/samcook/RedLock.net) (C#/.NET)
- [redsync](https://github.com/go-redsync/redsync) (Go)
- [redisson](https://github.com/redisson/redisson) (Java)
- [node-redlock](https://github.com/mike-marcacci/node-redlock) (JavaScript/TypeScript/Node.js)
- [Deno-Redlock](https://github.com/oslabs-beta/Deno-Redlock) (JavaScript/TypeScript/Deno)
- [pedlock-php](https://github.com/ronnylt/redlock-php) (PHP)
- [PHPRedisMutex](https://github.com/php-lock/lock?tab=readme-ov-file#phpredismutex) (PHP)
- [redlock-py](https://github.com/SPSCommerce/redlock-py) (Python)
- [pottery](https://github.com/brainix/pottery?tab=readme-ov-file#redlock) (Python)
- [aioredlock](https://github.com/joanvila/aioredlock) (Python with asyncio)
- [redlock-rb](https://github.com/antirez/redlock-rb) (Ruby)
- [rslock](https://github.com/hexcowboy/rslock) (Rust)

## Using Redlock with Dragonfly (Go)

Let's look at how to use Redlock with Dragonfly in a Go application using the `redsync` library.
Imagine that you have three Dragonfly instances, which are independent primary instances capable of handling lock requests.
This setup can be described using a `docker-compose.yml` file as follows:

```yaml
version: '3'
services:
  dragonfly-instance-0:
    container_name: "dragonfly-instance-0"
    image: 'ghcr.io/dragonflydb/dragonfly:v1.14.3-ubuntu'
    ulimits:
      memlock: -1
    ports:
      - "6379:6379"
  dragonfly-instance-1:
    container_name: "dragonfly-instance-1"
    image: 'ghcr.io/dragonflydb/dragonfly:v1.14.3-ubuntu'
    ulimits:
      memlock: -1
    ports:
      - "6380:6379"
  dragonfly-instance-2:
    container_name: "dragonfly-instance-2"
    image: 'ghcr.io/dragonflydb/dragonfly:v1.14.3-ubuntu'
    ulimits:
      memlock: -1
    ports:
      - "6381:6379"
```

Then, you can use the [`redsync`](https://github.com/go-redsync/redsync) library to acquire and release locks in a Go application:

```go
package main

import (
	"net/http"
	"time"

	"github.com/go-redsync/redsync/v4"
	redsyncredis "github.com/go-redsync/redsync/v4/redis"
	redsyncpool "github.com/go-redsync/redsync/v4/redis/goredis/v9"
	"github.com/redis/go-redis/v9"
)

// These hosts are reachable from within the Docker network.
const (
	dragonflyHost0 = "dragonfly-instance-0:6379"
	dragonflyHost1 = "dragonfly-instance-1:6379"
	dragonflyHost2 = "dragonfly-instance-2:6379"
)

const (
	// The name of the global lock.
	globalLockKeyName = "my-global-lock"

	// The expiry of the global lock.
	globalLockExpiry = time.Minute

	// Number of retries to acquire the global lock.
	globalLockRetries = 8

	// The delay between retries to acquire the global lock.
	globalLockRetryDelay = 10 * time.Millisecond
)

func main() {
	// Create three clients for each instance of Dragonfly.
	var (
		hosts   = []string{dragonflyHost0, dragonflyHost1, dragonflyHost2}
		clients = make([]redsyncredis.Pool, len(hosts))
	)
	for idx, addr := range hosts {
		client := redis.NewClient(&redis.Options{
			Addr: addr,
		})
		clients[idx] = redsyncpool.NewPool(client)
	}

	// Create an instance of 'Redsync' to work with locks.
	rs := redsync.New(clients...)

	// Create a global lock mutex.
	globalMutex := rs.NewMutex(
		globalLockKeyName,
		redsync.WithExpiry(globalLockExpiry),
		redsync.WithTries(globalLockRetries),
		redsync.WithRetryDelay(globalLockRetryDelay),
	)

	// Obtain a lock for the global lock mutex.
	// After this is successful, no one else can obtain the same lock (with the same mutex name),
	// until we unlock it, or it expires automatically after the specified expiry time.
	if err := globalMutex.Lock(); err != nil {
		panic(err)
	}

	// Do your work that requires the lock.
	// ...

	// Release the lock so other processes or threads can obtain a lock.
	if ok, err := globalMutex.Unlock(); !ok || err != nil {
		panic("unlock failed")
	}
}
```

## Useful Resources

- Redlock [Documentation](https://redis.io/docs/manual/patterns/distributed-locks/).
- The [dragonfly-examples](https://github.com/dragonflydb/dragonfly-examples) repository, which contains code examples for using Redlock with Dragonfly in Go.
