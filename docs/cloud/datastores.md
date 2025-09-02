---
sidebar_position: 2
---

import PageTitle from '@site/src/components/PageTitle';
import CloudBadge from'@site/src/components/CloudBadge/CloudBadge'

# Data Stores

<CloudBadge/>

<PageTitle title="Data Stores | Dragonfly Cloud" />

## Overview

A [Dragonfly Cloud](https://dragonflydb.cloud/) data store represents an endpoint for storing and retrieving in-memory
data, which is compatible with Redis (RESP2 and RESP3) and Memcached protocols. The endpoint is a fully managed
service that is backed by one or more [Dragonfly](https://github.com/dragonflydb/dragonfly) server instances.
The data store can be accessed from the public internet or over a private network.

On this page, you will find information on how to create, configure, and connect to a Dragonfly Cloud data store.

## Creating a Data Store

- To create a data store, on the **Data Stores** tab,
  click the [+Data Store](https://dragonflydb.cloud/datastores/new) button.
- The minimum configuration consists of **Name**, **Cloud Provider**, **Cloud Region**, **Memory Size**, and **Compute Tier**.
- The following cloud providers are supported:
    - Amazon Web Services (AWS)
    - Google Cloud Platform (GCP)
    - Microsoft Azure
- **Cluster Mode**
    - **Emulated Single-Shard**:
      When this mode is selected, Dragonfly Cloud provisions and manages
      a single-shard (standalone) vertically scalable data store.
    - **Dragonfly Swarm Multi-Shard**:
      When this mode is selected, Dragonfly Cloud provisions and manages
      a multi-shard distributed data store, which is both vertically and horizontally scalable.
    - For more details, please refer to the [cluster mode](#cluster-mode) section.
- **Memory Size** and **Compute Tier** specify the provisioned memory size and the CPU-to-memory ratio for the data store.
  Available tiers are:
    - **Standard**: This tier is suitable for moderate to high workloads.
      It provides a balanced CPU-to-memory ratio.
    - **Enhanced**: This tier is suitable for workloads that require more compute resources.
      It provides **2x the CPU** for the same amount of provisioned memory compared to the **Standard** tier.
    - **Extreme**: This tier is suitable for workloads that require extremely high compute resources.
      It provides **4x the CPU** for the same amount of provisioned memory compared to the **Standard** tier.
- For network bandwidth limits, please refer to the [network bandwidth](./bandwidth.md) section.
- **Note** -> **Cloud Provider** and **Cloud Region** can **NOT** be modified once the data store is created.
- **Note** -> **Cluster Mode** can **NOT** be modified once the data store is created.
- **You can modify the data store memory size and compute tier later with zero downtime to easily scale up or down.**

### Advanced Configurations

- By default, the data store will be configured with a **public endpoint**, **TLS**, and an auto-generated **passkey**,
  meaning you can securely connect to it from anywhere over the public internet.
- To create a data store with a **private endpoint**, see [security](#security), [networks](./networks.md),
  and [peering connections](./connections.md).
- By default, the data store will consist of a single Dragonfly server instance.
  To create a highly available data store, read more about [high availability](#high-availability) below.
  

### Connection Details & Data Store Status

- Once the data store is created, clicking the data store row will open a drawer with the data store configuration,
  including the auto-generated passkey and a Redis-compatible **Connection URI**.
- Once the data store's **Status** becomes **Active**, you can try accessing it with Redis CLI,
  for instance, `redis-cli -u <CONNECTION_URI> PING`.
  Read more information on [how to connect to the data store](./connect/redis-clients.md) below.

### Updating the Data Store Configuration

- To update the data store configuration, click the three-dot
  menu (<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e8eaed"><path d="M480-160q-33 0-56.5-23.5T400-240q0-33 23.5-56.5T480-320q33 0 56.5 23.5T560-240q0 33-23.5 56.5T480-160Zm0-240q-33 0-56.5-23.5T400-480q0-33 23.5-56.5T480-560q33 0 56.5 23.5T560-480q0 33-23.5 56.5T480-400Zm0-240q-33 0-56.5-23.5T400-720q0-33 23.5-56.5T480-800q33 0 56.5 23.5T560-720q0 33-23.5 56.5T480-640Z"/></svg>)
  in the data store row and then select **Edit**.
- **Dragonfly Cloud performs data store updates with zero downtime**.

---

## Cluster Mode

Dragonfly Cloud offers the following cluster modes to satisfy your scaling needs.

### Emulated (Single-Shard)

A single-shard Dragonfly data store is capable of handling significantly large in-memory data sizes and high
QPS (queries per second) normally comparable to what a Redis Cluster typically supports.
This mode simplifies the migration process from either a Redis standalone instance or a Redis Cluster to a
single-shard Dragonfly data store, which can scale vertically.
Some key points to keep in mind when you choose a single-shard Dragonfly data store:

- Regular standalone Redis client libraries can be used.
- Redis Cluster client libraries can be used.
- Single-shard data stores scale vertically—up to 600GB of in-memory data with millions of QPS.

### Dragonfly Swarm (Multi-Shard)

Dragonfly Swarm is the managed version of [Dragonfly Cluster](../managing-dragonfly/cluster-mode.md#multi-shard-cluster).
It is designed to scale both vertically and horizontally, offering **practically unlimited capacity**.
Dragonfly Swarm automatically configures the optimal number of shards based on the amount of memory you provision.
To interact with a Dragonfly Swarm data store, client libraries you use must support the Redis Cluster protocol.
Some key points to keep in mind when you choose a Dragonfly Swarm data store:

- Only Redis Cluster client libraries can be used. See [connecting with Redis clients](./connect/redis-clients.md) for more details.
- You can also add replica(s) for primary nodes within a Dragonfly Swarm cluster. By doing so, each shard becomes highly available.
  In the meantime, you can leverage these replicas to scale read traffic even further. **Read replicas** are enabled for
  Dragonfly Swarm clusters by default. Learn how to [configure your clients here](./connect/redis-clients.md).
- Multi-shard data stores scale both vertically and horizontally—up to 15TB of in-memory data with tens of millions of QPS.
- If your workload requires more than 15TB of memory, please contact support.

## Security

Dragonfly Cloud supports using both public and private endpoints for data access.

### Public Endpoint

- With a public endpoint, you can connect to the data store from anywhere over the internet.
- To protect your data store from unauthorized access,
  public endpoints are default with **TLS** and **passkey** enabled.
- **TLS** has some performance impact, so it can be disabled. **But it is highly recommended to leave it enabled**.
- **Passkey** is mandatory and cannot be disabled for public endpoints.

### Private Endpoint

- Private endpoints provide **better security**, **better performance**, and **lower latency** as the data transports
  to and from the data stores over private networks and not via the public internet.
- Using a private endpoint also **reduces data transfer costs** applied by the cloud provider.
- In order to create a data store with a private endpoint, **you must first create a [private network](./networks.md)**.
- Once you have created a private network, you can select it in the **Endpoint** dropdown
  when creating a new data store.
- **TLS** and **passkey** are disabled by default for data stores with private endpoints but can be enabled.

**Tip:** In order to completely avoid data transfer charges, place your data store in the same availability zone (AZ)
as your application. See [high availability](#high-availability) for specifying the data store availability zone.

## Durability & High Availability

### Eviction Policy

Eviction policy controls the behavior of a data store when it reaches its memory limit.

- **No Eviction:** items are never evicted, and out-of-memory errors are returned to the client
  when the data store is full.
- **Cache:** The data store behaves as a cache and automatically evicts items to free space for new writes
  when the data store is full. Dragonfly has only one cache eviction policy, which you can read more about
  [here](https://www.dragonflydb.io/blog/dragonfly-cache-design).

To choose the eviction policy, expand the **Durability & High Availability** section and select the desired policy.
Make sure to save the changes by creating a new data store or updating an existing one.

### High Availability

By default, the data store will consist of a single Dragonfly server. This means that in case of software failures,
hardware failures, or cloud zone outages, the data would be lost, and the data store could be completely unavailable.

To increase the availability of your data store, you can configure it to be deployed in up to three different zones:
**one primary/master zone and up to two replica zones**. Dragonfly Cloud automatically detects failures
and performs failover to an available replica when the primary is unavailable.
To add one or more replicas to your data store:

- Expand the **Durability & High Availability** section.
- Click on the **+Add Replica** button and select the zone for the replica.
- You can select the same zone as the primary or a different zone.
- When selecting a different zone, inter-zone data transfer costs may apply.
- **You can update the number of replicas of a data store with zero downtime**.
- **You can update the primary/replica zones of a data store with zero downtime**.

**Tip:** You can select a zone for the data store primary instance, and you should
select the same zone as your application to avoid data transfer costs.

## Specializations

Dragonfly is designed from the ground up to provide a seamless, highly efficient, and blazingly fast alternative to
Redis. Our mission is to enhance the performance of projects that rely on in-memory data stores without having to
compromise on reliability or ease of use. Being a drop-in replacement for Redis, Dragonfly can be integrated into any
project that utilizes Redis as its backend in-memory store. Dragonfly Cloud pushes this further by automatically
providing the most suitable server configuration(s) for your workload when you select a specialization.

- **BullMQ:** Enable this for running [BullMQ](https://bullmq.io/) workloads.
  This requires you to apply the hashtag syntax to the queue names as described [here](/docs/integrations/bullmq.md).
  If that is not possible for your application, please contact support.
- **Memcached:** Enable this for running Memcached workloads. Memcached protocol will be enabled on port `6371`.
  Note that authentication is not supported for Memcached, so it can only be enabled for data stores
  with a [private endpoint](#private-endpoint).
- **Sidekiq:** Enable this for running [Sidekiq](https://sidekiq.org/) workloads,
  [read more](/docs/integrations/sidekiq.md).

---

## Connecting to a Data Store

After the data store's **Status** changes to **Active**, it is ready for
connection. For detailed instructions on connecting, see [connecting with Redis clients](./connect/redis-clients.md).

## ACL Rules

You can leverage [Dragonfly's built-in support for ACLs](https://www.dragonflydb.io/docs/category/acl) to control access
to your data stores within Dragonfly Cloud. Each Dragonfly Cloud data store is created with a default ACL rule
that allows all commands for the `default` user:

```text
USER default ON >pmn4p0ssrbbl ~* +@ALL
```

- To modify the data store ACL rules, click the data store three-dot
  menu (<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e8eaed"><path d="M480-160q-33 0-56.5-23.5T400-240q0-33 23.5-56.5T480-320q33 0 56.5 23.5T560-240q0 33-23.5 56.5T480-160Zm0-240q-33 0-56.5-23.5T400-480q0-33 23.5-56.5T480-560q33 0 56.5 23.5T560-480q0 33-23.5 56.5T480-400Zm0-240q-33 0-56.5-23.5T400-720q0-33 23.5-56.5T480-800q33 0 56.5 23.5T560-720q0 33-23.5 56.5T480-640Z"/></svg>)
  and click **ACL Rules**.
- An editor drawer for ACL rules will open where you can add, modify, or delete ACL rules.
- ***CAUTION: Altering ACL rules can potentially disrupt access for current users. It is always recommended to test ACL
  rules on a test data store before applying them to a production data store.***

### Rotating Data Store Passkey

Here is a recipe to rotate the passkey for a data store, since it is part of the ACL rules:

- Modify the default ACL rule to something like: `USER default ON >myoldpass >mynewpass ~* +@ALL`.
- Verify you can now authenticate with both the old and new passkeys.
- Migrate all consumers to authenticate with the new passkey.
- Modify the default ACL rule to only include the new passkey: `USER default ON >mynewpass ~* +@ALL`.
- Verify you can no longer authenticate with the old passkey.
- ***CAUTION: Altering ACL rules can potentially disrupt access for current users. It is always recommended to test ACL
  rules on a test data store before applying them to a production data store.***

## Pricing & Support

- See more information about Dragonfly Cloud pricing [here](./pricing.md).
- See more information about Dragonfly Cloud support plans [here](./support.md).
