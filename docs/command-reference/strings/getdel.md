---
description: Get the value of a key and delete the key
---

# GETDEL

## Syntax

    GETDEL key

**Time complexity:** O(1)

Get the value of `key` and delete the key.
This command is similar to `GET`, except for the fact that it also deletes the key on success (if and only if the key's value type is a string).

## Return

[Bulk string reply](https://redis.io/docs/reference/protocol-spec#resp-bulk-strings): the value of `key`, `nil` when `key` does not exist, or an error if the key's value type isn't a string.

## Examples

```shell
dragonfly> SET mykey "Hello"
"OK"
dragonfly> GETDEL mykey
"Hello"
dragonfly> GET mykey
(nil)
```
