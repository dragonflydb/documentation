---
description: Get array of specific Redis command details, or all when no argument is given.
---

# COMMAND INFO

## Syntax

    COMMAND INFO [command-name [command-name ...]]

**Time complexity:** O(N) where N is the number of commands to look up

Returns [Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays) of details about multiple Redis commands.

Same result format as `COMMAND` except you can specify which commands
get returned.

If you request details about non-existing commands, their return
position will be nil.


## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays): nested list of command details.

## Examples

```cli
COMMAND INFO get set eval
COMMAND INFO foo evalsha config bar
```
