---
description:  Learn how to use Redis STRLEN to get the length of the string stored in a key.
---

import PageTitle from '@site/src/components/PageTitle';

# STRLEN

<PageTitle title="Redis STRLEN Command (Documentation) | Dragonfly" />

## Syntax

    STRLEN key

**Time complexity:** O(1)

**ACL categories:** @read, @string, @fast

Returns the length of the string value stored at `key`.
An error is returned when `key` holds a non-string value.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers): the length of the string at `key`, or `0` when `key` does not
exist.

## Examples

```shell
dragonfly> SET mykey "Hello world"
OK
dragonfly> STRLEN mykey
(integer) 11
dragonfly> STRLEN nonexisting
(integer) 0
```
