---
description:  Learn how to use SPUBLISH to distribute data to all subscribers of a specific channel in your messaging system.
---
import PageTitle from '@site/src/components/PageTitle';

# SPUBLISH

<PageTitle title="SPUBLISH Command (Documentation) | Dragonfly" />

## Syntax

    SPUBLISH shard_channel message

**Time complexity:** O(N) where N is the number of clients subscribed to the receiving shard channel.

**ACL categories:** @pubsub, @fast

Posts a message to the given shard channel.

In a Dragonfly cluster, shard channels are assigned to slots with the same algorithm used to assign keys to slots. These channels remain active on a shard, even during slot migrations. After a migration is
complete, clients get redirected to thew new node that owns the moved slot to continue sending/receiving pub/sub messages.

## Return

[Integer reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#integers): the number of clients that received the message. 

## Examples

```shell
> spublish movies some_action_movie
(integer) 1
```
