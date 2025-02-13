---
title: Migrate
description: The following guides will help you migrate from Redis Instances to Dragonfly Cloud
sidebar_position: 0
slug: /cloud/migrate
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import Link from '@docusaurus/Link';
import MigrationOptions from './_migration_options.mdx';

# Migrate to Dragonfly Cloud

There are two main approaches to migrate your Redis data to Dragonfly Cloud:

## Quick Migration with Snapshots

The fastest way to migrate your data is by importing a Redis snapshot (RDB file). This method is:
- **Best for large datasets** - efficiently transfer terabytes of data
- **Simple process** - just upload your RDB file and restore
- **Supports all Redis data types** - complete data compatibility
- **Brief Data Loss** - data changes after the snapshot is taken will be lost

Learn how to [import your Redis snapshots](/cloud/backups#importing-redis-backups-rdb) to get started quickly.

## Zero Downtime Live Migration

With zero-downtime migrations, we ensure no data loss and downtime by using [RedisShake](https://github.com/alibaba/RedisShake) where data is streamed continuously from the source Redis to Dragonfly Cloud. Once the data is streamed, we switch the clients to point to the new Dragonfly Cloud instance and remove the source Redis instance.

This is a more complex process and requires an additional component i.e [RedisShake](https://github.com/alibaba/RedisShake) to be running.

This is also heavily dependent on the availability of `PSYNC` commands on the source instance.

:::tip Need Help?
If you have any questions or need assistance with your migration, our team is here to help! Join our [Discord community](https://discord.gg/HsPjXGVH85) for real-time support.
:::

### Configure Your Migration

First, select your target Dragonfly deployment type:

<Tabs groupId="target-deployment" className="migration-tabs">
<TabItem value="single-node" label="Single Node Dragonfly" default>

### Migrate to Single Node Dragonfly

Select your current Redis deployment type below to get started:

<Tabs groupId="source-deployment" className="source-tabs">
  <TabItem value="elasticache" label="AWS ElastiCache" default>
    <div className="migration-source-config">
      <h4>Configure ElastiCache Migration</h4>
      <p>Choose your current ElastiCache setup:</p>
      <Tabs groupId="elasticache-mode">
        <TabItem value="cluster" label="Cluster Mode">
          <MigrationOptions isCluster={true} cloudProvider="AWS ElastiCache" />
        </TabItem>
        <TabItem value="single" label="Single Node">
          <MigrationOptions isCluster={false} cloudProvider="AWS ElastiCache" />
        </TabItem>
      </Tabs>
    </div>
  </TabItem>
  
  <TabItem value="redis-cloud" label="Redis Cloud">
    <div className="migration-source-config">
      <h4>Redis Cloud Migration</h4>
      <p>We're working on detailed migration guides for Redis Cloud. In the meantime, our team can help you migrate - join our <Link to="https://discord.gg/HsPjXGVH85">Discord community</Link> for assistance.</p>
    </div>
  </TabItem>
  
  <TabItem value="azure-redis" label="Azure Redis">
    <div className="migration-source-config">
      <h4>Azure Redis Migration</h4>
      <p>We're working on detailed migration guides for Azure Redis. In the meantime, our team can help you migrate - join our <Link to="https://discord.gg/HsPjXGVH85">Discord community</Link> for assistance.</p>
    </div>
  </TabItem>

  <TabItem value="selfhosted" label="Self-hosted Redis">
    <div className="migration-source-config">
      <h4>Self-hosted Redis Migration</h4>
      <p>We're working on detailed migration guides for self-hosted Redis. In the meantime, our team can help you migrate - join our <Link to="https://discord.gg/HsPjXGVH85">Discord community</Link> for assistance.</p>
    </div>
  </TabItem>
</Tabs>

</TabItem>

<TabItem value="cluster" label="Dragonfly Cluster">
  <div className="migration-source-config">
    <h3>Migrate to Dragonfly Cluster</h3>
    <p>Cluster migration support is coming soon! Join our <Link to="https://discord.gg/HsPjXGVH85">Discord community</Link> to get notified when it's available.</p>
  </div>
</TabItem>

</Tabs>