---
sidebar_position: 3
---

# Benchmarking Dragonfly

Dragonfly is a high-performance, distributed key-value store designed for scalability
and low latency. It's a drop-in replacement for Redis 6.x and memcached servers.
This document outlines a benchmarking methodology and results achieved using Dragonfly
with the `memtier_benchmark` load testing tool.

We benchmarked Dragonfly using the [memtier_benchmark](https://github.com/RedisLabs/memtier_benchmark)
load testing tool.
A prebuilt container is also available on [Docker Hub](https://hub.docker.com/r/redislabs/memtier_benchmark/)
Although Redis offers the `redis-benchmark` tool in its repository, it has not been as efficient
as `memtier_benchmark` and it often becomes the bottleneck instead of Dragonfly.

We also developed our own tool [dfly_bench](https://github.com/dragonflydb/dragonfly/blob/main/src/server/dfly_bench.cc),
which can be built from source in the Dragonfly repository.


## Methodology
- **Remote Deployment:** Dragonfly is a multi-threaded server designed to run remotely.
Therefore, we recomment running the load testing client and server on separate machines for a more accurate representation of real-world performance.
- **Minimizing Latency:** Locate client and server within the same Availability Zone and use private IPs for optimal network performance. If you benchmark in the AWS cloud, consider an AWS Cluster placement group
for the lowest possible latency. The rationale behind this - to remove any environmental factors
that might skew the test results.
- **Server vs. Client Resources**: Use a more powerful instance for the load testing client
to avoid client-side bottlenecks.

The remainder of this document will discuss how to set up a benchmark in the AWS cloud
to observe millions of QPS from a single instance.

## Load testing configuration
We used Dragonfly v1.15.0 (latest at the time of writing) with the following arguments:
`./dragonfly --logtostderr  --dbfilename=`

Please notice that Dragonfly uses of all the available vCPUs by default on the server.
If you want to control explicitly number of threads in Dragonfly you can add `--proactor_threads=<N>`.
Both the client and server instances run `Ubuntu 23.04` OS with kernel version 6.2.
In line with our recommendations above, we used internal IPs for connecting and
used stronger `c7gn.16xlarge` instance with 64 vCPUs for the load-testing program.

## Dragongly on `c6gn.12xlarge`

### Write-only test
On the loadtest instance (c7gn.16xlarge with 64 vCPUs) we run:
`memtier_benchmark -s $SERVER_PRIVATE_IP --distinct-client-seed --hide-histogram --ratio 1:0 -t 60 -c 20 -n 200000`

The run ended with the following summary:

```
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets      4195628.23          ---          ---         0.39283         0.37500         0.68700         2.54300    323231.06

```

In this test, we reached almost 4.2M queries per second (QPS) with the average latency of
392us between the `memtier_benchmark` and Dragonfly. Consequently, the P50 latency was 375us, P99 - 687us
and P99.9 was 2543us. It is a very short and simple test, but it still gives some perspective
about the performance of Dragonfly.

### Reads-only test
Without flushing the database, we run the following command:
`memtier_benchmark -s $SERVER_PRIVATE_IP --distinct-client-seed --hide-histogram --ratio 0:1 -t 60 -c 20 -n 200000`

Note that the ratio changed to "1:0.

```
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Gets      4109802.84   4109802.84         0.00         0.40126         0.38300         0.67900         0.90300    296551.68
```

We can observe that both `Ops` and `Hits` are the same, meaning all of the GET requests
coming from the load test hit the existing keys.
Dragonfly responded with returning values for each request and its average QPS was 4.1M qps,
with P99.9 latency - 903us.

### Read test with pipelining

Here's another way to loadtest Dragonfly. This one is sending SETs with pipeline of batch size 10:
`memtier_benchmark -s $SERVER_PRIVATE_IP --ratio 0:1 -t 60 -c 5  -n 200000  --distinct-client-seed --hide-histogram --pipeline=10`

```
ALL STATS
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Gets      7083583.57   7083583.57         0.00         0.45821         0.44700         0.69500         1.53500    511131.14
```

During the pipelining mode, memtier_benchmark sends `K` requests in batch without before waiting
for them to complete. In this case, `K` is `10`. Pipelining reduces the CPU load spent
in the networking stack, and as a result, Dragonfly can reach 7M qps with sub-millisecond latency.
Please note, that for real world usecases, pipelining requires cooperation of a client side app,
which must send multiple requests on a single connection before waiting for the server to respond.

Some asynchronous client libraries like `StackExchange.Redis` or `ioredis` allow multiplexing requests
on a single connection. They can still provide a simplified synchronous interface to their users while
benefitting from performance improvements of pipelining.

## Load testing Dragonfly `c7gn.12xlarge`

Next thing we tried running Dragonfly on the next generation instance with the same number of vCPUs (48).
We used the same `c7gn.16xlarge` for running `memtier_benchmark` and we used the same commands
to test writes, reads and pipelined reads:

| Test          | Ops/sec   | Avg. Latency (us) | P99.9 Latency (us) |
|---------------|-----------|-------------------|--------------------|
| Write-Only    | 5.2M      | 250               | 631                |
| Read-Only     | 6M        | 271               | 623                |
| Pipelined Read| 8.9M      | 323               | 839                |


### Writes
`memtier_benchmark -s $SERVER_PRIVATE_IP --distinct-client-seed --hide-histogram --ratio 1:0 -t 60 -c 20 -n 200000`

```
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets      5195097.56          ---          ---         0.26012         0.24700         0.49500         0.63100    400230.15
```

### Reads
`memtier_benchmark -s $SERVER_PRIVATE_IP --distinct-client-seed --hide-histogram --ratio 0:1 -t 60 -c 20 -n 200000`
```
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Gets      6078632.89   6078632.89         0.00         0.27177         0.26300         0.49500         0.62300    438616.86
```

### Pipelined Reads
`memtier_benchmark -s $SERVER_PRIVATE_IP --ratio 0:1 -t 60 -c 5  -n 200000  --distinct-client-seed --hide-histogram --pipeline=10`

```
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Gets      8975121.86   8975121.86         0.00         0.32325         0.31100         0.52700         0.83900    647619.14
```


## Comparison with Garnet
Microsoft Research recently released Garnet ([https://github.com/microsoft/garnet]),
a remote cache store. Due to interest within the Dragonfly community, we decided to compare
Garnet's performance with Dragonfly's. This comparison focuses on performance results
and does not delve into architectural differences or Redis compatibility implications.

<i>Note: Unfortunately, Garnet does not have aarch64 build available,
therefore we run both Garnet and Dragonfly on x86_64 server
`c6in.12xlarge`. We run Garnet via docker with host networking enabled via
`docker run --network=host ghcr.io/romange/garnet:latest --port=6379` command.
The docker container was built using the Garnet docker build file for ubuntu, located in their
repository.</i>

### Garnet on `c6in.12xlarge`

Similarly to previous tests we run `memtier_benchmark` on `c7gn.16xlarge` with `cluster`
placement policy for both instances. For writes we used the following command:

```
memtier_benchmark -s $SERVER_PRIVATE_IP --distinct-client-seed --hide-histogram --ratio 1:0 -t 60 -c 20 -n 200000
```

Similarly, for reads we used
```
memtier_benchmark -s $SERVER_PRIVATE_IP --distinct-client-seed --hide-histogram --ratio 0:1 -t 60 -c 20 -n 200000
```

and for pipelined reads we used

```
memtier_benchmark -s $SERVER_PRIVATE_IP --ratio 0:1 -t 60 -c 5  -n 2000000  --distinct-client-seed --hide-histogram --pipeline=10
```

Note that we increased number of requests to `2000000` per client connection in the latter case.

**Results**:

| Test          | Ops/sec   | Avg. Latency (us) | P99.9 Latency (us) |
|---------------|-----------|-------------------|--------------------|
| Write-Only    | 3.5M      | 346               | 4287               |
| Read-Only     | 3.7M      | 327               | 2623               |
| Pipelined Read| 25.4M !!! | 119               | 375                |


The interesting part is around pipelined reads, where Garnet scaled linearly to more than 25M qps
which is a really impressive performance.

On the other hand, a curious and random finding - a single "dbsize" command took 3 seconds
to run on Garnet.

### Dragonfly on `c6in.12xlarge`

We run Dragonfly on the same instances with the same test configurations.
Below are the results for Dragonfly.

| Test          | Ops/sec   | Avg. Latency (us) | P99.9 Latency (us) |
|---------------|-----------|-------------------|--------------------|
| Write-Only    | 3.6M      | 291               | 6815               |
| Read-Only     | 5.1M      | 299               | 7615               |
| Pipelined Read| 6.9M      | 358               | 1127               |

As you can see Dragonfly shows a comparable throughput for non-pipelined access,
but its P99.9 was worse. For pipelined commands, Dragonfly had x3.7 less throughput than Garnet.