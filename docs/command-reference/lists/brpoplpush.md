---
description: Pop an element from a list, push it to another list and return it;
  or block until one is available
---

# BRPOPLPUSH

## Syntax

    BRPOPLPUSH source destination timeout

**Time complexity:** O(1)

`BRPOPLPUSH` is the blocking variant of `RPOPLPUSH`.
When `source` contains elements, this command behaves exactly like `RPOPLPUSH`.
When used inside a `MULTI`/`EXEC` block, this command behaves exactly like `RPOPLPUSH`.
When `source` is empty, Redis will block the connection until another client
pushes to it or until `timeout` is reached.
A `timeout` of zero can be used to block indefinitely.

See `RPOPLPUSH` for more information.

## Return

[Bulk string reply](https://redis.io/docs/reference/protocol-spec#resp-bulk-strings): the element being popped from `source` and pushed to `destination`.
If `timeout` is reached, a [Null reply](https://redis.io/docs/reference/protocol-spec#resp-bulk-strings) is returned.

## Pattern: Reliable queue

Please see the pattern description in the `RPOPLPUSH` documentation.

## Pattern: Circular list

Please see the pattern description in the `RPOPLPUSH` documentation.
