---
description: "Learn the Redis TTL command to get remaining time-to-live of a key."
---

import PageTitle from '@site/src/components/PageTitle';

# FIELDTTL

<PageTitle title="Redis TTL Command (Documentation) | Dragonfly" />

## Syntax

    FIELDTTL key field

**Time complexity:** O(1)

**ACL categories:** @keyspace, @read, @fast

Returns the remaining time to live of a field that has a timeout (either hash or set).
This introspection capability allows a Dragonfly client to check how many seconds a given field will continue to be part of the dataset.
A ```WRONGTYPE``` error is returned if the key is not a hash or set.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers): TTL in seconds, or a negative value in order to signal an error.

- The command returns `-1` if the field exists but has no associated TTL.
- The command returns `-2` if the key does not exist.
- The command returns `-3` if the field does not exist.

## Examples

```shell
dragonfly> HSETEX myhash 10 field1 "Hello"
(integer) 1
# wait for 6 seconds
dragonfly> FIELDTTL myhash field1
(integer) 4
```
