---
acl_categories:
- '@pubsub'
- '@fast'
arguments:
- name: channel
  type: string
- name: message
  type: string
arity: 3
command_flags:
- pubsub
- loading
- stale
- fast
complexity: O(N+M) where N is the number of clients subscribed to the receiving channel
  and M is the total number of subscribed patterns (by any client).
description: Post a message to a channel
github_branch: main
github_path: /tmp/docs/content/commands/publish/index.md
github_repo: https://dragonflydb/redis-doc
group: pubsub
hidden: false
linkTitle: PUBLISH
since: 2.0.0
summary: Post a message to a channel
syntax_fmt: PUBLISH channel message
syntax_str: message
title: PUBLISH
---
Posts a message to the given channel.

In a Redis Cluster clients can publish to every node. The cluster makes sure
that published messages are forwarded as needed, so clients can subscribe to any
channel by connecting to any one of the nodes.

## Return

[Integer reply](/docs/reference/protocol-spec#resp-integers): the number of clients that received the message. Note that in a
Redis Cluster, only clients that are connected to the same node as the
publishing client are included in the count.
