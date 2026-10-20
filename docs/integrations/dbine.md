---
sidebar_position: 1
description: DBine
---

# DBine

## Introduction

[DBine](https://dbine.com) is a free, open source (MIT licensed) desktop database manager for Windows, macOS, and Linux, with 130+ databases and cloud services in the same window. It has a key browser, a command editor, and a server monitor for Redis-compatible servers.

DBine has a **Dragonfly** connection type. It speaks the Redis protocol and reads Dragonfly's own fields where they differ from Redis, for example the version from `dragonfly_version`.

## TL;DR

Run Dragonfly with its port published, then add a **Dragonfly** connection in DBine pointed at `localhost` and port `6379`.

```sh
docker run -p 6379:6379 --ulimit memlock=-1 docker.dragonflydb.io/dragonflydb/dragonfly:latest
```

## Running DBine with Dragonfly

### 1. Start Dragonfly

```sh
docker run -p 6379:6379 --ulimit memlock=-1 docker.dragonflydb.io/dragonflydb/dragonfly:latest
```

### 2. Install DBine

Download and install DBine from the [releases page](https://github.com/addlayer-io/dbine/releases).

### 3. Create a connection

1. In DBine, click **New connection**.
1. Select **Dragonfly** from the list of engines.
1. Fill in the server (`localhost`) and port (`6379`) of your Dragonfly instance, and the database number (`0` by default). Add a user and password if your instance requires them.
1. For an instance with TLS, open the **SSL/TLS** tab and select **Encrypt the connection (TLS)**.
1. Click **Test connection** to verify, then **Save and connect**.

The connection appears in the **Explorer**, with one node per logical database.

## What you can do

- **Browse keys.** The key browser lists keys with `SCAN` (never `KEYS`), groups them by prefix, and shows each key's type and TTL. You can search with a `MATCH` pattern and filter by type.
- **Run commands.** Right-click a database and choose **New query** to run single commands or scripts. Each reply is shown as a table, for example `ZREVRANGE leaderboard 0 4 WITHSCORES` as members and scores.
- **Edit values.** Changes made in the value editor are turned into commands that DBine adds to the editor, so you review them before running them.
- **Monitor the server.** Right-click the connection and choose **Monitor** for the server information, the client list (with `CLIENT KILL`), and a profiler built on `MONITOR`.
- **Use a read-only connection.** Select **Read-only** in the connection form, and DBine refuses commands that write.

## Limitations

- Dragonfly has no `CLIENT UNBLOCK`, so the client list doesn't offer cancelling a client's blocking command. Closing the client with `CLIENT KILL` is available.
- The profiler uses `MONITOR`, which reports the commands but not their durations.

The key browser, the command editor, and the monitor were tested against `docker.dragonflydb.io/dragonflydb/dragonfly:latest`.

## Useful Resources

- DBine [Homepage](https://dbine.com) and [GitHub](https://github.com/addlayer-io/dbine).
