---
description: "Experimental per-shard append-only file (AOF) in Dragonfly v2.1.0: how to enable it, the files it writes, startup and replay, durability, and snapshots."
sidebar_position: 3
---

# Append Only File (AOF)

Append Only File (AOF) captures every write operation received by the server.
Upon server restart, these operations are replayed to reconstruct the original dataset.

:::caution Experimental

Dragonfly v2.1.0 includes an experimental AOF. It is disabled by default and enabled with the `--aof` flag.
Snapshots remain the default persistence method: see [Saving Backups](./backups.md) and the [snapshotting design](./snapshotting.md).

:::

## Differences from Valkey AOF

Dragonfly's AOF works differently from [Valkey AOF](https://valkey.io/topics/persistence/):

- Each shard writes its own log, in Dragonfly's binary format rather than the Redis protocol.
  Dragonfly cannot load Valkey or Redis AOF files, and their tools cannot read Dragonfly's logs.
  To move data from Valkey or Redis, use [an RDB snapshot](../migrating-to-dragonfly/01-from-redis-instance/00-snapshot-and-restore.md) instead.
- AOF can only be enabled at startup, with `--aof`. There is no `appendonly` or `appendfsync` setting.
- There is no fsync policy: written data is flushed to disk once per second.
- There is no rewrite or compaction. `BGREWRITEAOF` and `WAITAOF` are unknown commands.

## Enabling AOF

Start Dragonfly with `--aof`:

```bash
./dragonfly --aof --dir=/var/lib/dragonfly --proactor_threads=4
```

