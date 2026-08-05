---
description: "Learn how to use Redis HSET command to set the value of a hash field. A fundamental function for data update tasks."
---

import PageTitle from '@site/src/components/PageTitle';
import Benchmark from '@site/src/components/Benchmark';

# HSET

<PageTitle title="Redis HSET Command (Documentation) | Dragonfly" />

## Syntax

    HSET key field value [field value ...]

**Time complexity:** O(1) for each field/value pair added, so O(N) to add N field/value pairs when the command is called with multiple field/value pairs.

**ACL categories:** @write, @hash, @fast

Sets the specified fields to their respective values in the hash stored at `key`.

This command overwrites the values of specified fields that exist in the hash.
If `key` doesn't exist, a new key holding a hash is created.

## Return

[Integer reply](https://valkey.io/topics/protocol/#integers): The number of fields that were added.

## Examples

```shell
dragonfly> HSET myhash field1 "Hello"
(integer) 1
dragonfly> HGET myhash field1
"Hello"
dragonfly> HSET myhash field2 "Hi" field3 "World"
(integer) 2
dragonfly> HGET myhash field2
"Hi"
dragonfly> HGET myhash field3
"World"
dragonfly> HGETALL myhash
1) "field1"
2) "Hello"
3) "field2"
4) "Hi"
5) "field3"
6) "World"
```

<!-- benchmark:start -->
## Benchmark

<Benchmark
  command="HSET"
  dragonflyOps={7990000}
  valkeyOps={704000}
  redisOps={638500}
  hardware="Server: m7g.8xlarge (arm64) · Client: c6gn.8xlarge (arm64)"
  tool="dfly_bench"
  client="32 threads, 5 connections, pipeline 30"
  dataset="100M keys, 128B values, uniform key distribution"
  duration="300s (10s warmup), 1 trial"
  measuredOn="2026-07-29"
  harnessPath="benchmarks/HSET/dfly_bench/HSET_reproduce.md"
  results={[
    { engine: "Dragonfly", throughput: "7.99M ops/s", p50: "0.507 ms", p99: "1.985 ms", p999: "7.332 ms", avgLatency: "0.583 ms" },
    { engine: "Valkey", throughput: "704.0K ops/s", p50: "6.573 ms", p99: "13.470 ms", p999: "17.760 ms", avgLatency: "6.804 ms" },
    { engine: "Redis", throughput: "638.5K ops/s", p50: "6.839 ms", p99: "11.613 ms", p999: "18.655 ms", avgLatency: "7.503 ms" },
  ]}
/>
<!-- benchmark:end -->
