---
description: Return the latest latency samples for all events.
---

# LATENCY LATEST

## Syntax

    LATENCY LATEST 

**Time complexity:** O(1)

The `LATENCY LATEST` command reports the latest latency events logged.

Each reported event has the following fields:

* Event name.
* Unix timestamp of the latest latency spike for the event.
* Latest event latency in millisecond.
* All-time maximum latency for this event.

"All-time" means the maximum latency since the Redis instance was
started, or the time that events were reset `LATENCY RESET`.

## Examples

```
127.0.0.1:6379> debug sleep 1
OK
(1.00s)
127.0.0.1:6379> debug sleep .25
OK
127.0.0.1:6379> latency latest
1) 1) "command"
   2) (integer) 1405067976
   3) (integer) 251
   4) (integer) 1001
```

For more information refer to the [Latency Monitoring Framework page][lm].

[lm]: https://redis.io/topics/latency-monitor

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays): specifically:

The command returns an array where each element is a four elements array
representing the event's name, timestamp, latest and all-time latency measurements.
