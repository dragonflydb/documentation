---
description: Get array of specific Redis command documentation
---

# COMMAND DOCS

## Syntax

    COMMAND DOCS [command-name [command-name ...]]

**Time complexity:** O(N) where N is the number of commands to look up

Return documentary information about commands.

By default, the reply includes all of the server's commands.
You can use the optional _command-name_ argument to specify the names of one or more commands.

The reply includes a map for each returned command.
The following keys may be included in the mapped reply:

* **summary:** short command description.
* **since:** the Redis version that added the command (or for module commands, the module version).
* **group:** the functional group to which the command belongs.
  Possible values are:
  - _bitmap_
  - _cluster_
  - _connection_
  - _generic_
  - _geo_
  - _hash_
  - _hyperloglog_
  - _list_
  - _module_
  - _pubsub_
  - _scripting_
  - _sentinel_
  - _server_
  - _set_
  - _sorted-set_
  - _stream_
  - _string_
  - _transactions_
* **complexity:** a short explanation about the command's time complexity.
* **doc_flags:** an array of documentation flags.
  Possible values are:
  - _deprecated:_ the command is deprecated.
  - _syscmd:_ a system command that isn't meant to be called by users.
* **deprecated_since:** the Redis version that deprecated the command (or for module commands, the module version)..
* **replaced_by:** the alternative for a deprecated command.
* **history:** an array of historical notes describing changes to the command's behavior or arguments.
  Each entry is an array itself, made up of two elements:
  1. The Redis version that the entry applies to.
  2. The description of the change.
* **arguments:** an array of maps that describe the command's arguments.
  Please refer to the [Redis command arguments][td] page for more information.

[td]: https://redis.io/topics/command-arguments

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays): a map as a flattened array as described above.

## Examples

```shell
dragonfly> COMMAND DOCS SET
1) "set"
2) 1) "summary"
2) "Set the string value of a key"
3) "since"
4) "1.0.0"
5) "group"
6) "string"
7) "complexity"
8) "O(1)"
9) "history"
10) 1) 1) "2.6.12"
2) "Added the `EX`, `PX`, `NX` and `XX` options."
2) 1) "6.0.0"
2) "Added the `KEEPTTL` option."
3) 1) "6.2.0"
2) "Added the `GET`, `EXAT` and `PXAT` option."
4) 1) "7.0.0"
2) "Allowed the `NX` and `GET` options to be used together."
11) "arguments"
12) 1) 1) "name"
2) "key"
3) "type"
4) "key"
5) "key_spec_index"
6) (integer) 0
2) 1) "name"
2) "value"
3) "type"
4) "string"
3) 1) "name"
2) "condition"
3) "type"
4) "oneof"
5) "since"
6) "2.6.12"
7) "flags"
8) 1) "optional"
9) "arguments"
10) 1) 1) "name"
2) "nx"
3) "type"
4) "pure-token"
5) "token"
6) "NX"
2) 1) "name"
2) "xx"
3) "type"
4) "pure-token"
5) "token"
6) "XX"
4) 1) "name"
2) "get"
3) "type"
4) "pure-token"
5) "token"
6) "GET"
7) "since"
8) "6.2.0"
9) "flags"
10) 1) "optional"
5) 1) "name"
2) "expiration"
3) "type"
4) "oneof"
5) "flags"
6) 1) "optional"
7) "arguments"
8) 1) 1) "name"
2) "seconds"
3) "type"
4) "integer"
5) "token"
6) "EX"
7) "since"
8) "2.6.12"
2) 1) "name"
2) "milliseconds"
3) "type"
4) "integer"
5) "token"
6) "PX"
7) "since"
8) "2.6.12"
3) 1) "name"
2) "unix-time-seconds"
3) "type"
4) "unix-time"
5) "token"
6) "EXAT"
7) "since"
8) "6.2.0"
4) 1) "name"
2) "unix-time-milliseconds"
3) "type"
4) "unix-time"
5) "token"
6) "PXAT"
7) "since"
8) "6.2.0"
5) 1) "name"
2) "keepttl"
3) "type"
4) "pure-token"
5) "token"
6) "KEEPTTL"
7) "since"
8) "6.0.0"
```
