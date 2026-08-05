---
description: Learn the proper use of Redis MSET to set multiple keys to multiple values simultaneously.
---

import PageTitle from '@site/src/components/PageTitle';
import Benchmark from '@site/src/components/Benchmark';

# MSET

<PageTitle title="Redis MSET Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `MSET` command is used to set multiple key-value pairs atomically in a single operation.
This means that either all the keys are set or none of them are, ensuring consistency across a set of operations.

The `MSET` command is a more efficient way to set multiple keys when compared to multiple calls to `SET`, as it minimizes the number of requests made to the database.

## Syntax

```shell
MSET key value [key value ...]
```

- **Time complexity:** O(N) where N is the number of keys to set.
- **ACL categories:** @write, @string, @slow

## Parameter Explanations

- `key`: The key to be set.
- `value`: The value to associate with the key.
- You can input multiple key-value pairs by repeating this `[key value]` pattern.

## Return Values

The `MSET` command always returns `OK` regardless of whether the keys already exist or not.
It will overwrite any existing keys with the provided values.

## Code Examples

### Basic Example

Set multiple key-value pairs:

```shell
dragonfly$> MSET key1 "value1" key2 "value2" key3 "value3"
OK
dragonfly$> GET key1
"value1"
dragonfly$> GET key2
"value2"
dragonfly$> GET key3
"value3"
```

### Overwriting Existing Keys

If any of the specified keys already exist, `MSET` will overwrite them:

```shell
dragonfly$> SET key1 "initial"
OK
dragonfly$> MSET key1 "new_value" key2 "additional_value"
OK
dragonfly$> GET key1
"new_value"
dragonfly$> GET key2
"additional_value"
```

### Atomic Operations with `MSET`

The atomic nature of the `MSET` command ensures that all keys are set together, providing consistency across values even in concurrent situations:

```shell
dragonfly$> MSET key1 "first_value" key2 "second_value" key3 "third_value"
OK

# Atomicity ensures these values are set together.
dragonfly$> MGET key1 key2 key3
1) "first_value"
2) "second_value"
3) "third_value"
```

## Benchmark

<Benchmark
  command="MSET"
  dragonflyOps={7420000}
  valkeyOps={1240000}
  redisOps={932900}
  hardware="Server: m7g.8xlarge (arm64) · Client: c6gn.8xlarge (arm64)"
  tool="dfly_bench"
  client="32 threads, 5 connections, pipeline 30"
  dataset="100M keys, 128B values, uniform key distribution"
  duration="300s (10s warmup), 1 trial"
  measuredOn="2026-07-28"
  harnessPath="benchmarks/MSET/dfly_bench/MSET_reproduce.md"
  results={[
    { engine: "Dragonfly", throughput: "7.42M ops/s", p50: "0.519 ms", p99: "3.193 ms", p999: "10.310 ms", avgLatency: "0.631 ms" },
    { engine: "Valkey", throughput: "1.24M ops/s", p50: "3.705 ms", p99: "11.262 ms", p999: "15.579 ms", avgLatency: "3.843 ms" },
    { engine: "Redis", throughput: "932.9K ops/s", p50: "4.390 ms", p99: "8.630 ms", p999: "15.157 ms", avgLatency: "5.132 ms" },
  ]}
/>

## Best Practices

- Use `MSET` when you need to update multiple keys at once, as it's more efficient than separate `SET` commands.
- Since `MSET` performs overwrite operations, ensure that overwriting values is intended in your use case.

## Common Mistakes

- Mixing up key-value pairs: Ensure that the number of arguments passed to `MSET` is even (each key must have a corresponding value).
- Assuming `MSET` will fail if any of the keys already exist; in fact, it does not check whether a key exists and will always overwrite the value.

## FAQs

### What happens if one of the keys already exists?

`MSET` will overwrite any existing key. It does not perform checks for existing values and does not provide a conditional setting mechanism.

### Can I use `MSET` without arguments?

No, you must provide at least one key-value pair. If the total number of arguments is not even, you will get a syntax error.

### How does `MSET` differ from `SET`?

While `SET` sets a single key-value pair, `MSET` allows you to set multiple key-value pairs in one atomic operation, which can be more efficient in batch updates. On the other hand, `SET` provides more options, such as `NX`, `EX`, and so forth, for more versatile operations on that single key.
