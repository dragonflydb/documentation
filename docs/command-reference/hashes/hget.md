---
description: "Learn how to use Redis HGET command to retrieve the value of a hash field. Perfect for data fetching tasks."
---

import PageTitle from '@site/src/components/PageTitle';

# HGET

<PageTitle title="Redis HGET Command (Documentation) | Dragonfly" />

## Syntax

    HGET key field

**Time complexity:** O(1)

**ACL categories:** @read, @hash, @fast

Returns the value associated with `field` in the hash stored at `key`.

## Return

[Bulk string reply](https://redis.io/docs/reference/protocol-spec/#bulk-strings): the value associated with `field`, or `nil` when `field` is not
present in the hash or `key` does not exist.

## Examples

```shell
dragonfly> HSET myhash field1 "foo"
(integer) 1
dragonfly> HGET myhash field1
"foo"
dragonfly> HGET myhash field2
(nil)
```
