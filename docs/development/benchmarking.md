---
sidebar_position: 3
---

# Benchmarking

Do you have an existing Redis environment and would like to see if Dragonfly could be a better
replacement? <br/>
Are you developing a service and would like to determine which cloud instance type to
allocate for Dragonfly? <br/>
Do you wonder how many replicas you need to support your workload?

If so, read on, because this page is for you!

## Squeezing the Best Performance

A benchmark is done to assess the performance aspects of a system. In the case of Dragonfly, a
benchmark is commonly used to assess the CPU and memory performance & utilization.

Depending on the goals of your benchmark, you should choose the machine size accordingly. For a
production mimicking benchmark, you should use a machine size and traffic load similar to that of
your busiest production timing, or even higher to allow for some cushion.

### `io_uring`

Dragonfly supports both `epoll` and [`io_uring`](https://en.wikipedia.org/wiki/Io_uring) Linux APIs.
`io_uring` is a newer API, which is faster. Dragonfly runs best with `io_uring`, but it is only
available with Linux kernels >= 5.1.

`io_uring` is available in Debian versions Bullseye (11) or later, Ubuntu 21.04 or later, Red Hat
Enterprise Linux 9.3 or later, Fedora 37 or later.

To find if your machine has `io_uring` support you could run the following:

```shell
grep io_uring_setup /proc/kallsyms
```

### Choosing Instance Type

Cloud providers, such as Amazon AWS, provide different types and sizes of virtual machines. When in
doubt, you could always opt in for a bigger instance (for both Dragonfly and the client to send the
benchmarking traffic) so that you'll know what the upper limit is.

### Choosing Thread Count

By default, Dragonfly will create a thread for each available CPU on the machine. You can modify
this behavior with the `--proactor_threads` flag. Generally you should not use this flag for a
machine dedicated to running Dragonfly. You can specify a lower number if you only want Dragonfly to
utilize some of the machine, but don't specify a higher number (i.e. more than CPUs) as it would
degrade performance.

## Setting Up Dragonfly

Dragonfly can run in [Docker](/getting-started/docker) or directly installed as a
[binary](/getting-started/binary) on your machine. See the [Getting Started](/getting-started) page
for other options and the latest documentation.

## Reducing Noise

Ideally, a benchmark should be run in as similar as possible environment as the production setup.

In busy production deployments, it is common to run Dragonfly in its own machine (virtual or
dedicated). If you plan to do so in your production setup as well (which we highly recommend),
consider running the benchmark in a similar way.

In practice, it means that any other systems in your setup (like other services & databases) should
run in other machines. Importantly, also **the software that sends the traffic should run in another
machine.**

## Sending Traffic

If your service already has existing benchmarking tools, or ways to record and replay production
traffic, you should definitely use them. That would be the closest estimation to what a real
production deployment with a backing Dragonfly would look like.

If, like many others, you do not (yet) have such a tool, you could either write your own tool to
simulate production traffic or use an existing tool like `memtier_benchmark`.

When writing your own tool, try to recreate the production traffic as closely as possible. Use the
same commands (like `SET`, `GET`, `SADD`, etc), with the expected ratio between them, and the
expected key and value sizes.

If you choose to use an existing benchmarking tool, a popular and mature one is
[`memtier_benchmark`](https://github.com/RedisLabs/memtier_benchmark). It's an Open Source tool for
generic load generation and benchmarking with many features. We use it for benchmarking constantly.
Check out their [documentation
page](https://redis.com/blog/memtier_benchmark-a-high-throughput-benchmarking-tool-for-redis-memcached/)
for more details, but as a quick reference you could use:

```shell
memtier_benchmark \
    --server=<IP / Host> \
    --threads=<thread count> \
    --clients=<clients per thread> \
    --requests=<requests per client>
```

## Having Troubles? Anything Unclear?

Improving our documentation and helping the community is always of the higher priority for us, so
please feel free to reach out!
