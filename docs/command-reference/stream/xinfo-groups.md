---
description: Get info about all consumer groups in a stream
---

# XINFO GROUPS

## Syntax

	XINFO GROUPS key

**ACL categories:** @read, @stream, @slow

**XINFO GROUPS** command returns details of every consumer group
that belong to the specified stream **<key\>**.

The command returns the following details for each group:

 * **name:** The consumer group's name
 * **consumers:** The number of consumers in the group
 * **pending:** The length of the group's pending entries list (PEL),
 which are messages that were delivered but are yet to be acknowledged.
 * **last-delivered-id:** The ID of the last entry delivered to the
 group's consumers.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays):
a list of consumer groups.

## Example

```shell
dragonfly> XINFO GROUPS mystream
1) 1) "name"
   2) "mygroup"
   3) "consumers"
   4) (integer) 2
   5) "pending"
   6) (integer) 10
   7) "last-delivered-id"
   8) "1623910467320-1"
2) 1) "name"
   2) "another-group"
   3) "consumers"
   4) (integer) 1
   5) "pending"
   6) (integer) 1
   7) "last-delivered-id"
   8) "1623910847311-1"
```
