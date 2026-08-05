---
description: "Learn the Redis TTL command to get remaining time-to-live of a key."
---

import PageTitle from '@site/src/components/PageTitle';
import Benchmark from '@site/src/components/Benchmark';

# TTL

<PageTitle title="Redis TTL Command (Documentation) | Dragonfly" />

## Syntax

    TTL key

**Time complexity:** O(1)

**ACL categories:** @keyspace, @read, @fast

Returns the remaining time to live of a key that has a timeout.
This introspection capability allows a Dragonfly client to check how many seconds a
given key will continue to be part of the dataset.

## Return

[Integer reply](https://valkey.io/topics/protocol/#integers): TTL in seconds, or a negative value in order to signal an error.

- The command returns `-2` if the key does not exist.
- The command returns `-1` if the key exists but has no associated expire.

## Examples

```shell
dragonfly> SET mykey "Hello"
OK
dragonfly> EXPIRE mykey 10
(integer) 1
dragonfly> TTL mykey
(integer) 10
```

## Benchmark

<Benchmark
  command="TTL"
  dragonflyOps={10630000}
  valkeyOps={2330000}
  redisOps={1940000}
  hardware="Server: m7g.8xlarge (arm64) · Client: c6gn.8xlarge (arm64)"
  tool="dfly_bench"
  client="32 threads, 5 connections, pipeline 30"
  dataset="100M keys, 128B values, uniform key distribution"
  duration="60s (10s warmup), 1 trial"
  measuredOn="2026-07-29"
  harnessPath="benchmarks/TTL/dfly_bench/TTL_reproduce.md"
  results={[
    { engine: "Dragonfly", throughput: "10.63M ops/s", p50: "0.411 ms", p99: "0.851 ms", p999: "1.076 ms", avgLatency: "0.439 ms" },
    { engine: "Valkey", throughput: "2.33M ops/s", p50: "2.225 ms", p99: "2.495 ms", p999: "2.499 ms", avgLatency: "2.049 ms" },
    { engine: "Redis", throughput: "1.94M ops/s", p50: "2.325 ms", p99: "2.980 ms", p999: "3.000 ms", avgLatency: "2.462 ms" },
  ]}
/>
