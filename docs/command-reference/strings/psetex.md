---
description:  Learn how to use Redis PSETEX to set key's value and expiration in milliseconds. 
---

import PageTitle from '@site/src/components/PageTitle';

# PSETEX

<PageTitle title="Redis PSETEX Command (Documentation) | Dragonfly" />

## Syntax

    PSETEX key milliseconds value

**Time complexity:** O(1)

**ACL categories:** @write, @string, @slow

`PSETEX` works exactly like `SETEX` with the sole difference that the expire
time is specified in milliseconds instead of seconds.

## Examples

```shell
dragonfly> PSETEX mykey 1000 "Hello"
OK
dragonfly> PTTL mykey
(integer) 1000
dragonfly> GET mykey
"Hello"
```
