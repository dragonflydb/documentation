---
description: Delete a key asynchronously in another thread. Otherwise it is just
  as DEL, but non blocking.
---

# UNLINK

## Syntax

    UNLINK key [key ...]

**Time complexity:** O(1) for each key removed regardless of its size. Then the command does O(N) work in a different thread in order to reclaim memory, where N is the number of allocations the deleted objects where composed of.

This command is very similar to `DEL`: it removes the specified keys.
Just like `DEL` a key is ignored if it does not exist. However the command
performs the actual memory reclaiming in a different thread, so it is not
blocking, while `DEL` is. This is where the command name comes from: the
command just **unlinks** the keys from the keyspace. The actual removal
will happen later asynchronously.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers): The number of keys that were unlinked.

## Examples

```cli
SET key1 "Hello"
SET key2 "World"
UNLINK key1 key2 key3
```
