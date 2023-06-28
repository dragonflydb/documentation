---
description: Returns a range of stream entries
---

# XRANGE

## Syntax

	XRANGE key start end [COUNT count]

**Time complexity:** O(N) with N being the number of elements
being returned. If N is constant (e.g. always asking for the
first 10 elements with COUNT), you can consider it O(1).

The **XRANGE** command returns stream entries matching the
given range of IDs. The range is specified by a minimum and
maximum ID. All the entries having an ID between the two
specified or exactly one of the two IDs specified (closed
interval) are returned.

**XRANGE** allows both **<start\>** and **<end\>** IDs to be
the same. In that case, the command only returns the specified
entry.

```shell
dragonfly> xrange mystream 1687926126874-0 1687926126874-0
1) 1) "1687926126874-0"
   2) 1) "k"
      2) "v"
```

## Special IDs

Sometimes, it is logical to get all the entries of a stream. It
is tedious to mention the minimum and maximum IDs explicitly.
To tackle this issue, **XRANGE** accepts two special characters
to denote the minimum ID and maximum ID of a stream. These are
"**-**" and "**+**" respectively. The following command returns
all entries from the stream *mystream*.

```shell
dragonfly> XRANGE mystream - +
1) 1) "1687926126874-0"
   2) 1) "k"
      2) "v"
2) 1) "1687926132506-0"
   2) 1) "l"
      2) "x"
3) 1) "1687926136634-0"
   2) 1) "n"
      2) "t"
4) 1) "1687926140032-0"
   2) 1) "q"
      2) "r"
```

## Incomplete IDs

It is possible to use incomplete IDs in **XRANGE** command. User
can specify just the first part of ID, the millisecond time:

```shell
dragonfly> XRANGE mystream 1687926126874 1687926140032
```

In this case, XRANGE will auto-complete the start interval with
**-0** and end interval with **-18446744073709551615**, in order
to return all the entries that were generated between a given
millisecond and the end of the other specified millisecond. This
also means that repeating the same millisecond two times, will get
all the entries within such millisecond, because the sequence number
range will be from zero to the maximum.

## Exclusive Ranges

By default, the **XRANGE** command returns entries including specified
IDs. If you want the behaviour to be exclusive, prefix the ID with
**(** character.

## COUNT option

**XRANGE** accepts a **COUNT** option to limit the number of entries
returned. It takes integer value.

```shell
dragonfly> XRANGE mystream - + COUNT 1
1) 1) "1687926126874-0"
   2) 1) "k"
      2) "v"
```

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays):

The returned entries are complete, that means that the ID and all the
fields they are composed are returned. Moreover, the entries are
returned with their fields and values in the exact same order as
XADD added them.
