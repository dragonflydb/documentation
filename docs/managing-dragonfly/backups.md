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

When a Dragonfly instance is started, it will try to find a snapshot file in its configured `dir` path and will load it automatically.
Like automatic backups, this can be disabled by configuring `dbfilename` with an empty value.

## Flags

- **`dir`** -- A path to the directory where the backup snapshot files will be saved.
- **`df_snapshot_format`** -- Set to `true` to save snapshots in Dragonfly file format, `true` by default.
- **`dbfilename`** -- The filename to save and load the database. See more details about this flag [below](#the-dbfilename-flag).
- **`snapshot_cron`** -- Generate snapshots based on a cron schedule. See more details about this flag [below](#the-snapshot_cron-flag).
- **`save_schedule` (deprecated)** -- Generate snapshots periodically.
The argument is a `HH:MM` format that supports [globbing](https://en.wikipedia.org/wiki/Glob_(programming)) (i.e., `23:45`, `*:15`, `*:*`).
**This flag is deprecated, and the support will be completely removed in a future release.**

### The `dbfilename` Flag

The `dbfilename` flag controls the filename Dragonfly uses for loading and saving backup snapshots.
It is notable that the passed argument should only contain the filename without any file extensions.
For instance, if the desired filename is `dump.dfs`, where `.dfs` is the extension for the Dragonfly snapshot file format, then this flag should be set to `dump`.

The flag supports adding timestamps automatically to snapshot filenames.
To generate filenames with timestamps, use the macro `{timestamp}` in the argument passed to this flag (i.e., `dump-{timestamp}`).
The macro will be replaced with timestamps of the local server time upon each snapshot save, in a lexicographically sortable format.

**The default value for this flag is `dump-{timestamp}`.**

Let's look at an example using the `dbfilename` flag. Start a Dragonfly instance with the following command:

```shell
$> ./dragonfly --logtostderr --dir my-snapshot-dir --dbfilename my-snapshot-file-{timestamp}
```

While the Dragonfly instance is running, issue the [`SAVE`](../command-reference/server-management/save.md) command twice, with roughly 5 seconds in between:

```shell
dragonfly$> SAVE
OK

# 5 seconds later...

dragonfly$> SAVE
OK
```

Subsequently, deactivate the Dragonfly instance about 5 seconds later.
This action will promptly initiate an automatic backup snapshot as the Dragonfly instance shuts down.
At this point, examine the contents of the `my-snapshot-dir` directory, which was initially designated as the input argument for the `dir` flag.
Within this directory, you should now observe the presence of three snapshots, each bearing the intended filename `my-snapshot-file`,
distinguished by generated timestamps replacing the `{timestamp}` macro, spaced approximately 5 seconds apart.

```shell
$> ls my-snapshot-dir
my-snapshot-file-2023-08-10T07:23:02-0000.dfs
my-snapshot-file-2023-08-10T07:23:02-summary.dfs
my-snapshot-file-2023-08-10T07:23:07-0000.dfs
my-snapshot-file-2023-08-10T07:23:07-summary.dfs
my-snapshot-file-2023-08-10T07:23:12-0000.dfs
my-snapshot-file-2023-08-10T07:23:12-summary.dfs
```

### The `snapshot_cron` Flag

In Dragonfly >= 1.7.1, the `snapshot_cron` flag was introduced.
When available, it's highly recommended to prioritize the `snapshot_cron` flag over the deprecated `save_schedule` flag.
As implied by its name, `snapshot_cron` establishes a cron schedule for the Dragonfly instance, enabling automatic backup snapshots.

Cron (or crontab) serves as a widely used job scheduler on Unix-like operating systems:

- If you'd like to delve deeper into cron, you can explore its [Wikipedia page](https://en.wikipedia.org/wiki/Cron).
- The [crontab guru](https://crontab.guru/) website is a useful online tool to translate and validate your cron schedule.

The general structure of the cron schedule is as follows:

```text
┌───────────────────── minute (0 - 59)
│ ┌─────────────────── hour (0 - 23)
│ │ ┌───────────────── day of the month (1 - 31)
│ │ │ ┌─────────────── month (1 - 12)
│ │ │ │ ┌───────────── day of the week (0 - 6) (Sunday to Saturday)
│ │ │ │ │
│ │ │ │ │
│ │ │ │ │
* * * * *
```

Here are some cron schedule examples:

| CRON	             | Description                                    |
|-------------------|------------------------------------------------|
| `* * * * *`       | At every minute                                |
| `*/5 * * * *`     | At every 5th minute                            |
| `*/30 * * * *`    | At every 30th minute                           |
| `0 */2 * * *`     | At minute 0 past every 2nd hour                |
| `5 */2 * * *`     | At minute 5 past every 2nd hour                |
| `0 0 * * *`       | At 00:00 (midnight) every day                  |
| `0 0 * * 1-5`     | At 00:00 (midnight) from Monday through Friday |
| `0 6 * * 1-5`     | At 06:00 (dawn) from Monday through Friday     |

Let's look at an example using the `snapshot_cron` flag. Start a Dragonfly instance with the following command:

```shell
$> ./dragonfly --logtostderr --dir my-snapshot-dir --snapshot_cron "*/5 * * * *"
```

The Dragonfly instance will automatically create backup snapshots at every 5th minute.

```shell
$> ls my-snapshot-dir
dump-2023-08-10T00:00:00-0000.dfs
dump-2023-08-10T00:00:00-summary.dfs
dump-2023-08-10T00:05:00-0000.dfs
dump-2023-08-10T00:05:00-summary.dfs
dump-2023-08-10T00:10:00-0000.dfs
dump-2023-08-10T00:10:00-summary.dfs
dump-2023-08-10T00:15:00-0000.dfs
dump-2023-08-10T00:15:00-summary.dfs
dump-2023-08-10T00:20:00-0000.dfs
dump-2023-08-10T00:20:00-summary.dfs
dump-2023-08-10T00:25:00-0000.dfs
dump-2023-08-10T00:25:00-summary.dfs
# ... more
# ... output
# ... omitted
```
