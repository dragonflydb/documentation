---
sidebar_position: 0
---

# Snapshot and Restore

Snapshot and Restore is a commonly used technique for migrating data between database instances.
To migrate a Redis instance to a Dragonfly instance, we can configure Redis to automatically save snapshots on disk or
manually call the [`SAVE`](https://redis.io/commands/save/) (or [`BGSAVE`](https://redis.io/commands/bgsave/)) command.

Once a point-in-time snapshot file (RDB file) is created, we can use it to bootstrap data into a Dragonfly instance.
During initialization, Dragonfly will try to find the RDB file in its `dir` path and will load it automatically, where `dir` is a configurable parameter.

To learn more about snapshot files and Dragonfly snapshot mechanism, please refer to the [Dragonfly Point-in-Time Snapshotting Design](../../managing-dragonfly/snapshotting.md) documentation page.
You can also learn more about [Saving Backups](../../managing-dragonfly/backups.md) and the related `dir` and `dbfilename` configuration flags.

## Migration Steps

- We have a Redis instance running. Issue the `SAVE` or `BGSAVE` command to create a snapshot.

```shell
redis> SAVE
OK
```

- Locate the RDB file `dump.rdb`.
- Note that by default, Redis saves the RDB file to the directory `/var/lib/redis/` in Linux.
- If running with Docker, Redis image(s) may be configured to save the RDB file to the `/data` directory in the container.

```shell
$> ls /var/lib/redis/
dump.rdb
```

- Once we have the RDB file, we can configure Dragonfly with the directory and filename for saving and loading snapshots.
- Copy the original RDB file `dump.rdb` to desired directory (`/data` in this example).
- Assume we have the Dragonfly binary within the current directory as well.

```shell
$> tree
.
├── data
│   └── dump.rdb # Redis snapshot dump file
└── dragonfly    # Dragonfly binary
```

- By using the following command to run Dragonfly, upon successful start, the Dragonfly instance should contain data from the `dump.rdb` file.
- The `dir` flag specifies where the snapshot file will be loaded and saved. And the `dbfilename` flag specifies the filename to load and save the database.

```shell
$> ./dragonfly --logtostderr --dir ./data --dbfilename dump
```
