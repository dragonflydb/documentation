---
description: Learn to use the Redis BZMPOP command to remove and return the smallest score member from sorted sets.
---

import PageTitle from '@site/src/components/PageTitle';

# BZMPOP

<PageTitle title="Redis BZMPOP Explained" />

## Syntax

```shell
BZMPOP timeout numkeys key [key ...] <MIN | MAX> [COUNT count]
```

- **Time complexity:** O(K) + O(M*log(N)) where K is the number of provided keys, N being the number of elements in the sorted set, and M being the number of elements popped.
- **ACL categories:** @write, @sortedset, @slow, @blocking

## Introduction

`BZMPOP` is the blocking variant of [`ZMPOP`](./zmpop.md).

When any of the sorted sets contains elements, this command behaves exactly like `ZMPOP`. When used inside a `MULTI/EXEC` block, this command behaves exactly like `ZMPOP`. When all sorted sets are empty, Redis will block the connection until another client adds members to one of the keys or until the timeout (a double value specifying the maximum number of seconds to block) elapses. A timeout of zero can be used to block indefinitely.

## Return Values

[Array reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#arrays): specifically:

* `nil` when no element could be popped.
* A two-element array with the first element being the name of the key from which elements were popped, and the second element is an array of the popped elements. Every entry in the elements array is also an array that contains
the member and its score.