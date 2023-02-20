---
description: Reset latency data for one or more events.
---

# LATENCY RESET

## Syntax

    LATENCY RESET [event [event ...]]

**Time complexity:** O(1)

The `LATENCY RESET` command resets the latency spikes time series of all, or only some, events.

When the command is called without arguments, it resets all the
events, discarding the currently logged latency spike events, and resetting
the maximum event time register.

It is possible to reset only specific events by providing the `event` names
as arguments.

Valid values for `event` are:
* `active-defrag-cycle`
* `aof-fsync-always`
* `aof-stat`
* `aof-rewrite-diff-write`
* `aof-rename`
* `aof-write`
* `aof-write-active-child`
* `aof-write-alone`
* `aof-write-pending-fsync`
* `command`
* `expire-cycle`
* `eviction-cycle`
* `eviction-del`
* `fast-command`
* `fork`
* `rdb-unlink-temp-file`

For more information refer to the [Latency Monitoring Framework page][lm].

[lm]: https://redis.io/topics/latency-monitor

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers): the number of event time series that were reset.
