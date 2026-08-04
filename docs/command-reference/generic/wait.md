---
description: "Learn how the WAIT command blocks until write commands are acknowledged by replicas."
---

import PageTitle from '@site/src/components/PageTitle';

# WAIT

<PageTitle title="WAIT Command (Documentation) | Dragonfly" />

## Syntax

    WAIT numreplicas timeout

**Time complexity:** Depends on the number of tracked replicas and shards, and on how long the command waits.

**ACL categories:** @slow, @connection

This command blocks the current client until all previous write commands are
acknowledged by at least `numreplicas` replicas, or until `timeout`
(in milliseconds) is reached.

It returns the number of replicas that acknowledged the writes. If the
requested number of replicas acknowledged before the timeout, the command
returns as soon as that happens; otherwise, it returns when the timeout
expires. In either case, the returned count may be lower than `numreplicas`.

`WAIT` can only be issued on a master instance. When called on a replica, it
returns an error.

Note that `WAIT` does not make Dragonfly a strongly consistent store: acknowledged
writes can still be lost during a failover, depending on which replica is promoted.
However, it greatly reduces the window of data loss.

## Dragonfly-specific behavior

Dragonfly's `WAIT` differs from the standard implementation in the following
ways:

- **Stronger acknowledgment guarantee.** The standard implementation only
  waits for the writes issued on the calling connection. Dragonfly waits for
  **all** writes performed on the instance up to the moment `WAIT` is called,
  from any connection. This is a strictly stronger guarantee.
- **A timeout of `0` is bounded.** In the standard implementation, a timeout
  of `0` blocks forever. In Dragonfly, it is capped at 10 minutes, after which
  the command returns the current acknowledgment count.
- **Early return on role or state changes.** `WAIT` returns the current count
  early if the instance starts shutting down or a takeover begins, and returns
  an error if the instance becomes a replica while waiting (for example, due to
  a concurrent `REPLICAOF`).
- **Fixed replica set.** The set of replicas is snapshotted when `WAIT` is
  invoked. If fewer connected replicas remain than `numreplicas` and all of
  them have already acknowledged, the command returns immediately instead of
  waiting out the timeout.

As in the standard implementation, when `WAIT` is called inside a
`MULTI`/`EXEC` transaction it does not block, and instead returns the number
of replicas that have already acknowledged all prior writes.

## Return

[Integer reply](https://valkey.io/topics/protocol/#integers): the number of
replicas that acknowledged all write commands issued before the `WAIT` call.

## Examples

```shell
dragonfly> SET foo bar
OK
dragonfly> WAIT 1 100
(integer) 1
dragonfly> WAIT 5 100
(integer) 1
```

In the example above, the instance has a single replica. The first `WAIT`
returns as soon as that replica acknowledges the write. The second call asks
for five replicas; since only one exists, it returns `1` immediately.
