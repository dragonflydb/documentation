---
description:  Learn how to use Redis LPUSH command to insert an element at the start of a list.
---
import PageTitle from '@site/src/components/PageTitle';
import Benchmark from '@site/src/components/Benchmark';

# LPUSH

<PageTitle title="Redis LPUSH Command (Documentation) | Dragonfly" />

## Syntax

    LPUSH key element [element ...]

**Time complexity:** O(1) for each element added, so O(N) to add N elements when the command is called with multiple arguments.

**ACL categories:** @write, @list, @fast

Insert all the specified values at the head of the list stored at `key`.
If `key` does not exist, it is created as empty list before performing the push
operations.
When `key` holds a value that is not a list, an error is returned.

It is possible to push multiple elements using a single command call just
specifying multiple arguments at the end of the command.
Elements are inserted one after the other to the head of the list, from the
leftmost element to the rightmost element.
So for instance the command `LPUSH mylist a b c` will result into a list
containing `c` as first element, `b` as second element and `a` as third element.

## Return

[Integer reply](https://valkey.io/topics/protocol/#integers): the length of the list after the push operations.

## Examples

```shell
dragonfly> LPUSH mylist "world"
(integer) 1
dragonfly> LPUSH mylist "hello"
(integer) 2
dragonfly> LRANGE mylist 0 -1
1) "hello"
2) "world"
```

<!-- benchmark:start -->
## Benchmark

<Benchmark
  command="LPUSH"
  dragonflyOps={6020000}
  valkeyOps={866300}
  redisOps={661900}
  hardware="Server: m7g.8xlarge (arm64) · Client: c6gn.8xlarge (arm64)"
  tool="dfly_bench"
  client="32 threads, 5 connections, pipeline 30"
  dataset="100M keys, 128B values, uniform key distribution"
  duration="300s (10s warmup), 1 trial"
  measuredOn="2026-07-29"
  harnessPath="benchmarks/LPUSH/dfly_bench/LPUSH_reproduce.md"
  results={[
    { engine: "Dragonfly", throughput: "6.02M ops/s", p50: "0.525 ms", p99: "5.972 ms", p999: "11.560 ms", avgLatency: "0.778 ms" },
    { engine: "Valkey", throughput: "866.3K ops/s", p50: "5.416 ms", p99: "11.628 ms", p999: "15.410 ms", avgLatency: "5.528 ms" },
    { engine: "Redis", throughput: "661.9K ops/s", p50: "7.110 ms", p99: "11.702 ms", p999: "18.645 ms", avgLatency: "7.239 ms" },
  ]}
/>
<!-- benchmark:end -->
