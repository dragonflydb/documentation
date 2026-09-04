---
sidebar_position: 1
description: LibreDB Studio
---

# LibreDB Studio

## Introduction

[LibreDB Studio](https://libredb.org) is an open source (MIT licensed) database IDE that runs in a browser: a query editor, a key browser, and a monitoring dashboard for a wide range of database engines, including Redis. It ships as a container, a Helm chart, or an npm package rather than a desktop download, so it runs next to your Dragonfly instance instead of on your laptop.

Dragonfly speaks the Redis wire protocol, so LibreDB Studio connects to it the same way it connects to Redis itself, through the [`ioredis`](https://github.com/redis/ioredis) driver. No Dragonfly-specific configuration, flags, or code changes are required.

## TL;DR

Run LibreDB Studio as a container next to Dragonfly, add a connection of type **Redis** pointed at your Dragonfly host and port, and use the query editor, key browser, and monitoring dashboard as you would against Redis.

```sh
docker run -p 3000:3000 ghcr.io/libredb/libredb-studio:latest
```

## Running LibreDB Studio with Dragonfly

### 1. Start Dragonfly

```sh
docker run --name dragonfly -p 6379:6379 --ulimit memlock=-1 docker.dragonflydb.io/dragonflydb/dragonfly:latest
```

### 2. Start LibreDB Studio

```sh
docker run -p 3000:3000 ghcr.io/libredb/libredb-studio:latest
```

A Helm chart and an npm package (`npx @libredb/studio`) are also available. See the [LibreDB Studio repository](https://github.com/libredb/libredb-studio) for details.

### 3. Create a connection

1. Open LibreDB Studio in your browser and sign in.
1. Click the **+** button to add a new connection.
1. For the connection type, select **Redis**.
1. Fill in the host and port of your Dragonfly instance (`6379` by default).
1. Click **Test Connection** to verify, then **Establish Connection**.

The connection appears in the sidebar with type `redis`. From there you can browse keys, run commands, and view monitoring data in the browser.

## What you can do

- **Browse keys.** The key browser groups keys by their prefix (everything before the first `:`), so `user:1` and `user:2` both appear under one `user:*` entry, the same grouping it uses for Redis.
- **Run commands.** The query editor accepts plain Redis commands (`HGETALL user:1`, `SCAN 0 MATCH user:* COUNT 50`, ...) or a JSON command object, with the same right-click "Generate Command" cheatsheet the Redis provider offers.
- **Monitor the server.** The monitoring dashboard reads `INFO`, `SLOWLOG GET`, and `CLIENT LIST` for an overview, performance metrics, slow-query log, and an active-sessions table.

## Limitations

LibreDB Studio's Dragonfly support goes through its Redis driver rather than a Dragonfly-specific one, so a few panels show what Dragonfly's `INFO` and `CLIENT LIST` actually publish rather than the full picture:

- The overview's version field shows `7.4.0`, the Redis compatibility level Dragonfly's `INFO` reports under `redis_version`, not Dragonfly's own version (`dragonfly_version`, published in the same `INFO` reply under its own field).
- The connections card reads "no limit published" rather than a number, because Dragonfly's `INFO` does not publish a value under the same field name the driver reads for a connection limit.
- Every row in the active-sessions table shows `default` in the User column, whatever ACL user the connection authenticated as, because Dragonfly's `CLIENT LIST` does not publish a per-session user field.
- Every row in the active-sessions table shows `idle` in the Query column and `N` in the State column, because Dragonfly's `CLIENT LIST` does not publish a per-session command or flags field either.

None of this affects the query editor, the key browser, or running commands: those answered identically to Redis in testing against `docker.dragonflydb.io/dragonflydb/dragonfly:latest`.

## Useful Resources

- LibreDB Studio [Homepage](https://libredb.org) and [GitHub](https://github.com/libredb/libredb-studio).
- Driver: [`ioredis`](https://github.com/redis/ioredis).
