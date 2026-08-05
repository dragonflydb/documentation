---
description:  Learn how to use the Redis LPOP command for removing and getting the first element in the list.
---
import PageTitle from '@site/src/components/PageTitle';
import Benchmark from '@site/src/components/Benchmark';

# LPOP

<PageTitle title="Redis LPOP Command (Documentation) | Dragonfly" />

## Syntax

    LPOP key [count]

**Time complexity:** O(N) where N is the number of elements returned

**ACL categories:** @write, @list, @fast

Removes and returns the first elements of the list stored at `key`.

By default, the command pops a single element from the beginning of the list.
When provided with the optional `count` argument, the reply will consist of up
to `count` elements, depending on the list's length.

## Return

When called without the `count` argument:

[Bulk string reply](https://valkey.io/topics/protocol/#bulk-strings): the value of the first element, or `nil` when `key` does not exist.

When called with the `count` argument:

[Array reply](https://valkey.io/topics/protocol/#arrays): list of popped elements, or `nil` when `key` does not exist.

## Examples

```shell
dragonfly> RPUSH mylist "one" "two" "three" "four" "five"
(integer) 5
dragonfly> LPOP mylist
"one"
dragonfly> LPOP mylist 2
1) "two"
2) "three"
dragonfly> LRANGE mylist 0 -1
1) "four"
2) "five"
```

## Benchmark

<Benchmark
  command="LPOP"
  dragonflyOps={10250000}
  valkeyOps={1690000}
  redisOps={1330000}
  hardware="Server: m7g.8xlarge (arm64) · Client: c6gn.8xlarge (arm64)"
  tool="dfly_bench"
  client="32 threads, 5 connections, pipeline 30"
  dataset="1M lists, 100 items each, 128B values, uniform key distribution"
  duration="300s (10s warmup), 1 trial"
  measuredOn="2026-07-29"
  harnessPath="benchmarks/LPOP/dfly_bench/LPOP_reproduce.md"
  results={[
    { engine: "Dragonfly", throughput: "10.25M ops/s", p50: "0.432 ms", p99: "0.871 ms", p999: "3.507 ms", avgLatency: "0.456 ms" },
    { engine: "Valkey", throughput: "1.69M ops/s", p50: "1.535 ms", p99: "10.042 ms", p999: "11.804 ms", avgLatency: "2.822 ms" },
    { engine: "Redis", throughput: "1.33M ops/s", p50: "1.562 ms", p99: "11.894 ms", p999: "13.783 ms", avgLatency: "3.588 ms" },
  ]}
/>
