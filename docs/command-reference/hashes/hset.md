---
description: Set the string value of a hash field
---

# HSET

## Syntax

    HSET key field value [field value ...]

**Time complexity:** O(1) for each field/value pair added, so O(N) to add N field/value pairs when the command is called with multiple field/value pairs.

**ACL categories:** @write, @hash, @fast

Sets the specified fields to their respective values in the hash stored at `key`.

This command overwrites the values of specified fields that exist in the hash.
If `key` doesn't exist, a new key holding a hash is created.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers): The number of fields that were added.

## Examples

```shell
dragonfly> HSET myhash field1 "Hello"
(integer) 1
dragonfly> HGET myhash field1
"Hello"
dragonfly> HSET myhash field2 "Hi" field3 "World"
(integer) 2
dragonfly> HGET myhash field2
"Hi"
dragonfly> HGET myhash field3
"World"
dragonfly> HGETALL myhash
1) "field1"
2) "Hello"
3) "field2"
4) "Hi"
5) "field3"
6) "World"
```
