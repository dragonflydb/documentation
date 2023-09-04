---
description: Get a substring of the string stored at a key
---

# SUBSTR

## Syntax

    SUBSTR key start end

**Time complexity:** O(N) where N is the length of the returned string. The complexity is ultimately determined by the returned length, but because creating a substring from an existing string is very cheap, it can be considered O(1) for small strings.

**ACL categories:** @read, @string, @slow

Returns the substring of the string value stored at `key`, determined by the
offsets `start` and `end` (both are inclusive).
Negative offsets can be used in order to provide an offset starting from the end
of the string.
So -1 means the last character, -2 the penultimate and so forth.

The function handles out of range requests by limiting the resulting range to
the actual length of the string.

## Return

[Bulk string reply](https://redis.io/docs/reference/protocol-spec#resp-bulk-strings): the substring indicated by `start`, `end` of the string stored at key `key`.

## Examples

```shell
dragonfly> SET mykey "This is a string"
"OK"
dragonfly> GETRANGE mykey 0 3
"This"
dragonfly> GETRANGE mykey -3 -1
"ing"
dragonfly> GETRANGE mykey 0 -1
"This is a string"
dragonfly> GETRANGE mykey 10 100
"string"
```
