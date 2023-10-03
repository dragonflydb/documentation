---
sidebar_position: 3
description: Feast
---

# Feast

## Introduction

Feast is a standalone, open-source feature store that stores and serves features consistently for offline training and online inference.
Feast uses online stores to serve features at low latency.
Feature values are loaded from data sources into the online store via materialization, which can be triggered using the `feast materialize` command.

Redis is one of the online stores supported by Feast.
Since Dragonfly is highly compatible with Redis, it can be used as an alternative online store for Feast with zero code changes and minimal configuration changes in your application.

## Running Feast with Dragonfly

Please follow the steps below to configure Dragonfly and utilize Feast in your application.

### 1. Prerequisites

Make sure you have Python and pip installed.
Then you can install the Feast SDK and CLI:

```bash
$> pip install feast
```

In order to use Dragonfly as the online store, you'll need to install the Redis extra for Feast:

```bash
$> pip install 'feast[redis]'
```

### 2. Feature Repository Creation

Bootstrap a new feature repository:

```bash
$> feast init feast_dragonfly
$> cd feast_dragonfly/feature_repo
```

Update `feature_repo/feature_store.yaml` with the below contents:

```yaml
project: feast_dragonfly
registry: data/registry.db
provider: local
online_store:
  type: redis
  connection_string: "localhost:6379"
```

### 3. Dragonfly Initialization

There are several options available to [get Dragonfly up and running quickly](../getting-started/getting-started.md).
Assuming you have a local Dragonfly binary, you can run Dragonfly with the following flags.
Make sure to use the same address and port as specified in the `feature_store.yaml` file above.

```bash
$> ./dragonfly --bind localhost --port 6379
```

### 4. Feast Usage

At this point, you have successfully configured Feast to use Dragonfly as the online store.
To learn more about how to actually use Feast, please refer to the [Feast quickstart guide](https://docs.feast.dev/getting-started/quickstart).

## Useful Resources

- Feast [Homepage](https://feast.dev/), [GitHub](https://github.com/feast-dev/feast), and [Documentation](https://docs.feast.dev/).
- Read more about how to configure Feast to use Dragonfly in their documentation [here](https://docs.feast.dev/reference/online-stores/dragonfly).
- Read our blog post on [Running the Feast Feature Store with Dragonfly](https://www.dragonflydb.io/blog/running-the-feast-feature-store-with-dragonfly).
