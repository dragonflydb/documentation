---
sidebar_position: 5
---

# Saving Backups

A Dragonfly instance can generate disk backups both automatically and manually.
A number of flags influence the behavior of the backup mechanism. The flags can be given through
the command line or via a [flag file](../getting-started/binary.md#flag-files).

## Automatic Backups

Dragonfly will create a backup upon shutdown whenever the `dbfilename` flag is not empty.
In addition, Dragonfly can be configured to perform scheduled backups with the `snapshot_cron` flag.
Note that:

- In Dragonfly >= 1.7.1, the `snapshot_cron` flag was introduced.
- In Dragonfly < 1.7.1, only the `save_schedule` flag could be used.
- The `save_schedule` flag is deprecated, and it will be completely removed in a future release.

Learn more about the detailed usage of [backup flags](#flags) below.

## Manual Backups

A backup can be triggered manually with the [`SAVE`](../command-reference/server-management/save.md) or [`BGSAVE`](../command-reference/server-management/bgsave.md) commands.

## Automatic Loading

When a Dragonfly instance is started, it will try to find a snapshot file in its current `dir` path and will load it automatically.
Like automatic backups, this can be disabled by configuring `dbfilename` with an empty value.

## Flags

- **`dir`** -- A path to the directory where the backup snapshot files will be saved.
- **`df_snapshot_format`** -- Set to `true` to save snapshots in Dragonfly file format, `true` by default.
- **`dbfilename`** -- The filename to save and load the database. See more details about this flag [below](#the-dbfilename-flag).
- **`snapshot_cron`** -- Generate snapshots based on a cron schedule. See more details about this flag [below](#the-snapshotcron-flag).
- **`save_schedule` (deprecated)** -- Generate snapshots periodically.
The argument is a `HH:MM` format that supports [globbing](https://en.wikipedia.org/wiki/Glob_(programming)) (i.e., `23:45`, `*:15`, `*:*`).
**This flag is deprecated, and the support will be completely removed in a future release.**

### `dbfilename`

The `dbfilename` flag controls the filename Dragonfly uses for loading and saving backup snapshots.
It is notable that the passed argument should only contain the filename without any file extensions.
For instance, if the desired filename is `dump.dfs`, where `.dfs` is the extension for the Dragonfly snapshot file format, then this flag should be set to `dump`.

The flag supports adding timestamps automatically to snapshot filenames.
To generate filenames with timestamps, use the macro `{timestamp}` in the argument passed to this flag (i.e., `dump-{timestamp}`).
The macro will be replaced with timestamps of the local server time upon each snapshot save, in a lexicographically sortable format.

**The default value for this flag is `dump-{timestamp}`.**

Let's look at an example. Start a Dragonfly instance with the following command:

```shell
$> ./dragonfly --logtostderr --dir my-snapshot-dir --dbfilename my-snapshot-file-{timestamp}
```

While the Dragonfly instance is running, issue the [`SAVE`](../command-reference/server-management/save.md) command twice, with 5 seconds in between:

```shell
dragonfly$> SAVE
OK

# 5 seconds later...

dragonfly$> SAVE
OK
```

Then turn off the Dragonfly instance after 5 more seconds, which will trigger an automatic backup snapshot upon shutdown.
Now, inspect the `my-snapshot-dir` directory, which was passed as the argument to the `dir` flag.
There should be 3 snapshots created with the desired filename `my-snapshot-file` with automatic timestamps that are 5 seconds apart.

```shell
$> ls my-snapshot-dir
my-snapshot-file-2023-08-10T04:24:38-0000.dfs
my-snapshot-file-2023-08-10T04:24:38-summary.dfs
my-snapshot-file-2023-08-10T04:24:43-0000.dfs
my-snapshot-file-2023-08-10T04:24:43-summary.dfs
my-snapshot-file-2023-08-10T04:24:48-0000.dfs
my-snapshot-file-2023-08-10T04:24:48-summary.dfs
```

### `snapshot_cron`

- **For Dragonfly version >= 1.7.1, this flag is preferred over `save_schedule`.**
