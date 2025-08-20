---
description:  Learn how to use Redis PUBSUB HELP to get guidance on usage details of the PUBSUB command in your Redis messaging setup.
---
import PageTitle from '@site/src/components/PageTitle';

# PUBSUB HELP

<PageTitle title="Redis PUBSUB HELP Command (Documentation) | Dragonfly" />

## Syntax

    PUBSUB HELP 

**Time complexity:** O(1)

**ACL categories:** @slow

The `PUBSUB HELP` command returns a helpful text describing the different subcommands.

## Return

[Array reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#arrays): a list of subcommands and their descriptions
