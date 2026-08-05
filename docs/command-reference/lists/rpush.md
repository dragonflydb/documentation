---
description:  Learn how to use Redis RPUSH command for appending a value at the end of a list.
---
import PageTitle from '@site/src/components/PageTitle';
import Benchmark from '@site/src/components/Benchmark';

# RPUSH

<PageTitle title="Redis RPUSH Command (Documentation) | Dragonfly" />

## Syntax

    RPUSH key element [element ...]

**Time complexity:** O(1) for each element added, so O(N) to add N elements when the command is called with multiple arguments.

**ACL categories:** @write, @list, @fast

Insert all the specified values at the tail of the list stored at `key`.
If `key` does not exist, it is created as empty list before performing the push
operation.
When `key` holds a value that is not a list, an error is returned.

It is possible to push multiple elements using a single command call just
specifying multiple arguments at the end of the command.
Elements are inserted one after the other to the tail of the list, from the
leftmost element to the rightmost element.
So for instance the command `RPUSH mylist a b c` will result into a list
containing `a` as first element, `b` as second element and `c` as third element.

## Return

[Integer reply](https://valkey.io/topics/protocol/#integers): the length of the list after the push operation.

## Examples

```shell
dragonfly> RPUSH mylist "hello"
(integer) 1
dragonfly> RPUSH mylist "world"
(integer) 2
dragonfly> LRANGE mylist 0 -1
1) "hello"
2) "world"
```

<!-- benchmark:start -->
## Benchmark

<Benchmark
  command="RPUSH"
  dragonflyOps={5990000}
  valkeyOps={893500}
  redisOps={698800}
  hardware="Server: m7g.8xlarge (arm64) · Client: c6gn.8xlarge (arm64)"
  tool="dfly_bench"
  client="32 threads, 5 connections, pipeline 30"
  dataset="100M keys, 128B values, uniform key distribution"
  duration="300s (10s warmup), 1 trial"
  measuredOn="2026-07-29"
  harnessPath="benchmarks/RPUSH/dfly_bench/RPUSH_reproduce.md"
  results={[
    { engine: "Dragonfly", throughput: "5.99M ops/s", p50: "0.531 ms", p99: "5.922 ms", p999: "11.373 ms", avgLatency: "0.782 ms" },
    { engine: "Valkey", throughput: "893.5K ops/s", p50: "5.197 ms", p99: "11.570 ms", p999: "15.476 ms", avgLatency: "5.359 ms" },
    { engine: "Redis", throughput: "698.8K ops/s", p50: "6.573 ms", p99: "11.298 ms", p999: "17.824 ms", avgLatency: "6.856 ms" },
  ]}
/>
<!-- benchmark:end -->
