---
sidebar_position: 2
description: ClickHouse
---

# ClickHouse

## Introduction

ClickHouse® is a high-performance, column-oriented SQL database management system (DBMS) for online analytical processing (OLAP).
ClickHouse provides various means for integrating with external systems, including table engines.
Once configured using `CREATE TABLE` or `ALTER TABLE` statements with the `ENGINE` clause, table engines allow ClickHouse to query external systems.
From a user perspective, the configured integration looks like a normal table, but queries are proxied to the external system.

Redis is one of the external integrations supported by ClickHouse.
Since Dragonfly is highly compatible with Redis, ClickHouse can be used with Dragonfly with zero code changes and minimal configuration changes in your application.

## Dragonfly x ClickHouse

To utilize Dragonfly's multi-threaded capability and achieve superior performance for your application,
please follow the steps below to configure ClickHouse using Dragonfly as a table engine.

### 1. Installations

First, you can run Dragonfly with the following flags, assuming you have a local Dragonfly binary:

```bash
$> ./dragonfly --logtostderr --bind localhost --port 6379
```

Next, [install ClickHouse locally](https://clickhouse.com/docs/en/install#quick-install) and use the `clickhouse local` client application as follows:

```bash
$> ./clickhouse local
```

Note that the above installation steps might be the simplest way to get started with Dragonfly and ClickHouse locally in order to demonstrate the integration.
For production deployments, we recommend reading through the [Managing Dragonfly section](../managing-dragonfly/managing-dragonfly.md) for Dragonfly
and the [Production Deployments section](https://clickhouse.com/docs/en/install#available-installation-options) for ClickHouse.

### 2. Table Engine Configuration

Despite an easy local installation, the integration of Dragonfly with ClickHouse is seamless,
thanks to the fact that ClickHouse supports various table engines and Dragonfly is highly compatible with Redis.

Create a table in ClickHouse using the `Redis` table engine along with the `localhost:6379` address of the Dragonfly server:

```sql
-- Within the ClickHouse CLI:
CREATE TABLE dragonfly_table
(
    `key` String,
    `v1` UInt32,
    `v2` String,
    `v3` Float32
)
ENGINE = Redis('localhost:6379') PRIMARY KEY(key);
-- 'localhost:6379' is the Dragonfly server address initialized above.
```

### 3. Usage

Insert data into the table:

```sql
INSERT INTO dragonfly_table Values('1', 1, '1', 1.0), ('2', 2, '2', 2.0);
```

Query the table:

```sql
SELECT * FROM dragonfly_table WHERE key='1';
SELECT COUNT(*) FROM dragonfly_table;
```

That's it! Just that simple, you have successfully integrated ClickHouse with Dragonfly.
Next, we will explore the advantages of using Dragonfly with ClickHouse.

## Dragonfly Advantages

### High Throughput

### Emulated Cluster Mode

## Useful Resources

- ClickHouse [Homepage](https://clickhouse.com/), [GitHub](https://github.com/ClickHouse/ClickHouse), and [Documentation](https://clickhouse.com/docs/en/intro).
- Read more about ClickHouse table engine integration with Redis [here](https://clickhouse.com/docs/en/engines/table-engines/integrations/redis),
  which can be replaced with Dragonfly by changing the `host:port` server address within the `ENGINE` clause.
- Read more about how ClickHouse works with dictionaries [here](https://clickhouse.com/docs/en/sql-reference/dictionaries).
