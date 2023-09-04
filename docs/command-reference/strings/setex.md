---
description: Set the value and expiration of a key
---

# SETEX

## Syntax

    SETEX key seconds value

**Time complexity:** O(1)

**ACL categories:** @write, @string, @slow

Set `key` to hold the string `value` and set `key` to timeout after a given
number of seconds.
This command is equivalent to executing the following commands:

```
SET mykey value
EXPIRE mykey seconds
```

`SETEX` is atomic, and can be reproduced by using the previous two commands
inside an `MULTI` / `EXEC` block.
It is provided as a faster alternative to the given sequence of operations,
because this operation is very common when Redis is used as a cache.

An error is returned when `seconds` is invalid.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec#resp-simple-strings)

## Examples

```shell
dragonfly> SETEX mykey 10 "Hello"
"OK"
dragonfly> TTL mykey
(integer) 10
dragonfly> GET mykey
"Hello"
```

