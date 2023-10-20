---
description: "Learn how to use Redis HDEL command to remove a field from a hash map. Great for data maintenance operations."
---

import PageTitle from '@site/src/components/PageTitle';

# HDEL

<PageTitle title="Redis HDEL Command (Documentation) | Dragonfly" />

## Syntax

    HDEL key field [field ...]

**Time complexity:** O(N) where N is the number of fields to be removed.

**ACL categories:** @write, @hash, @fast

Removes the specified fields from the hash stored at `key`.
Specified fields that do not exist within this hash are ignored.
If `key` does not exist, it is treated as an empty hash and this command returns
`0`.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers): the number of fields that were removed from the hash, not
including specified but non existing fields.

## Examples

```shell
dragonfly> HSET myhash field1 "foo"
(integer) 1
dragonfly> HDEL myhash field1
(integer) 1
dragonfly> HDEL myhash field2
(integer) 0
```
