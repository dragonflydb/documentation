---
description: "Learn how to use Redis HGET command to retrieve the value of a hash field. Perfect for data fetching tasks."
---

import PageTitle from '@site/src/components/PageTitle';
import Benchmark from '@site/src/components/Benchmark';

# HGET

<PageTitle title="Redis HGET Command (Documentation) | Dragonfly" />

## Syntax

    HGET key field

**Time complexity:** O(1)

**ACL categories:** @read, @hash, @fast

Returns the value associated with `field` in the hash stored at `key`.

## Return

[Bulk string reply](https://valkey.io/topics/protocol/#bulk-strings): the value associated with `field`, or `nil` when `field` is not
present in the hash or `key` does not exist.

## Examples

```shell
dragonfly> HSET myhash field1 "foo"
(integer) 1
dragonfly> HGET myhash field1
"foo"
dragonfly> HGET myhash field2
(nil)
```

## Benchmark

<Benchmark
  command="HGET"
  dragonflyOps={9310000}
  valkeyOps={791800}
  redisOps={744400}
  hardware="Server: m7g.8xlarge (arm64) · Client: c6gn.8xlarge (arm64)"
  tool="dfly_bench"
  client="32 threads, 5 connections, pipeline 30"
  dataset="100M keys, 128B values, uniform key distribution"
  duration="60s (10s warmup), 1 trial"
  measuredOn="2026-07-28"
  harnessPath="benchmarks/HGET/dfly_bench/HGET_reproduce.md"
  results={[
    { engine: "Dragonfly", throughput: "9.31M ops/s", p50: "0.468 ms", p99: "0.875 ms", p999: "1.163 ms", avgLatency: "0.489 ms" },
    { engine: "Valkey", throughput: "791.8K ops/s", p50: "6.483 ms", p99: "6.990 ms", p999: "6.999 ms", avgLatency: "6.044 ms" },
    { engine: "Redis", throughput: "744.4K ops/s", p50: "6.522 ms", p99: "9.979 ms", p999: "13.329 ms", avgLatency: "6.429 ms" },
  ]}
/>
