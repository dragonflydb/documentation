---
sidebar_position: 1
description: Redlock
---

# Redlock

## Introduction

[Redlock](https://redis.io/docs/manual/patterns/distributed-locks/) is a recognized algorithm used with Redis for creating
distributed locks, ensuring consistent operation and protection against failures such as network partitions and Redis crashes.
It operates by having a client send lock requests, using the [`SET`](../command-reference/strings/set.md) command, to multiple primary Redis instances.
The lock is successfully acquired when more than half of these instances agree on the lock acquisition.
To unlock, the client issues [`DEL`](../command-reference/generic/del.md) commands to all the instances involved.

Since Dragonfly is highly compatible with Redis and both `SET` and `DEL` commands are fully supported, Redlock implementations can be easily used with Dragonfly.

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