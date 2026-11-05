---
description: "Experimental per-shard append-only file (AOF) in Dragonfly v2.1.0: how to enable it, startup and replay, durability, and current limitations."
sidebar_position: 3
---

# Append Only File (AOF)

Append Only File (AOF) captures every write operation received by the server.
Upon server restart, these operations are replayed to reconstruct the original dataset.

:::caution Experimental

Dragonfly v2.1.0 includes an experimental AOF. It is disabled by default and enabled with the `--aof` flag.
It has no log compaction yet, and some crashes leave a log that Dragonfly cannot replay without manual recovery.
Read the [limitations](#limitations) before you rely on it.
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
A log can only be replayed with the shard count it was written with (see [limitations](#limitations)),
so set [`--proactor_threads`](./flags.md#--proactor_threads) explicitly instead of relying on the CPU count.

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
  With a smaller value, a shard can hang for good once keys start to expire:
  in a test with `4kb`, writes never completed and the server did not stop until it was killed.

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

At the end of the replay, each shard logs the following warning.
It marks the normal end of the log, not a disk error:

```text
W20261105 12:12:35.756007    11 execution_state.cc:93] ReportError: Input/output error
```

Startup blocks until the base is loaded and the log is replayed.
Unlike a regular snapshot load, which answers with `LOADING` errors meanwhile, Dragonfly accepts TCP connections during the replay but answers no command until it finishes,
so clients and health checks wait or time out. Configure startup and liveness probes to allow for the replay time.
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

If a write or `fdatasync` fails, for example because the disk is full, that shard stops writing its log until Dragonfly restarts.
Clients keep getting normal replies, and only the server log shows the failure:

```text
E20261105 12:16:27.472812    11 aof_segment_writer.cc:199] AOF write failed at offset 2082650: No space left on device
```

The writes made after the failure are not in the log, and the next restart loses them.
If the last block that reached the disk ends inside a record, which is likely under write load,
the restart fails instead, as described in [Crash Recovery](#crash-recovery).
Watch the server log for `AOF write failed` and `AOF fdatasync failed`.
To keep the data, free disk space and [start a new AOF from a snapshot](#starting-a-new-aof-from-a-snapshot) before you restart Dragonfly.

## Crash Recovery

After a crash, the end of a shard's log can be missing or damaged.
At startup, Dragonfly replays each shard's log up to its last valid block, cuts off the rest, and logs:

```text
W20261105 12:13:05.864750    11 aof_chain_reader.cc:247] AOF shard 0: damaged tail of 300 bytes after lsn 2
W20261105 12:13:05.864760    11 execution_state.cc:93] ReportError: AOF log ends with a damaged tail
```

Damage is never skipped: everything after the first damaged block of a shard is dropped, and the later segments of that shard are renamed to `*.discarded`.

Each shard's log is recovered on its own.
A multi-key command or a [`MULTI`](../command-reference/generic/multi.md)/`EXEC` transaction that wrote to several shards can therefore come back on only some of them.

Dragonfly v2.1.0 cannot recover the following cases on its own:

- **The log ends inside a record.** A record that does not fit in the rest of a block continues in the next one,
  which is common under write load and always the case for records larger than 8 KB.
  If a crash or a failed write leaves only the first part of such a record in the log, startup fails:

  ```text
  E20261105 13:38:09.394534    11 aof_replay.cc:72] AOF shard 0: the log ends inside a record after lsn 1, resuming after it is not supported yet
  E20261105 13:38:09.394541    11 aof_replay.cc:115] AOF replay failed on shard 0: State not recoverable
  E20261105 13:38:09.394557    11 server_family.cc:1076] AOF replay failed: State not recoverable
  ```

- **A crash during a command that the replay runs on all shards together:**
  [`FLUSHALL`](../command-reference/server-management/flushall.md), [`FLUSHDB`](../command-reference/server-management/flushdb.md),
  and the search index commands `FT.CREATE`, `FT.ALTER`, `FT.DROPINDEX`, `FT.SYNUPDATE`, `FT.ALIASADD`, `FT.ALIASUPDATE` and `FT.ALIASDEL`.
  If the command reached the logs of only some shards, the first restart succeeds, but the logs stay inconsistent.
  A later restart then either fails with `Global commands out of order across flows` and `AOF replay failed: State not recoverable`,
  or, if none of these commands ran in between, it runs the old command again, but only after the shards whose logs lack it have replayed everything:
  an old `FLUSHALL` or `FLUSHDB` then deletes writes made on those shards after the first restart.
  If a crash may have interrupted one of these commands, start a new AOF from a snapshot right after the first restart.

If Dragonfly cannot replay the log, start a new AOF from the newest snapshot in `--dir`, as described [below](#starting-a-new-aof-from-a-snapshot).
The writes logged after that snapshot are lost.

## Snapshots and AOF

In v2.1.0, snapshots do not shorten the log.
[`SAVE`](../command-reference/server-management/save.md), [`BGSAVE`](../command-reference/server-management/bgsave.md)
and [`--snapshot_cron`](./backups.md#the-snapshot_cron-flag) write regular snapshots, and the manifest keeps the base from the first start.

- With `--aof`, Dragonfly writes no snapshot on shutdown, not even with `SHUTDOWN SAVE`.
- Keep a `{timestamp}` in `--dbfilename`, as in the default `dump-{timestamp}`, so that every save writes new files.
  With a fixed name such as `dump`, a save overwrites the snapshot that is the base of the log,
  and the next start replays the entire log on top of the newer data.
  Commands that are not idempotent are then applied twice:
  with a counter at `10` in the base, `INCR`, `SAVE`, `INCR`, `BGSAVE` and a restart left the counter at `14` instead of `12`.
- Do not delete or move the base snapshot. Its file name is in `appendonly.manifest`.
- Do not run `DEBUG RELOAD` or `DFLY LOAD` on an instance started with `--aof`.
  They clear the dataset and load a snapshot, but only the clearing is logged:
  after the next restart, the loaded data is gone, and the writes made after the reload can be discarded as a damaged tail as well.

## Starting a New AOF from a Snapshot

There is no log compaction in v2.1.0: segments are never deleted, and every start adds one per shard.
To shrink the log, change the shard count, or recover from a log that Dragonfly cannot replay, start a new AOF from a snapshot:

1. Stop the clients that write to Dragonfly. Writes made after the next step are lost.
2. Run `SAVE DF`. With a `{timestamp}` in `--dbfilename`, it writes a new snapshot in Dragonfly format.
3. Stop Dragonfly. With `--aof`, it writes no other snapshot on shutdown.
4. Move `appendonly.manifest` and every `appendonly-*` file out of `--dir`.
5. Start Dragonfly with `--aof`, and with a new `--proactor_threads` value if you change the shard count.
   The newest snapshot that matches `--dbfilename` becomes the base of a new, empty log.

If Dragonfly cannot replay the log, skip steps 1 to 3.
The new log then starts from the newest snapshot already in `--dir`, and the writes logged after that snapshot are lost.

## Limitations

- **Fixed shard count.** A log can only be replayed with the shard count it was written with:
  [`--num_shards`](./flags.md#--num_shards) if set, otherwise the number of threads,
  `--proactor_threads`, which defaults to one per available CPU and so follows container CPU limits.
  Otherwise, startup fails with `AOF replay failed: AOF written with a different shard count`.
- **Expired keys can come back.** If the TTL of a key runs out while Dragonfly is stopped, and the key was modified after its TTL was set,
  the replay can recreate the key without a TTL.
  For example, after `SET k 10 EX 2` and `INCRBY k 5`, a restart 3 seconds later returns `k` with the value `5` and no TTL.
  Keys that were not modified after they got their TTL expire as expected.
- **Replication.** Replicas cannot use AOF: `--replicaof` together with `--aof` stops startup,
  and [`REPLICAOF`](../command-reference/server-management/replicaof.md) with a host and port is rejected. An instance started with `--aof` can serve as a primary.
- **Untested combinations.** Dragonfly's AOF tests do not cover replication, [cluster mode](./cluster-mode.md) or [SSD tiering](./tiering.md).
- **No monitoring.** `INFO` has no AOF fields, and there are no AOF metrics. Failures appear only in the server log.

The planned design, including checkpoints that keep the log bounded, is described in the upstream
[design proposal](https://github.com/dragonflydb/dragonfly/blob/v2.1.0/docs/aof.md). Dragonfly v2.1.0 implements only what this page describes.

If you have any thoughts or suggestions about this, we encourage you to join the conversation on our [Discord server](https://discord.com/invite/HsPjXGVH85).
