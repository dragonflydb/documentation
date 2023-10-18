---
description: "Learn how Redis EXISTS command checks if a key exists."
---

import PageTitle from '@site/src/components/PageTitle';

# EXISTS

<PageTitle title="Redis EXISTS Command (Documentation) | Dragonfly" />

## Syntax

    EXISTS key [key ...]

**Time complexity:** O(N) where N is the number of keys to check.

**ACL categories:** @keyspace, @read, @fast

Returns if `key` exists.

The user should be aware that if the same existing key is mentioned in the arguments multiple times, it will be counted multiple times. So if `somekey` exists, `EXISTS somekey somekey` will return 2.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers), specifically the number of keys that exist from those specified as arguments.

## Examples

```shell
dragonfly> SET key1 "Hello"
"OK"
dragonfly> EXISTS key1
(integer) 1
dragonfly> EXISTS nosuchkey
(integer) 0
dragonfly> SET key2 "World"
"OK"
dragonfly> EXISTS key1 key2 nosuchkey
(integer) 2
```
