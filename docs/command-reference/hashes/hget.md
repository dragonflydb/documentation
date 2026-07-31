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
/>
