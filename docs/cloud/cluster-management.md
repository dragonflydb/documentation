---
description: "View cluster migrations and configure memory balancing and controller limits for a Dragonfly Cloud data store."
sidebar_position: 3
---

import PageTitle from '@site/src/components/PageTitle';
import CloudBadge from '@site/src/components/CloudBadge/CloudBadge';

# Managing a Dragonfly Swarm Cluster

<CloudBadge/>

<PageTitle title="Managing a Dragonfly Swarm Cluster | Dragonfly Cloud" />

The **Cluster** menu is available for [Dragonfly Swarm (multi-shard) data stores](./datastores.md#dragonfly-swarm-multi-shard).
On the **Data Stores** page, open the three-dot menu in a data store's row, then expand **Cluster**.
The menu contains **Migrations** (when enabled), **Memory Balancing**, and **Controller Limits**.
Available actions depend on your permissions and the data store's status.

## Migrations

A migration moves hash slots from one shard to another as the cluster changes its slot distribution.
Select **Cluster → Migrations** to view migrations for the data store. The drawer shows **Active** migrations by default; choose **All** to include completed and other historical migrations.

Each row shows the migration ID, source and target shards, start and finish times, and status.
Expand a row to see the slot ranges, available progress information such as keys migrated, and any reported error.
Use **Load more** if there are additional records.

If you have permission to update the data store or its nodes and active migrations exist, the drawer shows **Cancel In-Progress Migrations**.
After confirmation, this requests cancellation of **all** in-progress migrations for that data store, regardless of the selected filter.
Slot ownership is reverted to the current state of each shard, and the change is applied to the nodes asynchronously.

:::note
The **Migrations** entry appears only when the feature is enabled in the console.
:::

## Memory Balancing

Memory balancing can automatically redistribute hash slots between shards when memory usage warrants it.
Select **Cluster → Memory Balancing** to view or update the policy.

| Setting | Description |
| --- | --- |
| **Enabled** | Turn automatic memory balancing on or off. |
| **Max parallel migrations** | Maximum number of migrations the memory balancer may run at once. Allowed values: 1–32; default: 8. |
| **Min memory utilization** | Minimum utilization that at least one shard must reach before balancing is considered. Allowed values: 60–100%; default: 80%. |
| **Window** | Choose **Anytime** or **Scheduled**. For a schedule, select weekdays, a start hour in UTC, and a duration of 1–24 hours. |

Click **Update** to save the policy. The [controller migration limits](#controller-limits) also apply to migrations scheduled by the cluster controller.

## Controller Limits

Select **Cluster → Controller Limits** to view or update limits for cluster operations.

| Setting | Description |
| --- | --- |
| **Incoming parallel migrations per shard** | Maximum number of concurrent migrations into a shard. Enter a whole number of at least 1; default: 1. |
| **Outgoing parallel migrations per shard** | Maximum number of concurrent migrations out of a shard. Enter a whole number of at least 1; default: 1. |
| **Max new shards** | Maximum number of shards a single data store update can add. Enter 0 for no limit, or a positive whole number; default: 0. An update that would add more shards than this limit is rejected. |

Click **Update** to save the limits. These per-shard migration limits are separate from the memory balancer's **Max parallel migrations** setting.
