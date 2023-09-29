---
sidebar_position: 1
description: BullMQ
---

# BullMQ

## Introduction

BullMQ is a Node.js library that implements a fast and robust queue system built on top of Redis that helps in resolving many modern-age microservices architectures.

## Dragonfly x BullMQ

Since Dragonfly is highly compatible with Redis, BullMQ can be used with Dragonfly with zero to minimal code changes in your application.
By replacing Redis with Dragonfly, you can achieve superior performance and scalability for your BullMQ application.

However, the integration of Dragonfly with BullMQ involves some specific configuration steps to ensure optimal performance and compatibility with BullMQ internals.

BullMQ extensively uses Lua scripts (server-side scripting) for executing commands in Redis.
When running a Lua script in Redis, it's essential to explicitly specify all the keys the script will access.
However, the design of BullMQ doesn't allow it to predict in advance which keys its Lua scripts will need.
Although accessing undeclared keys is unsupported in Redis, it nonetheless works.
However, in Dragonfly, it cannot work out of the box due to our multi-threaded transactional framework.

As such, one could run Dragonfly with Lua global transaction mode:

```bash
$> ./dragonfly --default_lua_flags=allow-undeclared-keys
```

This mode locks the entire data store for each Lua script. In other words, it is slow, but it is safe and does not require any changes from the code that uses BullMQ.

To utilize Dragonfly's multi-threaded capability and achieve superior performance for your application, we introduce a mode that enables locks on hashtags instead of individual keys.
In this mode, each BullMQ queue will be exclusively owned by a single thread, and accessing multiple queues could be done in parallel.
To employ Dragonfly in this mode, please follow the steps below to configure Dragonfly and utilize BullMQ in your application.

### 1. Hashtag Locking

Run Dragonfly with the following flags:

```bash
$> ./dragonfly --cluster_mode=emulated --lock_on_hashtags
```

- `--cluster_mode=emulated` instructs Dragonfly to emulate a Redis Cluster on a single instance.
- `--lock_on_hashtags` enables hashtag locking. More about hashtags in the [next step](#2-queue-naming-strategies).

### 2. Queue Naming Strategies

When setting up your application, use hashtags in your queue names.
In short, when a hashtag is present in a key, along with the `--lock_on_hashtags` flag, Dragonfly will lock the key to a thread based on the hashtag.
Read more about the original hashtag design for the Redis Cluster specification [here](https://redis.io/docs/reference/cluster-spec/#hash-tags),
as well as the Dragonfly emulated cluster mode [here](./../managing-dragonfly/cluster-mode.md).

In order to use a hashtag in a queue name, you can initialize a queue as follows:

```javascript
import { Queue } from 'bullmq';

// Note the wrapping curly brackets in the queue name string.
//
// Dragonfly assigns this queue to a specific thread based on only the substring "myprefix",
// instead of the full queue name string "{myprefix}:myqueue".
//
// Also, do not confuse the curly brackets here with JavaScript template literals.
// These curly brackets are part of the queue name string that will be used by Dragonfly.
const queue = new Queue("{myprefix}:myqueue");
```

Alternatively, you can utilize the BullMQ `prefix` option for queue initialization:

```javascript
import { Queue } from 'bullmq';

const queue = new Queue("myqueue", {
  prefix: "{myprefix}",
});
```

By adopting the queue naming strategies mentioned above, queues that share the same hashtag will be assigned to the same Dragonfly thread.
This ensures shard consistency and efficient hardware resource utilization.

### 3. Queue Dependencies

If you have queue dependencies, especially a parent-child relationship, it's important to use the same hashtag for both queues.
This ensures that they are processed within the same Dragonfly thread and maintains the integrity of the dependencies.

### 4. Thread Balancing

To achieve superior performance for your application, consider employing a larger number of queues with a different hashtag for each.
By distributing the queues across distinct Dragonfly threads, you can optimize the utilization of the Dragonfly architecture efficiently.

## Useful Resources

- BullMQ [Homepage](https://bullmq.io/), [GitHub](https://github.com/taskforcesh/bullmq), and [Documentation](https://docs.bullmq.io/).
