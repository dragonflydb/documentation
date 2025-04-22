---
description:  Learn how to use SSUBSCRIBE to listen for new messages published on specified channels, ideal for event-driven programming paradigms.
---
import PageTitle from '@site/src/components/PageTitle';

# SSUBSCRIBE

<PageTitle title="SSUBSCRIBE Command (Documentation) | Dragonfly" />

## Syntax

    SSUBSCRIBE shard_channel [shard_channel ...]

**Time complexity:** O(N) where N is the number of channels to subscribe to.

**ACL categories:** @pubsub, @slow

In a Dragonfly cluster, shard channels are assigned to slots with the same algorithm used to assign keys to slots. These channels remain active on a shard, even during slot migrations. After a migration is
complete, subscribed clients get redirected to the new node that owns the moved slot. All the shard channels needs to belong to a single slot in a given SSUBSCRIBE call. Clients can subscribe to
channels that belong to different slots via separate calls to SSUBSCRIBE.


## Examples

```shell
ssubscribe movies
Reading messages... (press Ctrl-C to quit)
1) "ssubscribe"
2) "movies"
3) (integer) 1
1) "smessage"
2) "movies"
3) "Fly me to the moon"
```
