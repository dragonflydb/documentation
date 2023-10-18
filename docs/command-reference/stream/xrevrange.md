---
description:  Learn how to use Redis XREVRANGE to fetch a range of messages from a stream in reverse order.
---

import PageTitle from '@site/src/components/PageTitle';

# XREVRANGE

<PageTitle title="Redis XREVRANGE Command (Documentation) | Dragonfly" />

## Syntax

	XREVRANGE key end start [COUNT count]

**Time complexity:** O(N) with N being the number of elements
being returned. If N is constant (e.g. always asking for the
first 10 elements with COUNT), you can consider it O(1).

**ACL categories:** @read, @stream, @slow

**XREVRANGE** is almost same as **XRANGE**. The only difference
is it returns the entries in reverse order, and also takes the
start-end range in reverse order (as you can notice in the
syntax). Reverse order means the range starts with higher IDs
and ends with lower IDs.

So for instance, the following command returns all the
elements from the higher ID to the lower ID:
```shell
XREVRANGE mystream + -
```

**COUNT** option limits the number of entries returned by
the command.
```shell
XREVRANGE mystream + - COUNT 2
```

## Return
[Array reply](https://redis.io/docs/reference/protocol-spec/#arrays)

The return format is exactly same as **XRANGE** command.

## Example

```shell
dragonfly> XREVRANGE mystream + - 
1) 1) "1687927770804-0"
   2) 1) "k3"
      2) "v3"
2) 1) "1687927767585-0"
   2) 1) "k2"
      2) "v2"
3) 1) "1687927765116-0"
   2) 1) "k"
      2) "v"
```
