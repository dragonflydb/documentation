---
description:  Learn how to conduct bitwise operations on strings using Redis BITOP.
---

import PageTitle from '@site/src/components/PageTitle';

# BITOP

<PageTitle title="Redis BITOP Command (Documentation) | Dragonfly" />

## Syntax

    BITOP <AND | OR | XOR | NOT> destkey key [key ...]

**Time complexity:** O(N)

**ACL categories:** @write, @bitmap, @slow

Perform a bitwise operation between multiple keys (containing string values) and
store the result in the destination key.

The `BITOP` command supports four bitwise operations: **AND**, **OR**, **XOR**
and **NOT**, thus the valid forms to call the command are:


* `BITOP AND destkey srckey1 srckey2 srckey3 ... srckeyN`
* `BITOP OR  destkey srckey1 srckey2 srckey3 ... srckeyN`
* `BITOP XOR destkey srckey1 srckey2 srckey3 ... srckeyN`
* `BITOP NOT destkey srckey`

As you can see **NOT** is special as it only takes an input key, because it
performs inversion of bits so it only makes sense as a unary operator.

The result of the operation is always stored at `destkey`.

## Handling of strings with different lengths

When an operation is performed between strings having different lengths, all the
strings shorter than the longest string in the set are treated as if they were
zero-padded up to the length of the longest string.

The same holds true for non-existent keys, that are considered as a stream of
zero bytes up to the length of the longest string.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers): the size of the string stored in the destination key, which is equal to the
size of the longest input string.

## Examples

```shell
dragonfly> SET key1 "foobar"
OK
dragonfly> SET key2 "abcdef"
OK
dragonfly> BITOP AND dest key1 key2
(integer) 6
dragonfly> GET dest
"`bc`ab"
```

## Pattern: real time metrics using bitmaps

`BITOP` is a good complement to the pattern documented in the `BITCOUNT` command
documentation.
Different bitmaps can be combined in order to obtain a target bitmap where
the population counting operation is performed.

## Performance considerations

`BITOP` is a potentially slow command as it runs in O(N) time.
Care should be taken when running it against long input strings.

For real-time metrics and statistics involving large inputs a good approach is
to use a replica (with replica-read-only option enabled) where the bit-wise
operations are performed to avoid blocking the master instance.
