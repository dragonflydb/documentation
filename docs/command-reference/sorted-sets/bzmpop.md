---
description: Learn to use the Redis BZMPOP command to remove and return the smallest score member from sorted sets.
---

import PageTitle from '@site/src/components/PageTitle';

# BZMPOP

<PageTitle title="Redis BZMPOP Explained" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `BZMPOP` command pops one or more members (element-score pairs) from the first non-empty sorted set
in the provided list of key names. It will block the connection for a specified period until a member is available to pop.

## Syntax

```shell
BZMPOP timeout numkeys key [key ...] <MIN | MAX> [COUNT count]
```

- **Time complexity:** O(K) + O(M*log(N)) where K is the number of provided keys, N being the number of elements in the sorted set, and M being the number of elements popped.
- **ACL categories:** @write, @sortedset, @slow, @blocking

`BZMPOP` is the blocking variant of the [`ZMPOP`](./zmpop) command.

When any of the sorted sets contains elements, this command behaves exactly like `ZMPOP`. When used inside a `MULTI/EXEC` block, this command behaves exactly like `ZMPOP`. When all sorted sets are empty, Redis will block the connection until another client adds members to one of the keys or until the `timeout` (a double value specifying the maximum number of seconds to block) elapses. A `timeout` of zero can be used to block indefinitely.

## Return Values

- [Null reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#nulls): when no element could be popped.
- [Array reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#arrays): a two-element array with the first element
  being the name of the key from which elements were popped, and the second element is an array of the popped elements.
  Every entry in the elements array is also an array that contains the member and its score.
