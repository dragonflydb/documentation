---
description:  Learn how to manage rate limiting in Redis with CL.THROTTLE command.
---

import PageTitle from '@site/src/components/PageTitle';

# CL.THROTTLE

<PageTitle title="Redis CL.THROTTLE Command (Documentation) | Dragonfly" />

## Syntax

    CL.THROTTLE <key> <max_burst> <count per period> <period> [<quantity>]

**Time complexity:** O(1)

https://redis.com/blog/redis-cell-rate-limiting-redis-module/ 

**ACL categories:** @throttle

This command provides functionality for implementing a rate limit mechanism and
is based on the Redis module called [redis-cell](https://github.com/brandur/redis-cell).

## Return

An [array](https://redis.io/docs/reference/protocol-spec/#arrays) of 5 integers with the following values:

1. Whether to limit the related action (0 for allowed, 1 for limited).
2. The total limit of the key. (Equivalent to `X-RateLimit-Limit`)
3. The remaining limit of the key. (Equivalent to `X-RateLimit-Remaining`)
4. Number of seconds to wait until a retry if the related action should be limited, else -1. (Equivalent to `Retry-After`)
5. Number of seconds until the limit is fully restored. (Equivalent to `X-RateLimit-Reset`)

## Examples

```shell
dragonfly> CL.THROTTLE USER1 0 1 10 1
1) (integer) 0
2) (integer) 1
3) (integer) 0
4) (integer) -1
5) (integer) 11
dragonfly> CL.THROTTLE USER1 0 1 10 1
1) (integer) 1
2) (integer) 1
3) (integer) 0
4) (integer) 10
5) (integer) 10
```
