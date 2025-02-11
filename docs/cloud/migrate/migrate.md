---
title: Migrate
description: The following guides will help you migrate from Redis Instances to Dragonfly Cloud
sidebar_position: 0
slug: /cloud/migrate
---

# Migrate to Dragonfly Cloud

If you are currently using Redis (both self-hosted and managed offerings like AWS ElastiCache, Redis Cloud, etc.), you can migrate to Dragonfly Cloud with zero downtime. While loading [snapshots](/cloud/migrate/aws) to Dragonfly Cloud is
already available, its not zero downtime as there is a brief period of time where data is lost (after the snapshot is taken and before it is loaded into Dragonfly Cloud).

With Migrations, We try to achieve zero downtime and no data loss. This is done by using [RedisShake](https://github.com/alibaba/RedisShake) where data is streamed from the source Redis to Dragonfly Cloud continuously. Once the data is streamed, we switch the clients to point to the new Dragonfly Cloud instance and remove the source Redis instance.

With this, we can achieve zero downtime and no data loss.

Based on your source Redis, we have different migration strategies.

- [AWS ElastiCache](./migrate/aws-elasticache)

Feel free to reach out to us on [Discord](https://discord.gg/HsPjXGVH85) if you have any questions or need help.