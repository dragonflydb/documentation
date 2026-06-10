---
description: "Get insights on using Redis RESTORE command to create key using serialized value."
---

import PageTitle from '@site/src/components/PageTitle';

# RESTORE

<PageTitle title="Redis RESTORE Command (Documentation) | Dragonfly" />

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
Additionally, listpack and intset payloads are deeply validated on restore.

## Return

[Simple string reply](https://valkey.io/topics/protocol/#simple-strings): The command returns OK on success.

## Examples

Serialize a key with `DUMP`, then recreate it from that payload with `RESTORE`:

```
dragonfly> SET greeting Hello
OK
dragonfly> DUMP greeting
"\x00\x05Hello\t\x00l;\xa6$i\x83\x9c2"
dragonfly> DEL greeting
(integer) 1
dragonfly> RESTORE greeting 0 "\x00\x05Hello\t\x00l;\xa6$i\x83\x9c2"
OK
dragonfly> GET greeting
"Hello"
```

The serialized value is a binary blob produced by `DUMP` and is tied to the
server's RDB version — a payload dumped from a different version may be rejected
by the version/checksum check described above.
