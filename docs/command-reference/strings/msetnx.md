---
description:  Understand how to use Redis MSETNX to set multiple keys only if they don't exist. 
---

import PageTitle from '@site/src/components/PageTitle';

# MSETNX

<PageTitle title="Redis MSETNX Command (Documentation) | Dragonfly" />

## Syntax

    MSETNX key value [key value ...]

**Time complexity:** O(N) where N is the number of keys to set.

**ACL categories:** @write, @string, @slow

Sets the given keys to their respective values.
`MSETNX` will not perform any operation at all even if just a single key already
exists.

Because of this semantic `MSETNX` can be used in order to set different keys
representing different fields of a unique logic object in a way that ensures
that either all the fields or none at all are set.

`MSETNX` is atomic, so all given keys are set at once.
It is not possible for clients to see that some of the keys were updated while
others are unchanged.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers), specifically:

* `1` if the all the keys were set.
* `0` if no key was set (at least one key already existed).

## Examples

```shell
dragonfly> MSETNX key1 "Hello" key2 "there"
(integer) 1
dragonfly> MSETNX key2 "new" key3 "world"
(integer) 0
dragonfly> MGET key1 key2 key3
1) "Hello"
2) "there"
3) (nil)
```
