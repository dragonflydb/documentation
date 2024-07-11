---
description: "Learn how to use Redis HSETEX command to set the value of a hash field and its expiry time. A smart way to manage temporary data."
---

import PageTitle from '@site/src/components/PageTitle';

# HSETEX

<PageTitle title="Redis HSETEX Command (Documentation) | Dragonfly" />

## Syntax

    HSETEX key seconds field value [field value ...]

**Time complexity:** O(1) for each field/value pair added, so O(N) to add N field/value pairs when the command is called with multiple field/value pairs.

**ACL categories:** @read, @hash, @fast

**Warning:** Experimental! Dragonfly-specific.

Similar to [`HSET`](./hset.md) but adds one or more hash fields that expire after specified number of seconds.
This command overwrites the values of specified fields that exist in the hash.
If `key` doesn't exist, a new key holding a hash is created.
In any case, the expiration of the field is updated according to the latest value and the current clock.

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
```
