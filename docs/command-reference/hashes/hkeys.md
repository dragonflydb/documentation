---
description: "Learn how to use Redis HKEYS command to fetch all the keys in a hash. Make large dataset navigation simpler and faster."
---

import PageTitle from '@site/src/components/PageTitle';

# HKEYS

<PageTitle title="Redis HKEYS Command (Documentation) | Dragonfly" />

## Syntax

    HKEYS key

**Time complexity:** O(N) where N is the size of the hash.

**ACL categories:** @read, @hash, @slow

Returns all field names in the hash stored at `key`.

## Return

[Array reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#arrays): list of fields in the hash, or an empty list when `key` does
not exist.

## Examples

```shell
dragonfly> HSET myhash field1 "Hello"
(integer) 1
dragonfly> HSET myhash field2 "World"
(integer) 1
dragonfly> HKEYS myhash
1) "field1"
2) "field2"
```
