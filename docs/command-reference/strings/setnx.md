---
description:  Learn how to use Redis SETNX for setting a key's value, only if the key does not exist.
---

import PageTitle from '@site/src/components/PageTitle';

# SETNX

<PageTitle title="Redis SETNX Command (Documentation) | Dragonfly" />

## Syntax

    SETNX key value

**Time complexity:** O(1)

**ACL categories:** @write, @string, @fast

Set `key` to hold string `value` if `key` does not exist.
When `key` already holds a value, no operation is performed.
`SETNX` is short for "**SET** if **N**ot e**X**ists".

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers), specifically:

* `1` if the key was set
* `0` if the key was not set

## Examples

```shell
dragonfly> SETNX mykey "Hello"
(integer) 1
dragonfly> SETNX mykey "World"
(integer) 0
dragonfly> GET mykey
"Hello"
```

