---
description: Get the value of a key
---

# GET

## Syntax

    GET key

**Time complexity:** O(1)

Get the value of `key`.
If the key does not exist the special value `nil` is returned.
An error is returned if the value stored at `key` is not a string, because `GET`
only handles string values.

## Return

[Bulk string reply](https://redis.io/docs/reference/protocol-spec#resp-bulk-strings): the value of `key`, or `nil` when `key` does not exist.

## Examples

```cli
GET nonexisting
SET mykey "Hello"
GET mykey
```
