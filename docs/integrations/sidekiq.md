---
sidebar_position: 4
description: Sidekiq
---

# Sidekiq

**Note:** Dragonfly v1.13+ is required for this integration.

## Introduction

Sidekiq is a background job processing system that is built for Ruby and originally used Redis as its backend store.
Sidekiq clients push jobs into one or more Redis lists, and the Sidekiq server pops jobs from those lists and executes them.
The unit of parallelism for Sidekiq is the list (referenced as a queue in Sidekiq lingo), and the way to scale Sidekiq involves creating multiple queues.

Dragonfly is highly compatible with Redis, and Sidekiq use cases map nicely to the Dragonfly's multi-threaded architecture.
By replacing Redis with Dragonfly, you can achieve superior performance and scalability for your Sidekiq applications.

## Running Sidekiq with Dragonfly

Integration with Sidekiq is seamless. Run Dragonfly and Sidekiq, and they will work together out of the box.
However, to utilize Dragonfly's multi-threaded architecture, you need to distribute queues equally among the number of Dragonfly shard threads available.

### 1. Dragonfly Initialization

There are several options available to [get Dragonfly up and running quickly](../getting-started/getting-started.md).
Assuming you have a local Dragonfly binary, you can run Dragonfly with the following flags:

```bash
$> ./dragonfly --bind localhost --port 6379 --shard_round_robin_prefix={QUEUE_PREFIX}
```

### 2. Sidekiq Configuration

Detailed instructions on how to configure Sidekiq with its backend store can be found [here](https://github.com/sidekiq/sidekiq/wiki/Using-Redis).
Since Dragonfly is highly compatible with Redis, just make sure to use the Dragonfly server address and port (i.e., `localhost:6379` for the local Dragonfly instance above) in the Sidekiq configuration.

### 3. Parallelization & Load Balancing

To increase parallelism and load balance in your application, you need to change the default way Dragonfly distributes its keys among the available shard threads.
It's therefore advised to configure Dragonfly with the `shard_round_robin_prefix` flag.
With this configuration, Dragonfly equally spreads the Sidekiq queues (lists) among the available shard threads.
Replace `QUEUE_PREFIX` with the prefix name of the Sidekiq queues.
For example, if your queues are named `my_queue:1`, `my_queue:2`, `my_queue:3`, etc., then replace `QUEUE_PREFIX` with `my_queue`.

## Useful Resources

- Sidekiq [Homepage](https://sidekiq.org/), [GitHub](https://github.com/sidekiq/sidekiq), and [Documentation](https://github.com/sidekiq/sidekiq/wiki).
- Sidekiq also has a dedicated documentation page on [Using Dragonfly](https://github.com/sidekiq/sidekiq/wiki/Using-Dragonfly).
