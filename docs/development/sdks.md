---
sidebar_position: 0
---

# SDKs

Your favorite Redis SDK or library should work as expected with Dragonfly as well. If you run in to any issues using a Redis SDK with Dragonfly please reach out via [Discord](https://discord.gg/HsPjXGVH85) or [get in touch with our team](https://www.dragonflydb.io/early-access).

# [BullMQ](https://docs.bullmq.io/)

The integration of Dragonfly with BullMQ involves some specific configuration steps to ensure optimal performance and compatibility with BullMQ internals.

BullMQ extensively uses Lua scripts (server side scripting) for executing commands in Redis.
When running a Lua script in Redis, it's essential to explicitly specify all the keys the script will access.
However, BullMQ's design doesn't allow it to predict in advance which keys its Lua scripts will need.
Although accessing undeclared keys is unsupported in Redis, it nonetheless works.
However, in Dragonfly it cannot work out of the box due to our multi-threaded transactional framework.

As such, one could run Dragonfly with Lua global transaction mode:

```
dragonfly --default_lua_flags=allow-undeclared-keys
```

This mode locks the entire data-store for each Lua script. In other words, it is slow, but it is safe and does not require any changes from the code that uses BullMQ.

To utilize Dragonfly's multi-threaded performance and achieve superior performance for your application, we introduce a mode that enables locks on hash tags instead of individual keys.
In this mode each BullMQ queue will be exclusively owned by a single thread, and accessing multiple queues could be done in parallel.
To employ Dragonfly in this mode, please follow the provided guide:

1. Run Dragonfly with the following flags

```
dragonfly -cluster_mode=emulated --lock_on_hashtags
```

2. Queue Naming Strategies: When setting up your application, use hash tags in your queue names. This can be done by initializing a queue as follows:

```javascript
const queue = new Queue("{name}");
```

Alternatively, you can utilize the bull queue prefix feature:

```javascript
const queue = new Queue("name", {
  prefix: "{myprefix}",
});
```

Ensuring Shard Consistency: By adopting the configuration mentioned above, queues that share the same hash tag will be assigned to the same Dragonfly thread. This ensures consistency and efficient resource utilization.

3. Queue Dependencies: If you have queue dependencies, especially a parent-child relationship, it's important to use the same hash tag for both queues. This ensures that they are processed within the same Dragonfly thread and maintains the integrity of the dependencies.

4. Enhancing Application Performance: To achieve superior performance for your application, consider employing a larger number of queues with different hashtag for each. By distributing the queues across distinct Dragonfly threads, you can optimize the utilization of the Dragonfly architecture efficiently.
