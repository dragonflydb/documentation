---
sidebar_position: 1
description: Tabularis
---

# Tabularis

## Introduction

[Tabularis](https://tabularis.dev) is an open source (Apache 2.0) desktop SQL workspace for Windows, macOS, and Linux. PostgreSQL, MySQL/MariaDB, and SQLite drivers ship built in; other engines, Redis among them, are added as plugins installed from inside the app. With the Redis plugin installed, keys show up in the same schema explorer, data grid, and editor as the relational databases a team already opens in Tabularis.

Dragonfly speaks the Redis wire protocol, so the Tabularis Redis plugin connects to it the same way it connects to Redis itself. No Dragonfly-specific configuration, flags, or code changes are required.

## TL;DR

Start Dragonfly, install Tabularis and its Redis plugin, then add a connection of type **Redis** pointed at the Dragonfly host and port.

```bash
docker run -p 6379:6379 --ulimit memlock=-1 docker.dragonflydb.io/dragonflydb/dragonfly
```

## Running Tabularis with Dragonfly

### 1. Start Dragonfly

Run Dragonfly locally, for example with Docker:

```bash
docker run -p 6379:6379 --ulimit memlock=-1 docker.dragonflydb.io/dragonflydb/dragonfly
```

See [Getting Started](../getting-started/docker.md) for other installation options.

### 2. Install Tabularis

```bash
winget install Debba.Tabularis      # Windows
brew install --cask tabularis       # macOS
sudo snap install tabularis         # Linux
```

Installers for each platform are also available on the [releases page](https://github.com/TabularisDB/tabularis/releases).

### 3. Install the Redis plugin

Tabularis ships without a Redis driver. Open **Settings > Available Plugins**, find **Redis (Rust)**, and click **Install**. The plugin is downloaded from the Tabularis plugin registry and registered as a new database type without restarting the app. A second plugin, **Redis (Go)**, offers read-only access if you prefer that.

### 4. Create a connection

1. Click **Add Connection**.
1. Under **Database type**, select **Redis (Rust)**.
1. Fill in the host (`127.0.0.1` for the container above) and port (`6379`), and pick a logical database index (0 by default).
1. If Dragonfly runs with `--requirepass`, enter the password. With ACL users configured, enter the username as well.
1. Click **Test Connection** to verify, then **Save**.

Open the connection from the connection manager. The keyspace appears in the schema explorer as a set of virtual tables.

## What you can do

- **Browse keys.** The `__redis_keys__` table lists every key with its type, a value preview, and TTL. Keys that share a prefix (`user:1`, `user:2`, ...) are also grouped into a `__keys:user__` table of their own.
- **Inspect by data structure.** The `hashes`, `lists`, `sets`, `zsets`, and `streams` tables expose key contents by type, and rows can be inserted, updated, and deleted inline from the data grid.
- **Read server stats.** The plugin parses `INFO` into version, memory, clients, and keyspace figures, and lists active Pub/Sub channels with their subscriber counts.

## Notes

- Dragonfly publishes its Redis compatibility level under `redis_version` (7.4.0 for `df-v2.0.0`) and its own version under `dragonfly_version`. A client that reads the standard field, as the Redis plugin does, reports the former.
- The connection form takes a single host and port. Cluster and Sentinel discovery are not implemented, which does not affect a Dragonfly instance.

## Useful Resources

- Tabularis [Homepage](https://tabularis.dev) and [GitHub](https://github.com/TabularisDB/tabularis).
- Redis plugins: [Rust](https://github.com/nicholas-papachriston/tabularis-redis-plugin) and [Go](https://github.com/gzamboni/tabularis-redis-plugin-go).
