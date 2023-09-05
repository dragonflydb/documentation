---
description: Read entries from one or multiple streams
---

# XREAD

## Syntax

    XREAD [COUNT count] [BLOCK Milliseconds] STREAMS key [key ...] id [id ...]


**ACL categories:** @read, @stream, @slow, @blocking

Read entries from one or multiple streams. In case of multiple
streams, the order of stream entries is maintained. Note that
XREAD returns entries with IDs **greater** than the specified
ones. This is useful in cases where user need to know the new
unread entries from specified streams.

The number of keys and ids should be balanced. User in no way
can provide keys with fewer ids or vice-versa. The i'th id
corresponds to the i'th key. Below is an example -

```shell
dragonfly> XREAD STREAMS mystream other-stream 1687926136634-0 1687921762755-0
1) 1) "mystream"
   2) 1) 1) "1687926140032-0"
         2) 1) "k"
            2) "v"
2) 1) "other-stream"
   2) 1) 1) "1687924609465-0"
         2) 1) "k2"
            2) "v2"
```


### COUNT

User can limit the number of received entries by specifying the
**COUNT** limit. It takes an integer value and returns atmost
that number of entries.

```shell
dragonfly> XREAD COUNT 2 STREAMS mystream 0
1) 1) "mystream"
   2) 1) 1) "1686831019899-0"
         2) 1) "a"
            2) "1"
      2) 1) "1686831037806-0"
         2) 1) "b"
            2) "2"
```

### BLOCK

Sometimes, the specified stream doesn't have any new entries to
consume. New entries may be added in some interval or time range.
In that case, **BLOCK** option comes in handy. **BLOCK** takes
a value denoting the *milliseconds* the command will block for.

Once **BLOCK** is used in the command, the command waits for the
specified time interval. The command returns immediately if one of
the requested stream receive new entries within the specified time
range. Else it simply returns a Null reply.

If new entries are already present in the stream before executing
command, it immediately returns those entries even if **BLOCK**
option is specified.

Note that, all clients who are waiting for the same range of IDs
get same new entries.

### STREAMS

**STREAMS** is a required option and it must be the last specified
option. It takes lists of keys and ids. The format is as follows -

```shell
STREAMS key1 key2 key3 ... id1 id2 id3 ...
```

The number of keys and ids should be exactly same. Else a *syntax
error* will be triggered. For a given list of keys and ids, the
command searches for entries greater than i'th id of the i'th stream
(like in the above example, XREAD searches for entries greater than
*id1* for the stream *key1* and so on). Keys should be valid streams.

User can specify IDs in three ways - 
 * **Incomplete IDs:** Client only specifies the timestamp. Here the sequence
   part is interpreted as 0.
```shell
dragonfly> XREAD STREAMS key1 key2 1 0
```
   The above command is equivalent to the below command:
```shell
dragonfly> XREAD STREAMS key1 key2 1-0 0-0
```
 * **Complete IDs:** Client specifies the full ID.
 * **Special "$" ID:** In some cases, client wants only the recent entries
 which are not previously read. Using hard-coded IDs is not an option
 here. The special ID **$** is what we need to use to accomplish that.
 When specified, the command returns the recent unread entries. It is
 equivalent to specifying the last read stream entry ID.
```shell
dragonfly> XREAD STREAMS key $
```

## Return

[Array Reply](https://redis.io/docs/reference/protocol-spec#resp-arrays).
In some cases, the command returns a null reply. For example, when **BLOCK**
is used.

## Example

```shell
dragonfly> XADD mystream * k v
"1687927570399-0"
dragonfly> XADD mystream * k2 v2
"1687927576419-0"
dragonfly> XADD mystream * k3 v3
"1687927580654-0"
dragonfly> xread streams mystream 1687927570398
1) 1) "mystream"
   2) 1) 1) "1687927570399-0"
         2) 1) "k"
            2) "v"
      2) 1) "1687927576419-0"
         2) 1) "k2"
            2) "v2"
      3) 1) "1687927580654-0"
         2) 1) "k3"
            2) "v3"
```

