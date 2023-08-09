---
sidebar_position: 0
---

# Snapshot and Restore

Snapshot and Restore is a widely adopted technique for migrating data across different database instances.
To facilitate a transition from a Redis setup to a Dragonfly environment, the process involves configuring Redis to generate snapshots, known as RDB (Redis Database) files, on disk.
Alternatively, users can manually trigger the [`SAVE`](https://redis.io/commands/save/) or [`BGSAVE`](https://redis.io/commands/bgsave/) command to create these snapshots.

To migrate the Redis data into a Dragonfly instance, the first step is to obtain the point-in-time snapshot, represented by the RDB file.
As part of the Dragonfly initialization process, the system locates the designated `dir` path, a configurable flag that points to the directory where Dragonfly manages its on-disk data.
This is where the RDB file should be placed for automatic loading during startup.

Dragonfly's seamless migration is further enhanced by its automated recognition of the RDB file.
Upon identifying the snapshot in the specified dir path, Dragonfly efficiently loads the data encapsulated within, streamlining the migration process.

For a deeper understanding of the intricacies surrounding snapshot files and the intricacies of Dragonfly's snapshot mechanism, you can delve into the comprehensive resource provided in the [Dragonfly Point-in-Time Snapshotting Design](../../managing-dragonfly/snapshotting.md) documentation page.
Additionally, to learn more about managing backups within Dragonfly, the [Saving Backups](../../managing-dragonfly/backups.md) section offers invaluable insights into configuring crucial flags like `dir` and `dbfilename`.

## Migration Steps

The Snapshot and Restore technique streamlines the migration of data from a running Redis instance to a Dragonfly environment through the use of snapshots.
The steps outlined below guide you through the transition process:

### 1. Create a Redis Snapshot

Begin by initiating a snapshot of the Redis data using the `SAVE` or `BGSAVE` command:

```shell
redis> SAVE
OK
```

### 2. Locate the RDB File

After issuing the snapshot command, you'll find the resulting RDB file named `dump.rdb`.
If you're utilizing Docker, be aware that the Redis image configuration might direct the RDB file to the `/data` directory within the container.
By default, Redis saves this file in the `/var/lib/redis/` directory on Linux systems:

```shell
$> ls /var/lib/redis/
dump.rdb
```

### 3. Configure Dragonfly

Prepare Dragonfly for the migration process by configuring the appropriate directory and filename settings for snapshot management.
For illustration purposes, let's assume the original RDB file `dump.rdb` is copied to the desired directory `/data`, and the Dragonfly binary resides within the same directory:

```shell
$> tree
.
├── data
│   └── dump.rdb # original Redis snapshot dump file
└── dragonfly    # Dragonfly binary
```

### 4. Launch Dragonfly

To successfully initiate the Dragonfly instance with the Redis snapshot, execute the following command.
Ensure that the Dragonfly binary is present in the directory:

```shell
$> ./dragonfly --logtostderr --dir ./data --dbfilename dump
```

In the command above, the `dir` flag designates the location for loading and saving snapshot files, while the `dbfilename` flag specifies the filename used for the database.

### 5. Reconfigure and Restart Applications

As part of the migration process, update the connection string or credentials used by your server applications to connect to Dragonfly.
This step involves modifying your applications' configuration to point to the Dragonfly instance instead of the previous Redis instance.

## Downtime Considerations

It's important to note that this migration technique may involve a downtime window for your application.
During the transition period, data synchronization between the old Redis instance and the new Dragonfly instance might not be possible.
Be sure to plan and communicate the downtime to minimize disruptions to your users or services.
