---
description:  Learn to extend a string value in Redis using the APPEND command.
---

import PageTitle from '@site/src/components/PageTitle';

# APPEND

<PageTitle title="Redis APPEND Command (Documentation) | Dragonfly" />

## Syntax

    APPEND key value

**Time complexity:** O(1). The amortized time complexity is O(1) assuming the appended value is small and the already present value is of any size, since the dynamic string library used by Redis will double the free space available on every reallocation.

**ACL categories:** @read, @set, @slow

If `key` already exists and is a string, this command appends the `value` at the
end of the string.
If `key` does not exist it is created and set as an empty string, so `APPEND`
will be similar to `SET` in this special case.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers): the length of the string after the append operation.

## Examples

```shell
dragonfly> EXISTS mykey
(integer) 0
dragonfly> APPEND mykey "Hello"
(integer) 5
dragonfly> APPEND mykey " World"
(integer) 11
dragonfly> GET mykey
"Hello World"
```

## Pattern: Time series

The `APPEND` command can be used to create a very compact representation of a
list of fixed-size samples, usually referred as _time series_.
Every time a new sample arrives we can store it using the command

```
APPEND timeseries "fixed-size sample"
```

Accessing individual elements in the time series is not hard:

* `STRLEN` can be used in order to obtain the number of samples.
* `GETRANGE` allows for random access of elements.
  If our time series have associated time information we can easily implement
  a binary search to get range combining `GETRANGE` with the Lua scripting
  engine available in Redis 2.6.
* `SETRANGE` can be used to overwrite an existing time series.

The limitation of this pattern is that we are forced into an append-only mode
of operation, there is no way to cut the time series to a given size easily
because Redis currently lacks a command able to trim string objects.
However the space efficiency of time series stored in this way is remarkable.

Hint: it is possible to switch to a different key based on the current Unix
time, in this way it is possible to have just a relatively small amount of
samples per key, to avoid dealing with very big keys, and to make this pattern
more friendly to be distributed across many Redis instances.

An example sampling the temperature of a sensor using fixed-size strings (using
a binary format is better in real implementations).

```shell
dragonfly> APPEND ts "0043"
(integer) 4
dragonfly> APPEND ts "0035"
(integer) 8
dragonfly> GETRANGE ts 0 3
"0043"
dragonfly> GETRANGE ts 4 7
"0035"
```
