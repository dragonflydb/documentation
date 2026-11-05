---
description: "Experimental Append Only File (AOF) persistence in Dragonfly: how to enable it, its durability guarantees, and its current limitations."
sidebar_position: 3
---

# Append Only File (AOF)

:::warning Experimental

AOF support is **experimental** and under active development. It is available starting with
Dragonfly v2.1 as an early MVP. The on-disk format, flags, and behavior may change between releases,
and several features (such as log compaction) are not implemented yet.
Do not rely on it as the only copy of production data.
See [Current Limitations](#current-limitations) before enabling it.

:::

Append Only File (AOF) persistence logs every write to disk, so that the dataset can be rebuilt
after a restart or a crash.
Without AOF, Dragonfly persists data only through point-in-time [snapshots](./backups.md),
and a crash loses every write made after the last snapshot.

Unlike the single global log of Redis and Valkey, Dragonfly's AOF is **sharded**:
in line with Dragonfly's shared-nothing architecture, every shard thread writes its own log,
so logging adds no global bottleneck, and shards replay their logs in parallel on startup.
Dragonfly's AOF files are not compatible with Redis or Valkey AOF files.

## Enabling AOF

AOF is enabled at startup with the `--aof` flag. The files are written to the directory set by `--dir`:

```bash
./dragonfly --aof --dir /data
```

With Docker, mount a volume for the data directory:

```bash
docker run -p 6379:6379 -v /path/on/host:/data \
  docker.dragonflydb.io/dragonflydb/dragonfly --aof --dir /data
```

AOF requires:

- **Linux with the io_uring backend.** Dragonfly refuses to start with `--aof` when it runs with
  the epoll backend (for example, with `--force_epoll`).
- **A local `--dir`.** Cloud storage paths (such as `s3://`) are not supported for AOF.
- **A primary (master) instance.** AOF is not supported on replicas: Dragonfly refuses to start
  with both `--aof` and `--replicaof`, and `REPLICAOF host port` fails while AOF is enabled.

AOF cannot be enabled or disabled at runtime with `CONFIG SET`.

### Flags

| Flag                       | Default | Description                                                                                                       |
| -------------------------- | ------- | ----------------------------------------------------------------------------------------------------------------- |
| `--aof`                    | `false` | If true, each shard logs its writes to an append-only file in `--dir`.                                            |
| `--aof_max_buffered_bytes` | `64MB`  | Per shard: unwritten AOF bytes above which the shard blocks until the writes complete. Do not set it below `8KB`. |

### Enabling AOF on an Existing Dataset

On the first start with `--aof`, if a snapshot matching `--dbfilename` exists in `--dir`,
Dragonfly loads it and uses it as the starting point of the AOF.
From then on, every restart loads that snapshot and replays the log on top of it.

- Only Dragonfly-format (DFS) snapshots are supported. With an RDB file, Dragonfly refuses to start with `--aof`.
- **Do not delete or move that snapshot file** while AOF is enabled: if it is missing, Dragonfly refuses to start.

### Files

AOF files live in `--dir`, next to the snapshot files:

```
appendonly.manifest
appendonly-<shard>-<seq>.aof
```

Do not edit, move, or delete these files by hand.

## Restarts

When AOF data exists in `--dir`, Dragonfly restores the dataset from the AOF and does not load `--dbfilename`.
If the end of the log was only partially written, for example after a crash, the incomplete part is discarded.

On a graceful shutdown, Dragonfly flushes every log to disk.
With `--aof`, Dragonfly does not save a snapshot on shutdown, since the log already holds the data.

## Durability Guarantees

Writes are flushed to disk once per second, similar to `appendfsync everysec` in Redis.
Replies to clients do not wait for the disk, so the loss window is best effort:

- **Process crash** (segfault, OOM kill, `kill -9`): only the most recent writes (typically a few milliseconds) can be lost.
- **OS crash or power loss:** about the last second of writes can be lost.
- A slow disk can stretch both windows.

Consistency after a crash:

- Each shard recovers its writes in order, up to the point of the crash.
- Transactions are **not** atomic across a crash. A `MULTI`/`EXEC` block or a Lua script may be applied partially,
  and a multi-shard transaction may be applied on some shards only.

## Current Limitations

The following are not supported yet in the current MVP:

- **No log compaction or rewrite.** The log grows without bound: `SAVE`, `BGSAVE`, and `--snapshot_cron`
  produce regular snapshots, but they do not shrink the log. There is no `BGREWRITEAOF` equivalent.
  Monitor the disk usage of `--dir`. Restart time also grows with the size of the log.
- **Fixed fsync policy.** There is no `appendfsync always` or `appendfsync no` equivalent.
- **The number of threads cannot change.** Changing `--proactor_threads` or `--num_shards`
  between restarts makes startup fail.
- **Startup blocks until the dataset is restored.** The server does not accept connections until it has
  loaded the log, instead of answering with a `LOADING` error.
- **Disk errors stop logging.** If a write to the log fails, the server keeps serving requests,
  but later writes are not logged until a restart, and they are lost on that restart.
- **Some crashes need manual recovery.** In rare cases, a crash can leave a log that Dragonfly cannot
  recover from automatically yet, and startup fails.
- **Expired keys during recovery.** Keys whose expiration time passed while the server was down
  may be restored incorrectly. For example, a key set with a TTL that was later removed with
  `PERSIST` may be missing after the restart.
- **Not supported on replicas**, and it cannot be combined with `REPLICAOF`.
- **No `INFO` metrics** for AOF yet.
- **Commands that load data directly**, such as `DFLY LOAD` or `DEBUG RELOAD`, are not supported with AOF.

If you have feedback on AOF or run into an issue, open an issue on [GitHub](https://github.com/dragonflydb/dragonfly/issues)
or join the conversation on our [Discord server](https://discord.com/invite/HsPjXGVH85).
