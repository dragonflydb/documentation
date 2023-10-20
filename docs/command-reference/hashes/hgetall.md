---
description: "Learn how to use Redis HGETALL command to fetch all fields and values of a hash. Streamline your data retrieval with ease."
---

import PageTitle from '@site/src/components/PageTitle';

# HGETALL

<PageTitle title="Redis HGETALL Command (Documentation) | Dragonfly" />

## Syntax

    HGETALL key

**Time complexity:** O(N) where N is the size of the hash.

**ACL categories:** @read, @hash, @slow

Returns all fields and values of the hash stored at `key`.
In the returned value, every field name is followed by its value, so the length
of the reply is twice the size of the hash.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec/#arrays): list of fields and their values stored in the hash, or an
empty list when `key` does not exist.

## Examples

```shell
dragonfly> HSET myhash field1 "Hello"
(integer) 1
dragonfly> HSET myhash field2 "World"
(integer) 1
dragonfly> HGETALL myhash
1) "field1"
2) "Hello"
3) "field2"
4) "World"
```
