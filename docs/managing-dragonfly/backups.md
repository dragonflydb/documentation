---
sidebar_position: 5
---

# Saving Backups

A Dragonfly instance can generate disk backups both automatically and manually.
A number of flags influence the behavior of the backup mechanism. The flags can be given through
the command line or with a [flagfile](../getting-started/binary.md#flag-files).

## Automatic Backups
Dragonfly can be configured to fo a scheduled backup with the `save_schedule` flag. In addition,
Dragonfly will create a backup on shutdown whenever the `dbfilename` flag is not empty.

## Manual Backups
A backup can be triggered manually with the [`SAVE`](../command-reference/server-management/save.md) command.

## Automatic Loading
When a dragonfly instance is started, it will try to find a dump file in its current `dir` path and will load it automatically.
Like automatic backups, this can be disabled by configuring `dbfilename` with an empty value.

## Flags

* **`dir`** - A path to the folder where the dump will be saved.
* **`df_snapshot_format`** - Set true to save dump in Dragonfly file format (true by default).
* **`dbfilename`** - The file name to save and load the database. To generate a file with a timestamp, set the macro `{timestamp}` in the filename, e.g. `dump-{timestamp}`.
The macro will be replaced with a timestamp of the local time in a lexicographically sorted format.
The default filename is `dump-{timestamp}`.
* **`save_schedule`** - Generate snapshots periodically. The argument is a `HH:MM` format that supports globbing (e.g. `23:45`, `*:15`, `*:*`)
