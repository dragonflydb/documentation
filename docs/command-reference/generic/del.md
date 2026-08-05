---
description: "Learn how to use Redis DEL command to delete a key."
---

import PageTitle from '@site/src/components/PageTitle';
import Benchmark from '@site/src/components/Benchmark';

# DEL

<PageTitle title="Redis DEL Command (Documentation) | Dragonfly" />

## Syntax

    DEL key [key ...]

**Time complexity:** O(N) where N is the number of keys that will be removed. When a key to remove holds a value other than a string, the individual complexity for this key is O(M) where M is the number of elements in the list, set, sorted set or hash. Removing a single key that holds a string value is O(1).

**ACL categories:** @keyspace, @write, @slow

Removes the specified keys.
A key is ignored if it does not exist.

## Return

[Integer reply](https://valkey.io/topics/protocol/#integers): The number of keys that were removed.

## Examples

```shell
dragonfly> SET key1 "Hello"
OK
dragonfly> SET key2 "World"
OK
dragonfly> DEL key1 key2 key3
(integer) 2
```

<!-- benchmark:start -->
## Benchmark

<Benchmark
  command="DEL"
  dragonflyOps={10250000}
  valkeyOps={2380000}
  redisOps={1960000}
  hardware="Server: m7g.8xlarge (arm64) · Client: c6gn.8xlarge (arm64)"
  tool="dfly_bench"
  client="32 threads, 5 connections, pipeline 30"
  dataset="100M keys, 128B values, uniform key distribution"
  duration="300s (10s warmup), 1 trial"
  measuredOn="2026-07-28"
  harnessPath="benchmarks/DEL/dfly_bench/DEL_reproduce.md"
  results={[
    { engine: "Dragonfly", throughput: "10.25M ops/s", p50: "0.445 ms", p99: "0.822 ms", p999: "1.131 ms", avgLatency: "0.456 ms" },
    { engine: "Valkey", throughput: "2.38M ops/s", p50: "1.759 ms", p99: "3.992 ms", p999: "4.461 ms", avgLatency: "2.008 ms" },
    { engine: "Redis", throughput: "1.96M ops/s", p50: "2.255 ms", p99: "6.612 ms", p999: "7.977 ms", avgLatency: "2.439 ms" },
  ]}
/>
<!-- benchmark:end -->
