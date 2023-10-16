# ACL CAT

## Syntax

    ACL CAT [category]

**ACL categories:** @slow

The command shows the available ACL categories if called without arguments.
If a category name is given, the command shows all the Dragonfly commands in the specified category.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec/#arrays)

## Examples

```shell
dragonfly> ACL CAT
 1) KEYSPACE
 2) READ
 3) WRITE
 4) SET
 5) SORTED_SET
 6) LIST
 7) HASH
 8) STRING
 9) BITMAP
10) HYPERLOG
11) GEO
12) STREAM
13) PUBSUB
14) ADMIN
15) FAST
16) SLOW
17) BLOCKING
18) DANGEROUS
19) CONNECTION
20) TRANSACTION
21) SCRIPTING
22) FT_SEARCH
23) THROTTLE
24) JSON
```

With [category]:

```shell
dragonfly> ACL CAT STRING
 1) PREPEND
 2) SETRANGE
 3) DECRBY
 4) MSETNX
 5) MGET
 6) MSET
 7) GETRANGE
 8) PSETEX
 9) SUBSTR
10) INCRBYFLOAT
11) SET
12) GETDEL
13) INCR
14) SETNX
15) GET
16) APPEND
17) STRLEN
18) GETEX
19) GETSET
20) SETEX
21) DECR
22) INCRBY
```
