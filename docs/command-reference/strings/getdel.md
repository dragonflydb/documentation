---
description:  Learn how to use Redis GETDEL to retrieve and delete a key’s value.
---

import PageTitle from '@site/src/components/PageTitle';

# GETDEL

<PageTitle title="Redis GETDEL Command (Documentation) | Dragonfly" />

## Syntax

    GETDEL key

**Time complexity:** O(1)

**ACL categories:** @write, @string, @fast

Get the value of `key` and delete the key.
This command is similar to `GET`, except for the fact that it also deletes the key on success (if and only if the key's value type is a string).

## Return

[Bulk string reply](https://redis.io/docs/reference/protocol-spec/#bulk-strings): the value of `key`, `nil` when `key` does not exist, or an error if the key's value type isn't a string.

## Examples

```shell
dragonfly> SET mykey "Hello"
OK
dragonfly> GETDEL mykey
"Hello"
dragonfly> GET mykey
(nil)
```
