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


```bash
$> ./dragonfly --logtostderr --bind localhost --port 6379
```

```bash
$> ./clickhouse local
```

```sql
-- within the ClickHouse CLI
CREATE TABLE dragonfly_table
(
    `key` String,
    `v1` UInt32,
    `v2` String,
    `v3` Float32
)
ENGINE = Redis('localhost:6379') PRIMARY KEY(key);
```

## Dragonfly Advantages

### High Throughput

### Emulated Cluster Mode

## Useful Resources

- ClickHouse [Homepage](https://clickhouse.com/), [GitHub](https://github.com/ClickHouse/ClickHouse), and [Documentation](https://clickhouse.com/docs/en/intro).
- Read more about ClickHouse table engine integration with Redis [here](https://clickhouse.com/docs/en/engines/table-engines/integrations/redis),
  which can be replaced with Dragonfly by changing the `host:port` server address within the `ENGINE` clause.
- Read more about how ClickHouse works with dictionaries [here](https://clickhouse.com/docs/en/sql-reference/dictionaries).
