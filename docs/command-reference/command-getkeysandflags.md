---
description: Extract keys and access flags given a full Redis command
---

# COMMAND GETKEYSANDFLAGS

## Syntax

    COMMAND GETKEYSANDFLAGS command [arg [arg ...]]

**Time complexity:** O(N) where N is the number of arguments to the command

Returns [Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays) of keys from a full Redis command and their usage flags.

`COMMAND GETKEYSANDFLAGS` is a helper command to let you find the keys from a full Redis command together with flags indicating what each key is used for.

`COMMAND` provides information on how to find the key names of each command (see `firstkey`, [key specifications](https://redis.io/topics/key-specs#logical-operation-flags), and `movablekeys`),
but in some cases it's not possible to find keys of certain commands and then the entire command must be parsed to discover some / all key names.
You can use `COMMAND GETKEYS` or `COMMAND GETKEYSANDFLAGS` to discover key names directly from how Redis parses the commands.

Refer to [key specifications](https://redis.io/topics/key-specs#logical-operation-flags) for information about the meaning of the key flags.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays): list of keys from your command.
Each element of the array is an array containing key name in the first entry, and flags in the second.

## Examples

```cli
COMMAND GETKEYS MSET a b c d e f
COMMAND GETKEYS EVAL "not consulted" 3 key1 key2 key3 arg1 arg2 arg3 argN
COMMAND GETKEYSANDFLAGS LMOVE mylist1 mylist2 left left
```
