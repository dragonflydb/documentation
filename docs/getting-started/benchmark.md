---
sidebar_position: 3
---

# Benchmarking Dragonfly
We have been benchmarking Dragonfly using the [memtier_benchmark](https://github.com/RedisLabs/memtier_benchmark)
load testing tool.
There is also a prebuilt container, available on [Docker Hub](https://hub.docker.com/r/redislabs/memtier_benchmark/)
While Redis offers the `redis-benchmark` tool in its repository, it has not been as efficient
as memtier_benchmark and it requires more connections to load Dragonfly.

Finally, we have developed our own tool [dfly_bench](https://github.com/dragonflydb/dragonfly/blob/main/src/server/dfly_bench.cc), which can be built from source in Dragonfly repository.


## Methodology
Dragonfly is a multi-threaded beast designed to run remotely.
Therefore, we recommend benchmarking it by running the load test and the server on separate machines.

If your goal is to test the scalability of the software under test, in this case Dragonfly,
it's advisable to remove any factors that might "level the playing field" compared to other software implementations.

For instance, to minimize the impact of environment and network latency, we strongly recommend
running both machines as close together as possible, ideally within the same
Availability Zone (AZ) and region. For the AWS cloud, consider using a "Cluster" placement group
to achieve the lowest possible latency.

The remainder of this document will discuss how to set up a benchmark in the AWS cloud
to observe millions of QPS from a single instance.

## Load testing `c6gn.12xlarge`
I usually choose a loadtest machine to be stronger than the server instance to eliminate
any possible bottlenecks on the client side. For this setup, I used `c7gn.16xlarge` for running
the loadtest client and `c6gn.12xlarge` for running dragonfly.
I used Dragonfly v1.15.0 (latest at the time of writing) with the following arguments:
`./dragonfly --logtostderr  --dbfilename=`

Please notice that Dragonfly will uses all the available vCPUs by default, in this case 48 vCPUs
If you want to control explicitly number of threads in Dragonfly you can add `--proactor_threads=<N>`
argument.
Both machines run `Ubuntu 23.04` OS with kernel version 6.2.


### Writes-only test
On the loadtest instance (c7gn.16xlarge with 64 vCPUs) I run:
`memtier_benchmark -s $SERVER_IP --distinct-client-seed --hide-histogram --ratio 1:0 -t 60 -c 20 -n 200000`

The run ended with the following summary:

```
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets      4195628.23          ---          ---         0.39283         0.37500         0.68700         2.54300    323231.06

```

### Reads-only test
Without flushing the database, I run the following command:
`memtier_benchmark -s $SERVER_IP --distinct-client-seed --hide-histogram --ratio 0:1 -t 60 -c 20 -n 200000`

notice the ratio changed to "1:0.

```
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Gets      4109802.84   4109802.84         0.00         0.40126         0.38300         0.67900         0.90300    296551.68
```


### Read test with pipelining

There are many other ways to loadtest Dragonfly. Here is one with sending SETs with pipeline of batch size 10:
`memtier_benchmark -s $SERVER_IP --ratio 0:1 -t 60 -c 5  -n 200000  --distinct-client-seed --hide-histogram --pipeline=10`

```
ALL STATS
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Gets      7083583.57   7083583.57         0.00         0.45821         0.44700         0.69500         1.53500    511131.14
```

## Load testing c7gn.12xlarge

Next thing I tried running Dragonfly on the next generation instance with the same number of vCPUs (48).
I used the same commands to test writes, reads and pipelined reads.

### Writes
`memtier_benchmark -s $SERVER_IP --distinct-client-seed --hide-histogram --ratio 1:0 -t 60 -c 20 -n 200000`

```
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Sets      5195097.56          ---          ---         0.26012         0.24700         0.49500         0.63100    400230.15
```

### Reads
`memtier_benchmark -s $SERVER_IP --distinct-client-seed --hide-histogram --ratio 0:1 -t 60 -c 20 -n 200000`
```
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Gets      6078632.89   6078632.89         0.00         0.27177         0.26300         0.49500         0.62300    438616.86
```

### Pipelined Reads
`memtier_benchmark -s $SERVER_IP --ratio 0:1 -t 60 -c 5  -n 200000  --distinct-client-seed --hide-histogram --pipeline=10`

```
============================================================================================================================
Type         Ops/sec     Hits/sec   Misses/sec    Avg. Latency     p50 Latency     p99 Latency   p99.9 Latency       KB/sec
----------------------------------------------------------------------------------------------------------------------------
Gets      8975121.86   8975121.86         0.00         0.32325         0.31100         0.52700         0.83900    647619.14
```