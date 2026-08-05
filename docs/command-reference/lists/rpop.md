---
description:  Discover how to use Redis RPOP command to remove and fetch the last element of a list.
---
import PageTitle from '@site/src/components/PageTitle';
import Benchmark from '@site/src/components/Benchmark';

# RPOP

<PageTitle title="Redis RPOP Command (Documentation) | Dragonfly" />

## Syntax

    RPOP key [count]

**Time complexity:** O(N) where N is the number of elements returned

**ACL categories:** @write, @list, @fast

Removes and returns the last elements of the list stored at `key`.

By default, the command pops a single element from the end of the list.
When provided with the optional `count` argument, the reply will consist of up
to `count` elements, depending on the list's length.

## Return

When called without the `count` argument:

[Bulk string reply](https://valkey.io/topics/protocol/#bulk-strings): the value of the last element, or `nil` when `key` does not exist.

When called with the `count` argument:

[Array reply](https://valkey.io/topics/protocol/#arrays): list of popped elements, or `nil` when `key` does not exist.

## Examples

```shell
dragonfly> RPUSH mylist "one" "two" "three" "four" "five"
(integer) 5
dragonfly> RPOP mylist
"five"
dragonfly> RPOP mylist 2
1) "four"
2) "three"
dragonfly> LRANGE mylist 0 -1
1) "one"
2) "two"
```

## Benchmark

<Benchmark
  command="RPOP"
  dragonflyOps={10670000}
  valkeyOps={1810000}
  redisOps={1490000}
  hardware="Server: m7g.8xlarge (arm64) · Client: c6gn.8xlarge (arm64)"
  tool="dfly_bench"
  client="32 threads, 5 connections, pipeline 30"
  dataset="1M lists, 100 items each, 128B values, uniform key distribution"
  duration="300s (10s warmup), 1 trial"
  measuredOn="2026-07-29"
  harnessPath="benchmarks/RPOP/dfly_bench/RPOP_reproduce.md"
  results={[
    { engine: "Dragonfly", throughput: "10.67M ops/s", p50: "0.416 ms", p99: "0.792 ms", p999: "3.282 ms", avgLatency: "0.437 ms" },
    { engine: "Valkey", throughput: "1.81M ops/s", p50: "1.532 ms", p99: "9.645 ms", p999: "11.570 ms", avgLatency: "2.639 ms" },
    { engine: "Redis", throughput: "1.49M ops/s", p50: "1.550 ms", p99: "11.361 ms", p999: "11.985 ms", avgLatency: "3.217 ms" },
  ]}
/>
