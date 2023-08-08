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

- Locate the snapshot dump file `dump.rdb`.
- Note that by default, Redis saves the snapshot dump file to the directory `/var/lib/redis/` in Linux.
- If running with Docker, Redis image(s) may be configured to save the dump file to the `/data` directory in the container.

```shell
$> ls /var/lib/redis/
dump.rdb
```

- Once we have the snapshot dump file, we can configure Dragonfly with the directory name and filename for saving and loading the database.
- Copy the original Redis snapshot dump file `dump.rdb` to desired directory (`/data` in this example).
- Assume we have the Dragonfly binary within the current directory as well.

```shell
$> tree
.
├── data
│   └── dump.rdb # Redis snapshot dump file
└── dragonfly    # Dragonfly binary
```

- If using the following command to run Dragonfly, upon successful start, the Dragonfly instance should contain the data from the `dump.rdb` file.

```shell
$> ./dragonfly --logtostderr --dir ./data --dbfilename dump
```

- Read more about [Saving Backups](../../managing-dragonfly/backups.md) and the related configuration flags `dir` and `dbfilename`.
