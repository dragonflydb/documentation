---
description: "Learn to use the Dragonfly SHRINK command to compact the hash table of a set or hash after many members are removed."
---

import PageTitle from '@site/src/components/PageTitle';

# SHRINK

<PageTitle title="Dragonfly SHRINK Command (Documentation) | Dragonfly" />

## Syntax

    SHRINK key

**Time complexity:** O(N) where N is the number of buckets in the hash table before the shrink.

**ACL categories:** @fast, @write

Compacts the hash table that stores the set or hash at `key`: Dragonfly rebuilds the table with as many buckets as there are members, rounded up to a power of two and at least 8.
For a hash, and for a set when `--use_oah_set=false`, `SHRINK` also removes the fields or members whose TTL has passed while it rebuilds the table, and deletes the key if none remain.
This command is Dragonfly-specific.

`SHRINK` applies only to sets and hashes stored as a hash table, which the error message calls the DenseSet encoding.
Small hashes stored as a listpack (see [`--listpack_max_bytes`](../../managing-dragonfly/flags.md#--listpack_max_bytes)
and [`--listpack_max_field_len`](../../managing-dragonfly/flags.md#--listpack_max_field_len)), small integer-only sets stored as an intset,
and keys of all other types return an error.

In Dragonfly v2.1.0, the reply is not the amount of memory that `SHRINK` frees:

- Sets use the OAH format by default ([`--use_oah_set`](../../managing-dragonfly/flags.md#--use_oah_set)),
  which shrinks the table automatically when members are removed, so `SHRINK` on a set usually returns `0`.
  It still compacts a set whose members expired and were dropped by a read, because reads do not shrink the table. That compaction frees memory.
- For hashes, and for sets when `--use_oah_set=false`, the reply reports how much the bucket array shrank, but the array keeps its allocated memory.
  `MEMORY USAGE` of the key does not decrease after `SHRINK`, even when the reply is not `0`, unless `SHRINK` removed expired fields or members.

## Return

One of the following:

- [Integer reply](https://valkey.io/topics/protocol/#integers): the number of bytes by which the bucket array shrank, or `0` if the table was already compact.
- [Nil reply](https://valkey.io/topics/protocol/#nulls): the key does not exist.
- [Error reply](https://valkey.io/topics/protocol/#simple-errors): `ERR WRONGTYPE Key is not a set or hash with DenseSet encoding` if the key holds another type, or a set or hash in a compact encoding.
  The error starts with `ERR`, not `WRONGTYPE`, so clients that look for `WRONGTYPE` errors do not recognize it.

## Examples

Create a hash with 1,000 fields, remove all but 10 of them, and shrink it.
The number in the reply depends on the size of the table.
The second call returns `0` because the table is already compact.

```shell
dragonfly> EVAL "for i = 1, 1000 do redis.call('HSET', KEYS[1], 'field' .. i, 'v') end" 1 myhash
(nil)
dragonfly> EVAL "for i = 11, 1000 do redis.call('HDEL', KEYS[1], 'field' .. i) end" 1 myhash
(nil)
dragonfly> HLEN myhash
(integer) 10
dragonfly> SHRINK myhash
(integer) 8064
dragonfly> SHRINK myhash
(integer) 0
```

The same steps on a set return `0`, because removing the members already shrank its table:

```shell
dragonfly> EVAL "for i = 1, 1000 do redis.call('SADD', KEYS[1], 'member' .. i) end" 1 myset
(nil)
dragonfly> EVAL "for i = 11, 1000 do redis.call('SREM', KEYS[1], 'member' .. i) end" 1 myset
(nil)
dragonfly> SCARD myset
(integer) 10
dragonfly> SHRINK myset
(integer) 0
```

A small hash and a missing key:

```shell
dragonfly> HSET small field1 a field2 b
(integer) 2
dragonfly> SHRINK small
(error) ERR WRONGTYPE Key is not a set or hash with DenseSet encoding
dragonfly> SHRINK nosuchkey
(nil)
```
