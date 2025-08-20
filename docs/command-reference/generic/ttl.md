---
description: "Learn the Redis TTL command to get remaining time-to-live of a key."
---

import PageTitle from '@site/src/components/PageTitle';

# TTL

<PageTitle title="Redis TTL Command (Documentation) | Dragonfly" />

## Syntax

    TTL key

**Time complexity:** O(1)

**ACL categories:** @keyspace, @read, @fast

Returns the remaining time to live of a key that has a timeout.
This introspection capability allows a Dragonfly client to check how many seconds a
given key will continue to be part of the dataset.

## Return

[Integer reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#integers): TTL in seconds, or a negative value in order to signal an error.

- The command returns `-2` if the key does not exist.
- The command returns `-1` if the key exists but has no associated expire.

## Examples

```shell
dragonfly> SET mykey "Hello"
OK
dragonfly> EXPIRE mykey 10
(integer) 1
dragonfly> TTL mykey
(integer) 10
```
