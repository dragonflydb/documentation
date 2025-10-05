---
description:  Learn how to use the Redis BLMPOP command to remove and fetch the last element from list.
---
import PageTitle from '@site/src/components/PageTitle';

# BLMPOP

<PageTitle title="Redis BLMPOP Command (Documentation) | Dragonfly" />

## Syntax

```shell
BLMPOP timeout numkeys key [key ...] <LEFT | RIGHT> [COUNT count]
```

**Time complexity:** O(N+M) where N is the number of provided keys and M is the number of elements returned.

**ACL categories:** @write, @list, @slow, @blocking

`BLMPOP` is the blocking variant of [`LMPOP`](./lmpop).

When any of the lists has elements, this command functions exactly like `LMPOP`.
The same applies when it is used within a `MULTI/EXEC` block.
If all lists are empty, Dragonfly will block the connection until another client pushes elements to one of the keys
or the specified `timeout` (a double value representing the maximum blocking time in seconds) expires.
A `timeout` of zero can be used to block indefinitely.

## Return

- [Null reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#nulls): when no element could be popped and the `timeout` is reached.
- [Array reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#arrays): a two-element array with the first element
  being the name of the key from which elements were popped, and the second element being an array of the popped elements.
