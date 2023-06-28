---
description: Trim a particular stream
---

# XTRIM

## Syntax

	XTRIM key <MAXLEN | MINID> [= | ~] threshold [LIMIT count]

**Time Complexity:** O(N), with N being the number of evicted entries.
Constant times are very small however, since entries are organized in
macro nodes containing multiple entries that can be released with a
single deallocation.

**XTRIM** works same like how trimming works in **XADD** (when option
specified). But instead of adding a new entry, **XTRIM** focuses
completely on trimming entries. **<key\>** is the stream name of
which the entries need to be trimmed.

With **XTRIM**, you can either specify **MAXLEN** or **MINID** to
control the stratgy to trim.

**MAXLEN** ensures that the number of entries in a stream
doesn't exceed a certain limit. **MINID** on the other hand
ensures that entries with IDs less than the specified **MINID**
get deleted. These two options take a *threshold* denoting the
length (in case of **MAXLEN**) or ID (in case of **MINID**).

Dragonfly gives two options to control the trimming nature.
"**=**" argument tells the command to do the exact trimming of
entries. Whereas **~** argument tells the command to do
the approximate trimming. That is, it is upto the command to
decide how many entries need to be deleted. So a stream may
have **few more** entries than the given *threshold* (due to
performance reasons). It is more efficient than exact trimming.
By default, exact trimming is used when no options are specified.

```shell
dragonfly> XTRIM mystream MAXLEN ~ 100
(integer) 98
```

**LIMIT** is useful when you want to limit the number of delete
operations used for **MAXLEN** or **MINID** (in case of approximate
trimming). When **LIMIT** isn't specified, the default value of
*100 \* the number of entries* in a macro node will be implicitly
used as the count. Specifying the value 0 as count disables the
limiting mechanism entirely.

```shell
dragonfly> XTRIM mystream MAXLEN ~ 100 LIMIT 2
(integer) 2
```

## Return
[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers):
The number of entries deleted from the stream.

## Example

```shell
dragonfly> XADD mystream * name John
"1687921762755-0"
dragonfly> XADD mystream * name Alice
"1687924580856-0"
dragonfly> XADD mystream * name Bob
"1687924609465-0"
dragonfly> XLEN mystream
(integer) 3
dragonfly> XTRIM mystream MAXLEN = 2
(integer) 2
```
