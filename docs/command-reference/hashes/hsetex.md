---
description: "Learn how to use Redis HSETEX command to set the value of a hash field and its expiry time. A smart way to manage temporary data."
---

import PageTitle from '@site/src/components/PageTitle';

# HSETEX

<PageTitle title="Redis HSETEX Command (Documentation) | Dragonfly" />

## Syntax

    HSETEX key [NX] [KEEPTTL] seconds field value [field value ...]

**Time complexity:** O(1) for each field/value pair added, so O(N) to add N field/value pairs when the command is called with multiple field/value pairs.

**ACL categories:** @read, @hash, @fast

**Warning:** Experimental! Dragonfly-specific.

Similar to [`HSET`](./hset.md) but adds one or more hash fields that expire after specified number of seconds.
By default, this command overwrites the values and expirations of specified fields that exist in the hash.
If `NX` option is specified, the field data will not be overwritten.
If `KEEPTTL` option is specified, the TTL for the field will not be overwritten.
If `key` doesn't exist, a new key holding a hash is created.

The expiration time can be accessed with the [`FIELDTTL`](../generic/fieldttl.md) command.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers): The number of fields that were added.

## Examples

```shell
dragonfly> HSETEX myhash 5 field1 "Hello"
(integer) 1
# wait for 4 seconds
dragonfly> HGETALL myhash
1) "field1"
2) "Hello"
# wait for 1 seconds
dragonfly> HGETALL myhash
(empty array)
dragonfly> HSETEX myhash 5 field1 "Hello"
(integer) 1
dragonfly> HSETEX myhash NX 100 field1 "Hello"
(integer) 0
# wait for 5 seconds
dragonfly> HGETALL myhash
(empty array)
```
