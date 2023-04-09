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

The output filename can be configured with the `--dbfilename` flag. Any occurences of the substring `{timestamp}`
will also be replaced with a timestamp of the local time in a lexicographically sorted format. If given, the filename extension must be either `.rdb` or `.dfs` and match the dump format. If no extension is given, it will be appended
automatically.

The default filename is `dump-{timestamp}`.

In addition to the `SAVE` command, you can generate snapshots periodically using the `--save_schedule` flag.

[tp]: https://redis.io/topics/persistence

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec#resp-simple-strings): The commands returns OK on success.
