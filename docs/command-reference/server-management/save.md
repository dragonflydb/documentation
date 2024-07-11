---
description:  Learn how to use Redis SAVE command to create a backup of the current database.
---

import PageTitle from '@site/src/components/PageTitle';

# SAVE

<PageTitle title="Redis SAVE Command (Documentation) | Dragonfly" />

## Syntax

    SAVE [RDB|DF]

**Time complexity:** O(N) where N is the total number of keys in all databases

**ACL categories:** @admin, @slow, @dangerous

The `SAVE` commands performs a save of the dataset producing a
_point in time_ snapshot of all the data inside the Dragonfly instance, in the form
of a set of [DFS files](../../managing-dragonfly/snapshotting).

Use `SAVE RDB` to save the snapshot in form of an RDB file instead.
Please refer to the [persistence documentation][tp] for detailed information about RDB files.

## Flags

- **`df_snapshot_format`** - Set true to save dump in Dragonfly file format (true by default).
- **`dbfilename`** - The file name to save and load the database. To generate a file with a timestamp, set the macro `{timestamp}` in the filename, e.g. `dump-{timestamp}`.
  The macro will be replaced with a timestamp of the local time in a lexicographically sorted format.
  The default filename is `dump-{timestamp}`.
- **`snapshot_cron`** - Generate snapshots periodically. The argument is a cron format (e.g. `0 0 * * *`, `*/5 * * * *`)

[tp]: https://redis.io/topics/persistence

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec/#simple-strings): The commands returns OK on success.