Without `--dir`, the files are written to the working directory.
A log is replayed with the shard count it was written with: [`--num_shards`](./flags.md#--num_shards) if set,
otherwise the number of threads. Set [`--proactor_threads`](./flags.md#--proactor_threads) explicitly instead of relying on the CPU count.

With Docker, Dragonfly also needs a seccomp profile that allows io_uring:

```bash
docker run -p 6379:6379 --ulimit memlock=-1 --security-opt seccomp=unconfined \
  -v dragonfly-data:/data \
  docker.dragonflydb.io/dragonflydb/dragonfly --aof --proactor_threads=4
```

The working directory of the image is `/data`, so the AOF files go to the `dragonfly-data` volume.
Docker's default seccomp profile blocks io_uring.
Without `--security-opt seccomp=unconfined`, Dragonfly switches to epoll and exits
(in this and the following log excerpts, timestamps, thread ids, offsets, sizes and LSNs vary):

```text
W20261105 12:10:43.740739     6 dfly_main.cc:573] Check if io_uring is disabled via /proc/sys/kernel/io_uring_disabled. Switching to epoll.
E20261105 12:10:43.747426     6 server_family.cc:1076] --aof needs io_uring
```

Instead of `unconfined`, you can pass a custom seccomp profile:
Docker's default profile with the `io_uring_setup`, `io_uring_enter` and `io_uring_register` system calls added to the allowed ones.

### Requirements

AOF runs only on Linux. Dragonfly checks the following at startup and exits with the error shown if a requirement is not met:

| Requirement | Startup error |
| --- | --- |
| io_uring: Linux kernel 5.10 or newer, io_uring not disabled or blocked by seccomp, enough locked memory, no [`--force_epoll`](./flags.md#--force_epoll) | `--aof needs io_uring` |
| A local [`--dir`](./flags.md#--dir): `s3://`, `gs://` and Azure Blob paths are not supported | `--aof needs a local --dir` |
| [`--hz`](./flags.md#--hz) greater than `0`, because the heartbeat writes the log | `--aof needs --hz > 0, the heartbeat seals AOF blocks` |
| Not a replica: no [`--replicaof`](./flags.md#--replicaof) | `--aof is not supported on replicas` |

At runtime, the AOF flags cannot be changed, and an instance started with `--aof` refuses to become a replica:

```shell
dragonfly> CONFIG SET aof true
(error) ERR Unknown option or number of arguments for CONFIG SET - 'aof'
dragonfly> CONFIG GET aof*
(empty array)
dragonfly> REPLICAOF 10.0.0.2 6379
(error) ERR REPLICAOF is not supported with --aof
```

### Flags

- **`--aof`**: If true, each shard logs its writes to an append-only file in `--dir`. Default: `false`.
- **`--aof_max_buffered_bytes`**: Per shard, the amount of logged data not yet written to disk above which the shard blocks until writes complete. Default: `64MiB`.
  Do not set it below `8kb`, the size of a log block.

## Files in `--dir`

With two shards, `--dir` contains these files while Dragonfly runs:

```text
appendonly-0-0.aof
appendonly-0-1.aof
appendonly-1-0.aof
appendonly-1-1.aof
appendonly.manifest
```

- `appendonly.manifest` records the base snapshot, the shard count and where each shard's log starts.
  It is protected by a checksum. A damaged manifest stops startup with `failed to read the AOF manifest: invalid AOF manifest`.
- `appendonly-<shard>-<seq>.aof` are the log segments of each shard.
  Every start continues the log in a new segment, and while Dragonfly runs, each shard keeps its next, still empty segment ready.
  A clean shutdown deletes the empty segment. After a crash, it stays.
- `*.discarded` files are segments that crash recovery set aside. Dragonfly never reads them.
- The base snapshot, if one was adopted at the first start, stays where it is. Dragonfly never deletes it.

## Startup

### First Start

When `--dir` has no AOF manifest, Dragonfly starts a new log:

- If `--dir` has a snapshot that matches [`--dbfilename`](./backups.md#the-dbfilename-flag) (for the default `dump-{timestamp}`, the newest one),
  Dragonfly loads it and uses the file in place as the base of the log. Without a snapshot, the log starts from an empty dataset.
- The base must be in Dragonfly format. An RDB file stops startup with `--aof adopts only DFS dumps for now, found /data/dump.rdb`.
  To start from an RDB file, start Dragonfly once without `--aof` so that it loads the file,
  run [`SAVE DF`](../command-reference/server-management/save.md), and stop it with `SHUTDOWN NOSAVE`,
  so that the newest snapshot is the one in Dragonfly format. Then start it with `--aof`.
  If an earlier start with `--aof` stopped at the RDB file, this start logs `Redoing an interrupted AOF bootstrap`, which is expected.
- If `--dir` contains AOF segments but no manifest, Dragonfly does not start: `AOF files in /data but no manifest, e.g. /data/appendonly-0-0.aof`.

### Later Starts

On later starts, Dragonfly does not look for snapshots by `--dbfilename`. Instead, it:

1. Loads the base named in the manifest. If the file is gone, startup stops with `the AOF base /data/dump-summary.dfs is missing`.
2. Replays each shard's log on top of the base, all shards in parallel.
3. Continues each shard's log in a new segment.

Startup blocks until the base is loaded and the log is replayed.
Configure startup and liveness probes to allow for the replay time.
Because v2.1.0 has no compaction, every start replays the entire log since the base, and the replay takes longer as the log grows.

## Durability

Replies do not wait for the disk:

- Each shard collects its log records in blocks of up to 8 KB and writes a block when it is full or at the next heartbeat:
  every 10 ms with the default `--hz` of `100` (every `1000 / hz` milliseconds).
- Once per second, each shard flushes what it has written with `fdatasync`.

A crash of the Dragonfly process loses the records that have not reached the file yet:
up to one heartbeat interval of writes, plus any blocks still queued for the disk, which `--aof_max_buffered_bytes` limits per shard.
A crash of the machine or a power loss can also lose about the last second of written data.
A clean shutdown, with `SIGTERM` or [`SHUTDOWN`](../command-reference/server-management/shutdown.md), writes and syncs every logged record before Dragonfly exits.

## Crash Recovery

After a crash, the end of a shard's log can be missing or damaged.
At startup, Dragonfly replays each shard's log up to its last valid block, cuts off the rest, and logs:

```text
W20261105 12:13:05.864750    11 aof_chain_reader.cc:247] AOF shard 0: damaged tail of 300 bytes after lsn 2
W20261105 12:13:05.864760    11 execution_state.cc:93] ReportError: AOF log ends with a damaged tail
```

Damage is never skipped: everything after the first damaged block of a shard is dropped, and the later segments of that shard are renamed to `*.discarded`.

## Snapshots and AOF

In v2.1.0, snapshots do not shorten the log.
[`SAVE`](../command-reference/server-management/save.md), [`BGSAVE`](../command-reference/server-management/bgsave.md)
and [`--snapshot_cron`](./backups.md#the-snapshot_cron-flag) write regular snapshots, and the manifest keeps the base from the first start.

- With `--aof`, Dragonfly writes no snapshot on shutdown, not even with `SHUTDOWN SAVE`.
- Keep a `{timestamp}` in `--dbfilename`, as in the default `dump-{timestamp}`, so that every save writes new files and the base snapshot of the log stays unchanged.
- Do not delete or move the base snapshot. Its file name is in `appendonly.manifest`.

## Starting a New AOF from a Snapshot

There is no log compaction in v2.1.0: segments are never deleted, and every start adds one per shard.
To shrink the log or change the shard count, start a new AOF from a snapshot:

1. Stop the clients that write to Dragonfly. Writes made after the next step are lost.
2. Run `SAVE DF`. With a `{timestamp}` in `--dbfilename`, it writes a new snapshot in Dragonfly format.
3. Stop Dragonfly. With `--aof`, it writes no other snapshot on shutdown.
4. Move `appendonly.manifest` and every `appendonly-*` file out of `--dir`.
5. Start Dragonfly with `--aof`, and with a new `--proactor_threads` value if you change the shard count.
   The newest snapshot that matches `--dbfilename` becomes the base of a new, empty log.

## Monitoring

`INFO` has no AOF fields, and Dragonfly exports no AOF metrics. AOF messages appear in the server log.

If you have any thoughts or suggestions about AOF, we encourage you to join the conversation on our [Slack community](https://join.slack.com/t/dragonflycommunityhq/shared_invite/zt-4ftpylx50-SQZ0g0CD2lJMvi0EsqPNbQ).
