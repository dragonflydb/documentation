---
sidebar_position: 1
description: Sidekiq
---

# Sidekiq

**Note:** Dragonfly v1.13+ is required for this integration.

## Introduction

Sidekiq is a background job processing system that is built for Ruby and originally used Redis as its backend store.
Sidekiq clients push jobs into one or more Valkey lists, and the Sidekiq server pops jobs from those lists and executes them.
The unit of parallelism for Sidekiq is the list (referenced as a queue in Sidekiq lingo), and the way to scale Sidekiq involves creating multiple queues.

Dragonfly is highly compatible with Valkey, and Sidekiq use cases map nicely to the Dragonfly's multi-threaded architecture.
By replacing Valkey with Dragonfly, you can achieve superior performance and scalability for your Sidekiq applications.

## Running Sidekiq with Dragonfly

Sidekiq works with Dragonfly out of the box. Point Sidekiq at Dragonfly instead of Valkey, and optionally enable
`--shard_sidekiq_queues` to keep queue operations on a single Dragonfly shard thread.

### 1. Dragonfly Initialization

There are several options available to [get Dragonfly up and running quickly](../getting-started/getting-started.md).
Assuming you have a local Dragonfly binary, run:

```bash
$> ./dragonfly --bind localhost --port 6379 --shard_sidekiq_queues
```

### 2. Sidekiq Configuration

Follow the [Sidekiq backend configuration guide](https://github.com/sidekiq/sidekiq/wiki/Using-Redis),
using the Dragonfly address and port (i.e., `localhost:6379` for the instance above).

### 3. Queue Sharding

Dragonfly assigns each key to a shard thread by hashing the key name.
An operation that touches keys on different shards requires a multi-shard transaction, which increases latency compared to a single-shard one.

[Sidekiq Pro `super_fetch`](https://github.com/sidekiq/sidekiq/wiki/Reliability) moves each job
with `LMOVE` from the public queue `queue:<name>` to a per-process private queue `queue:sq|<identity>|<name>`.
Hashed by the full key name, these two keys usually land on different shards.

With `--shard_sidekiq_queues`, Dragonfly hashes keys matching `<prefix>queue:<name>` and `<prefix>queue:sq|<identity>|<name>`
by `<name>` only. A queue and its private queues then share a shard, and each `super_fetch` `LMOVE` runs on a single shard.
Different queues are spread across shards by the hash of their names, so use multiple queues to make use of all Dragonfly threads.

The flag applies to any key containing `queue:`, not only Sidekiq keys. For example, `job_queue:123:data` is sharded by `123:data`.
This only changes shard placement, not behavior.

Dragonfly takes the queue name from after the last `queue:` in the key, and for a private queue, from after the last `|`.
As a result, a queue and its private queues are sharded by different names, and usually land on different shards, if:

- the queue name contains `|`, or
- the Sidekiq process identity (`<hostname>:<pid>:<nonce>`) contains `queue:`, i.e., the hostname ends in `queue`.

When hashtags determine sharding (`--cluster_mode` or `--lock_on_hashtags`), a key containing a hashtag is sharded by
its first hashtag instead. For example, `queue:{mail}` and `queue:sq|<identity>|{mail}` are both sharded by `mail`.
In `--cluster_mode`, cluster clients reject an `LMOVE` between keys in different slots, so give each queue name a hashtag
(e.g., `{mail}`) to keep the public and private queues in the same slot.

The flag has no effect when `--cluster_mode` is set together with `--experimental_cluster_shard_by_slot`.

## Useful Resources & Benchmarks

- Sidekiq [Homepage](https://sidekiq.org/), [GitHub](https://github.com/sidekiq/sidekiq), and [Documentation](https://github.com/sidekiq/sidekiq/wiki).
- Sidekiq also has a dedicated documentation page on [Using Dragonfly](https://github.com/sidekiq/sidekiq/wiki/Using-Dragonfly).
- Read our blog post [Running and Optimizing Sidekiq Workloads with Dragonfly](https://www.dragonflydb.io/blog/running-sidekiq-with-dragonfly)
  with internal implementation details and performance benchmarks.
