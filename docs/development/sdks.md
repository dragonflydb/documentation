---
sidebar_position: 0
---

# SDKs

Your favorite Redis SDK or library should work as expected with Dragonfly as well. If you run in to any issues using a Redis SDK with Dragonfly please reach out via [Discord](https://discord.gg/HsPjXGVH85) or [get in touch with our team](https://www.dragonflydb.io/early-access).

# BullMQ

Dragonfly employs a share-nothing architecture to achieve while BullMQ relies on relies on Lua scripts to execute atomic operations across diverse keys. The integration of Dragonfly with BullMQ involves some specific configuration steps to ensure optimal performance and compatibility with Bull internals.

1. Run Dragonfly with the following flags --cluster_mode=emulated --lock_on_hashtags

2. Queue Naming Strategies: When setting up your application, use hash tags in your queue names. This can be done by initializing a queue as follows:

```shell
const queue = new Queue('{name}');
```

Alternatively, you can utilize the bull queue prefix feature:

```shell
const queue = new Queue('name', {
  prefix: '{myprefix}'
});
```

Ensuring Shard Consistency: By adopting the configuration mentioned above, queues that share the same hash tag will be assigned to the same Dragonfly shard. This ensures consistency and efficient resource utilization.

3. Queue Dependencies: If you have queue dependencies, especially a parent-child relationship, it's important to use the same hash tag for both queues. This ensures that they are processed within the same Dragonfly shard and maintains the integrity of the dependencies.

4. Enhancing Application Performance: To achieve heightened performance for your application, consider employing a larger number of queues. By distributing the queues across distinct Dragonfly shards, you can optimize the utilization of the Dragonfly architecture efficiently.
