---
description: Create a key using the provided serialized value, previously
  obtained using DUMP.
---

# RESTORE

## Syntax

    RESTORE key ttl serialized-value [REPLACE] [ABSTTL]

**Time complexity:** O(1) to create the new key and additional O(N*M) to reconstruct the serialized value, where N is the number of Dragonfly objects composing the value and M their average size. For small string values the time complexity is thus O(1)+O(1*M) where M is small, so simply O(1). However for sorted set values the complexity is O(N*M*log(N)) because inserting values into sorted sets is O(log(N)).

**ACL categories:** @keyspace, @write, @slow, @dangerous

Create a key associated with a value that is obtained by deserializing the
provided serialized value (obtained via `DUMP`).

If `ttl` is 0 the key is created without any expire, otherwise the specified
expire time (in milliseconds) is set.

If the `ABSTTL` modifier was used, `ttl` should represent an absolute
[Unix timestamp][hewowu] (in milliseconds) in which the key will expire.

[hewowu]: http://en.wikipedia.org/wiki/Unix_time

`!RESTORE` will return a "Target key name is busy" error when `key` already
exists unless you use the `REPLACE` modifier.

`!RESTORE` checks the data checksum. If it does not match an error is returned.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec#resp-simple-strings): The command returns OK on success.

## Examples

```
dragonfly> DEL mykey
0
dragonfly> RESTORE mykey 0 "\x0e\x01\x11\x11\x00\x00\x00\x0e\x00\x00\x00\x03\x00\x00\xf2\x02\xf3\x02\xf4\xff\t\x00\xfa\x81\x98P\x85\xf8\xd9\xed"
OK
dragonfly> TYPE mykey
list
dragonfly> LRANGE mykey 0 -1
1) "1"
2) "2"
3) "3"
```
