---
sidebar_position: 0
---

# Snapshot and Restore

Snapshot and Restore is a commonly used technique for migrating data between database instances.
To migrate a Redis instance to a Dragonfly instance, we can configure Redis to automatically save snapshots on disk or
manually call the [`SAVE`](https://redis.io/commands/save/) (or [`BGSAVE`](https://redis.io/commands/bgsave/)) command.

Once an RDB file is created, we can use it to bootstrap data into a Dragonfly instance.
During startup, Dragonfly will try to find the snapshot dump file in its current directory path and will load it automatically.

To learn more about RDB files and Dragonfly snapshot mechanism, please refer to the [Dragonfly Point-in-Time Snapshotting Design](../../managing-dragonfly/snapshotting.md) documentation

## Migration Steps

- We have a Redis instance running. Issue the `SAVE` or `BGSAVE` command to create a snapshot.

```shell
redis> SAVE
OK
```

- By default, Redis saves the snapshot dump file `dump.rdb` to the directory `/var/lib/redis/`

```shell
bash> ls /var/lib/redis/
dump.rdb
```

```shell
./dragonfly --logtostderr --dir ./data  --dbfilename dump
```
