---
description:  Learn how to use the Redis BZMPOP command to remove and fetch the last element from list.
---
import PageTitle from '@site/src/components/PageTitle';

# BRPOP

<PageTitle title="Redis BZMPOP Command (Documentation) | Dragonfly" />

## Syntax

    BZMPOP timeout numkeys key [key ...] <MIN | MAX> [COUNT count]

**Time complexity:** O(K) + O(Mlog(N)) where K is the number of provided keys, N being the number of elements in the sorted set, and M being the number of elements popped.

**ACL categories:** @write, @sortedset, @slow, @blocking

BLMPOP is the blocking version of LMPOP. When any of the lists contain elements, it operates exactly like LMPOP. Inside a MULTI/EXEC block, it also behaves the same as LMPOP. 
If all lists are empty, Dragonfly will block the connection until another client pushes an element or until the specified timeout (a double value representing the maximum number 
of seconds to block) expires. A timeout of zero causes it to block indefinitely.

## Return

[Array reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#arrays): specifically:

* A `nil` Nil reply: when no element could be popped and the timeout is reached.
* A a two-element array with the first element being the name of the key from which elements were popped, and the second element being an array of the popped elements.
