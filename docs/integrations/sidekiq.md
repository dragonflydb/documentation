---
sidebar_position: 4
description: Sidekiq
---

# Sidekiq

## Introduction


Sidekiq is a background processing system that is built on top of Redis. The former executes jobs asynchronously and the latter serves as the backend.
Sidekiq clients push jobs into a Dragonfly list and Sidekiq processes pop jobs from that list and execute them. The unit of parallelism for
Sidekiq is the list (referenced as Queue in Sidekiq lingo) and the way to scale Sidekiq involves creating multiple queues.

Dragonfly is highly compatible with Redis and Sidekiq use cases map nicely to the Dragonfly's multi threaded architecture. By replacing Redis with Dragonfly, 
you can achieve superior performance and scalability for your Sidekiq applications.

## Running Sidekiq with Dragonfly

Integration with Sidekiq is seamless. Run Dragonfly and Sidekiq and it will work outside of the box. However, to utilize Dragonfly's multi-threaded 
architecture you need to distribute queues equally among the number of shard threads available.

### 1. Parallelization and load balancing

To increase parallelism and load balance your application you need to change the default way of how Dragonfly distributes its keys 
among the available shard threads. It's therefore advised to configure Dragonfly with `--shard_round_robin_prefix=QUEUE_PREFIX`. With this configuration
Dragonfly equally spreads the Sidekiq queues (lists) among the available shard threads. Replace `QUEUE_PREFIX` with the prefix name of the Sidekiq queues. 
For example, if your queues are named `queue:1, queue:2, queue:3, queue:n` then replace `QUEUE_PREFIX` with `queue`.

## Useful Resources

- BullMQ [Homepage](https://sidekiq.org/), [](https://github.com/sidekiq/sidekiq), and [Documentation](https://github.com/sidekiq/sidekiq/wiki).
