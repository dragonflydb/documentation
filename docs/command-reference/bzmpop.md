---
description: Remove and return members with scores in a sorted set or block
  until one is available
---

# BZMPOP

## Syntax

    BZMPOP timeout numkeys key [key ...] <MIN | MAX> [COUNT count]

**Time complexity:** O(K) + O(M*log(N)) where K is the number of provided keys, N being the number of elements in the sorted set, and M being the number of elements popped.

`BZMPOP` is the blocking variant of `ZMPOP`.

When any of the sorted sets contains elements, this command behaves exactly like `ZMPOP`.
When used inside a `MULTI`/`EXEC` block, this command behaves exactly like `ZMPOP`.
When all sorted sets are empty, Redis will block the connection until another client adds members to one of the keys or until the `timeout` (a double value specifying the maximum number of seconds to block) elapses.
A `timeout` of zero can be used to block indefinitely.

See `ZMPOP` for more information.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays): specifically:

* A `nil` when no element could be popped.
* A two-element array with the first element being the name of the key from which elements were popped, and the second element is an array of the popped elements. Every entry in the elements array is also an array that contains the member and its score.

