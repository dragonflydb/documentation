---
acl_categories:
- '@pubsub'
- '@slow'
arguments:
- multiple: true
  name: channel
  type: string
arity: -2
command_flags:
- pubsub
- noscript
- loading
- stale
complexity: O(N) where N is the number of channels to subscribe to.
description: Listen for messages published to the given channels
github_branch: main
github_path: /tmp/docs/content/commands/subscribe/index.md
github_repo: https://dragonflydb/redis-doc
group: pubsub
hidden: false
linkTitle: SUBSCRIBE
since: 2.0.0
summary: Listen for messages published to the given channels
syntax_fmt: SUBSCRIBE channel [channel ...]
syntax_str: ''
title: SUBSCRIBE
---
Subscribes the client to the specified channels.

Once the client enters the subscribed state it is not supposed to issue any
other commands, except for additional `SUBSCRIBE`, [`SSUBSCRIBE`](/commands/ssubscribe), [`PSUBSCRIBE`](/commands/psubscribe), [`UNSUBSCRIBE`](/commands/unsubscribe), [`SUNSUBSCRIBE`](/commands/sunsubscribe), 
[`PUNSUBSCRIBE`](/commands/punsubscribe), [`PING`](/commands/ping), [`RESET`](/commands/reset) and [`QUIT`](/commands/quit) commands.

## Behavior change history

*   `>= 6.2.0`: [`RESET`](/commands/reset) can be called to exit subscribed state.