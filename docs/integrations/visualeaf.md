---
sidebar_position: 1
description: VisuaLeaf
---

# VisuaLeaf

## Introduction

[VisuaLeaf](https://visualeaf.com/) is a cross-platform desktop database client for Windows, macOS, and Linux. Alongside SQL and MongoDB databases, it connects to Redis, with a key browser and a key viewer.

Dragonfly speaks the Redis wire protocol, so VisuaLeaf connects to it the same way it connects to Redis, through its **Redis** connection type. No Dragonfly-specific configuration is needed.

## TL;DR

Start Dragonfly, add a connection of type **Redis** in VisuaLeaf pointed at Dragonfly's host and port, and browse your keys.

```sh
docker run -p 6379:6379 --ulimit memlock=-1 docker.dragonflydb.io/dragonflydb/dragonfly:latest
```

## Connecting VisuaLeaf to Dragonfly

### 1. Start Dragonfly

```sh
docker run -p 6379:6379 --ulimit memlock=-1 docker.dragonflydb.io/dragonflydb/dragonfly:latest
```

### 2. Install VisuaLeaf

Download VisuaLeaf from the [download page](https://visualeaf.com/download). A free Community Edition is available, along with paid editions.

### 3. Create a connection

1. Open VisuaLeaf and click **New Connection**.
1. Search for `redis` and select **Redis**.
1. Fill in the host (`localhost`) and port (`6379`) of your Dragonfly instance, and the password if you started Dragonfly with `--requirepass`.
1. Click **Test Connection** to verify, then **Save & Connect**.

The connection appears in the **Connections** sidebar.

## What you can do

- **Browse keys.** The key browser scans keys with `SCAN`, so it does not block Dragonfly on large keyspaces, and shows each key's type (string, hash, list, set, sorted set).
- **Inspect values.** Open a key to view its value, including the individual fields of a hash, and its TTL.
- **Switch databases.** VisuaLeaf lists Dragonfly's logical databases with their key counts.
