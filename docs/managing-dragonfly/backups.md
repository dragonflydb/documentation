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

- **The `snapshot_cron` flag was introduced in Dragonfly version >= 1.7.1**
- **For Dragonfly version < 1.7.1, only the `save_schedule` flag could be used.**

Learn more about backup [Flags](#flags) below.

## Manual Backups

A backup can be triggered manually with the [`SAVE`](../command-reference/server-management/save.md) or [`BGSAVE`](../command-reference/server-management/bgsave.md) commands.

## Automatic Loading

When a Dragonfly instance is started, it will try to find a snapshot file in its current `dir` path and will load it automatically.
Like automatic backups, this can be disabled by configuring `dbfilename` with an empty value.

## Flags

- **`dir`** -- A path to the directory where the backup snapshot files will be saved.

- **`df_snapshot_format`** -- Set to `true` to save snapshots in Dragonfly file format, `true` by default.

- **`dbfilename`** -- The filename to save and load the database.
  - To generate a file with a timestamp, set the macro `{timestamp}` in the filename (i.e., `dump-{timestamp}`).
  - The macro will be replaced with a timestamp of the local server time upon save, in a lexicographically sortable format.
  - The default filename is `dump-{timestamp}`.

- **`snapshot_cron`** -- Generate snapshots based on a cron schedule.
  - **For Dragonfly version >= 1.7.1, this flag is preferred over `save_schedule`.**

- **`save_schedule` (deprecated)** -- Generate snapshots periodically.
  - **This flag is deprecated, and the support will be completely removed in a future release.**
  - The argument is a `HH:MM` format that supports [globbing](https://en.wikipedia.org/wiki/Glob_(programming)) (i.e., `23:45`, `*:15`, `*:*`).
