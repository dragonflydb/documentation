---
description: Set multiple hash fields to multiple values
---

# HMSET

## Syntax

    HMSET key field value [field value ...]

**Time complexity:** O(N) where N is the number of fields being set.

Sets the specified fields to their respective values in the hash stored at
`key`.
This command overwrites any specified fields already existing in the hash.
If `key` does not exist, a new key holding a hash is created.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec#resp-simple-strings)

## Examples

```shell
dragonfly> HMSET myhash field1 "Hello" field2 "World"
"OK"
dragonfly> HGET myhash field1
"Hello"
dragonfly> HGET myhash field2
"World"
```
