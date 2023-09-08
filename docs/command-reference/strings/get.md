---
description: Get the value of a key
---

# GET

## Syntax

    GET key

**Time complexity:** O(1)

**ACL categories:** @write, @string, @fast

Get the value of `key`.
If the key does not exist the special value `nil` is returned.
An error is returned if the value stored at `key` is not a string, because `GET`
only handles string values.

## Return

[Bulk string reply](https://redis.io/docs/reference/protocol-spec/#bulk-strings): the value of `key`, or `nil` when `key` does not exist.

## Examples

```shell
dragonfly> GET nonexisting
(nil)
dragonfly> SET mykey "Hello"
"OK"
dragonfly> GET mykey
"Hello"
```
