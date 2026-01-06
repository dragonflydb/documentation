---
description: Rate limiting with a leaky bucket-type algorithm.
---

import PageTitle from '@site/src/components/PageTitle';

# CL.THROTTLE

<PageTitle title="Redis CL.THROTTLE Command (Documentation) | Dragonfly" />

## Syntax

```
CL.THROTTLE <key> <max_burst> <count per period> <period> [<quantity>]
```

**Time complexity:** O(1)

**ACL categories:** @throttle

This command provides functionality for implementing a rate limiter and
is based on a Redis module called [redis-cell](https://github.com/brandur/redis-cell).

The command implements the fairly sophisticated [generic cell rate algorithm (GCRA)](https://en.wikipedia.org/wiki/Generic_cell_rate_algorithm),
which is a leaky bucket-type scheduling algorithm providing a rolling time window and doesn't depend on a background drip process.

By using the `CL.THROTTLE` command, **which is natively supported in Dragonfly**,
you can replace (directly or with code modification) existing Redis modules or libraries implementing
a leaky bucket or a token bucket rate limiter, such as the following:

- The [redis-cell](https://github.com/brandur/redis-cell) module for Redis.
- The [redis_rate](https://github.com/go-redis/redis_rate/) library for Go.
- The [bucket4j](https://github.com/bucket4j/bucket4j) library for Java.
- The [limiter](https://github.com/jhurliman/node-rate-limiter) library for JavaScript, TypeScript, and NodeJS.
- The [governor](https://github.com/boinkor-net/governor) library for Rust.

## Parameter Explanations

- `key`: An identifier to rate limit against, such as a user ID or an IP address.
- The rest of the parameters are self-explanary:

```shell
dragonfly$> CL.THROTTLE user123 20 120 60 1
#                          ^     ^   ^  ^ ^
#                          |     |   |  | └───── apply 1 token (default if omitted)
#                          |     |   └──┴─────── 120 tokens / 60 seconds
#                          |     └────────────── 20 max_burst
#                          └──────────────────── key "user123"
```

## Return Values

An [array](https://redis.io/docs/latest/develop/reference/protocol-spec/#arrays) of 5 integers with the following values:

1. Whether to limit the related action (0 for allowed, 1 for limited).
2. The total limit of the key. (Equivalent to `X-RateLimit-Limit`)
3. The remaining limit of the key. (Equivalent to `X-RateLimit-Remaining`)
4. Number of seconds to wait until a retry if the related action should be limited, else -1. (Equivalent to `Retry-After`)
5. Number of seconds until the limit is fully restored. (Equivalent to `X-RateLimit-Reset`)

## Examples

```shell
dragonfly$> CL.THROTTLE user123 0 1 10 1
1) (integer) 0
2) (integer) 1
3) (integer) 0
4) (integer) -1
5) (integer) 11

dragonfly$> CL.THROTTLE user123 0 1 10 1
1) (integer) 1
2) (integer) 1
3) (integer) 0
4) (integer) 10
5) (integer) 10
```
