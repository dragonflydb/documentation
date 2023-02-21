---
description: Synchronously save the dataset to disk
---

# SAVE

## Syntax

    SAVE [RDB|DF]

**Time complexity:** O(N) where N is the total number of keys in all databases

The `SAVE` commands performs a save of the dataset producing a
_point in time_ snapshot of all the data inside the Dragonfly instance, in the form
of a set of [DFS files](../../managing-dragonfly/snapshotting).

Use `SAVE RDB` to save the snapshot in form of an RDB file instead.

Please refer to the [persistence documentation][tp] for detailed information.

[tp]: https://redis.io/topics/persistence

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec#resp-simple-strings): The commands returns OK on success.
