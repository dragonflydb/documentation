---
sidebar_position: 1
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

## Running ClickHouse with Dragonfly

To utilize Dragonfly's multi-threaded capability and achieve superior performance for your application,
please follow the steps below to configure ClickHouse using Dragonfly as a table engine.

### 1. Installations

First, you can run Dragonfly with the following flags, assuming you have a local Dragonfly binary:

```bash
$> ./dragonfly --bind localhost --port 6379
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

### 1. High Throughput

One of the major advantages of integrating Dragonfly with ClickHouse is the potential for increased throughput.
On a single AWS EC2 `c6gn.16xlarge` instance, Dragonfly is able to achieve a throughput of 4M ops/sec for `GET` and `SET` commands.
While the precise benchmarking data for the Dragonfly/ClickHouse integration is still in the works,
the underlying multi-threaded architecture and design of Dragonfly are geared towards ensuring higher throughput.
We will update this section with more details once the benchmarking data is available.

### 2. Large Datasets

As suggested by ClickHouse, when using a table engine for the key-value model, it is recommended to use point queries instead of range queries.
However, if range queries are required, ClickHouse can still utilize the `SCAN` command to fulfill them.

- Point query example -- `WHERE key = xx` or `WHERE key IN (xx, yy)`
- Range query example -- `WHERE key > xx`

Dragonfly is able to support up to 1TB on a single instance.
Redis, on the other hand, is typically constrained to handling tens of GB on an individual instance.
Further, the use of Redis Cluster, which might seem like a solution, is off the table as it doesn't support the `SCAN` command in its cluster mode.
Hence, for applications requiring expansive datasets and range queries, Dragonfly stands as the most effective and reliable choice for the key-value table engine when paired with ClickHouse.
We do understand that 1TB is probably not "big data" in modern terms, but supporting 1TB on a single instance is still an advantage and should be sufficient for many ad-hoc analytics use cases.

## Useful Resources

- ClickHouse [Homepage](https://clickhouse.com/), [GitHub](https://github.com/ClickHouse/ClickHouse), and [Documentation](https://clickhouse.com/docs/en/intro).
- Read more about ClickHouse table engine integration with Redis [here](https://clickhouse.com/docs/en/engines/table-engines/integrations/redis),
  which can be replaced with Dragonfly by changing the `host:port` server address within the `ENGINE` clause.
- Read more about how ClickHouse works with dictionaries [here](https://clickhouse.com/docs/en/sql-reference/dictionaries).
