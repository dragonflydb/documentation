---
description: Get info about all consumers that belong to a consumer group of a stream
---

# XINFO CONSUMERS

## Syntax

	XINFO CONSUMERS key group

**ACL categories:** @read, @stream, @slow

**XINFO CONSUMERS** command returns the list of consumers that belong to the **<group\>** consumer group of the stream stored at **<key\>**.


The following information is provided for each consumer in the group:

 * **name:** The consumer group's name
 * **pending:** The number of entries in the PEL: pending messages for the consumer, which are messages that were delivered but are yet to be acknowledged
 * **idle:** the number of milliseconds that have passed since the consumer's last attempted interaction (Examples: **XREADGROUP**, **XCLAIM**, **XAUTOCLAIM**)
 * **inactive:** the number of milliseconds that have passed since the consumer's last successful interaction (Examples: **XREADGROUP** that actually read some entries into the PEL, **XCLAIM**/**XAUTOCLAIM** that actually claimed some entries)

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec/#arrays):
a list of consumers.

## Example

```shell
dragonfly> XINFO CONSUMERS mystream mygroup
1) 1) name
   2) "Alice"
   3) pending
   4) (integer) 1
   5) idle
   6) (integer) 9104628
   7) inactive
   8) (integer) 18104698
2) 1) name
   2) "Bob"
   3) pending
   4) (integer) 1
   5) idle
   6) (integer) 83841983
   7) inactive
   8) (integer) 993841998
```
