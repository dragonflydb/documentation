---
sidebar_position: 1
description: BullMQ
---

# BullMQ

## Introduction

BullMQ is a Node.js library that implements a fast and robust queue system built on top of Redis that helps in resolving many modern-age architectures of microservices.

Since Dragonfly is highly compatible with Redis, BullMQ can be used with Dragonfly with zero or minimal code changes.
By replacing Redis with Dragonfly, you can achieve superior performance and scalability for your BullMQ application.

## TL;DR

If you can use [hashtags](https://redis.io/docs/latest/operate/oss_and_stack/reference/cluster-spec/#hash-tags) in your queue names or prefixes (e.g., use `{queue1}` instead of `queue1`),
add the following flags. This will enhance the performance of your BullMQ workloads.

```bash
$> ./dragonfly --cluster_mode=emulated --lock_on_hashtags
```

Otherwise, you would have to run Dragonfly with the following flag to allow accessing undeclared keys from Lua scripts, **but this will slow things down considerably**.

```bash
$> ./dragonfly --default_lua_flags=allow-undeclared-keys
```

That's all you need to know to run BullMQ with Dragonfly.
If you want to learn more about the details of the server flags used above, please continue reading the sections below.

---

## Using Undeclared Keys (Not Optimized)

BullMQ extensively uses Lua scripts (server-side scripting) for executing commands in Redis.
When running a Lua script in Redis, it's essential to explicitly specify all the keys the script will access.
However, the design of BullMQ doesn't allow it to predict in advance which keys its Lua scripts will need.
Although accessing undeclared keys is unsupported in Redis, it nonetheless works.

In Dragonfly, accessing undeclared keys from scripts is disabled by default because unpredictability, atomicity, and multithreading don't mix well.
As such, one could run Dragonfly with the following flag:

```bash
$> ./dragonfly --default_lua_flags=allow-undeclared-keys
```

**However, it is very important to note that running Dragonfly with `--default_lua_flags=allow-undeclared-keys`
locks the entire data store for each Lua script execution and slows things down considerably.**
Thus, we suggest following the [Using Hashtags & Optimized Configurations](#using-hashtags--optimized-configurations) section below to
completely avoid the `allow-undeclared-keys` flag and achieve superior performance for your BullMQ application.

## Using Hashtags & Optimized Configurations

To utilize Dragonfly's multi-threaded capability and achieve superior performance for your application, we introduce a mode that enables locks on hashtags instead of individual keys.
In this mode, each BullMQ queue will be exclusively owned by a single thread, and accessing multiple queues could be done in parallel.
To employ Dragonfly in this mode, please follow the steps below.

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
as well as the Dragonfly emulated cluster mode [here](../managing-dragonfly/cluster-mode.md).

In order to use a hashtag in a queue name, you can initialize a queue as follows:

```javascript
import { Queue } from 'bullmq';

// Note the wrapping curly brackets in the queue name string.
//
// Dragonfly assigns this queue to a specific thread based on only the substring "myqueue",
// instead of the full queue name string "{myqueue}". Despite how your queue name is formatted,
// Dragonfly will only consider the substring "myqueue" as the hashtag.
//
// Also, do not confuse the curly brackets here with JavaScript template literals.
// These curly brackets are part of the queue name string that will be used by Dragonfly.
const queue = new Queue("{myqueue}");
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

However, because of this, if you use prefix hashtags, it is important to **use unique per-queue prefixes so that not all queues are handled by the same Dragonfly thread**.
See [Thread Balancing](#3-thread-balancing) below for more details.

You should always avoid using the same hashtag for all queues.
But sometimes, it is fine to strategically place certain queues on the same Dragonfly thread.
See [Queue Dependencies](#4-queue-dependencies) below for more details.

### 3. Thread Balancing

To achieve superior performance for your application, consider employing a larger number of queues with a different hashtag for each.
By distributing the queues across distinct Dragonfly threads, you can optimize the utilization of the Dragonfly architecture efficiently.

### 4. Queue Dependencies (Parent / Child)

If you have queue dependencies, especially a parent-child relationship, it's important to use the same hashtag for both queues.
This ensures that they are processed within the same Dragonfly thread and maintains the integrity of the dependencies.

## Useful Resources & Benchmarks

- BullMQ [Homepage](https://bullmq.io/), [GitHub](https://github.com/taskforcesh/bullmq), and [Documentation](https://docs.bullmq.io/).
- Read our blog post [How We Optimized Dragonfly to Get 30x Throughput with BullMQ](https://www.dragonflydb.io/blog/running-bullmq-with-dragonfly-part-2-optimization)
  with internal implementation details and performance benchmarks.
