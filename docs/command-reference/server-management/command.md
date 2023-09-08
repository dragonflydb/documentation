---
description: Get array of Dragonfly command details
---

# COMMAND

## Syntax

    COMMAND 

**Time complexity:** O(N) where N is the total number of Dragonfly commands

**ACL categories:** @slow, @connection

Return an array with details about every Dragonfly command.

The `COMMAND` command is introspective.
Its reply describes all commands that the server can process.
Clients can call it to obtain the server's runtime capabilities during the handshake.

The reply it returns is an array with an element per command.
Each element that describes a Dragonfly command is represented as an array by itself.

The command's array consists of a fixed number of elements.
The exact number of elements in the array depends on the server's version.

1. Name
2. Arity
3. Flags
4. First key
5. Last key
6. Step

## Name

This is the command's name in lowercase.

**Note:**
Command names are case-insensitive.

## Arity

Arity is the number of arguments a command expects.
It follows a simple pattern:

* A positive integer means a fixed number of arguments.
* A negative integer means a minimal number of arguments.

Command arity _always includes_ the command's name itself (and the subcommand when applicable).

Examples:

* `GET`'s arity is _2_ since the command only accepts one argument and always has the format `GET _key_`.
* `MGET`'s arity is _-2_ since the command accepts at least one argument, but possibly multiple ones: `MGET _key1_ [key2] [key3] ...`.

## Flags

Command flags are an array. It can contain the following simple strings (status reply):

* **admin:** the command is an administrative command.
* **blocking:** the command may block the requesting client.
* **denyoom**: the command is rejected if the server's memory usage is too high (see the _maxmemory_ configuration directive).
* **fast:** the command operates in constant or log(N) time.
  This flag is used for monitoring latency with the `LATENCY` command.
* **loading:** the command is allowed while the database is loading.
* **noscript:** the command can't be called from [scripts](https://redis.io/topics/eval-intro).
* **readonly:** the command doesn't modify data.
* **write:** the command may modify data.

## First key

The position of the command's first key name argument.
For most commands, the first key's position is 1.
Position 0 is always the command name itself.

## Last key

The position of the command's last key name argument.
Commands usually accept one, two or multiple number of keys.

Commands that accept a single key have both _first key_ and _last key_ set to 1.

Commands that accept two key name arguments, e.g. `BRPOPLPUSH`, `SMOVE` and `RENAME`, have this value set to the position of their second key.

Multi-key commands that accept an arbitrary number of keys, such as `MSET`, use the value -1.

## Step

The step, or increment, between the _first key_ and the position of the next key.

Consider the following two examples:

```
1) 1) "mset"
   2) (integer) -3
   3) 1) write
      2) denyoom
   4) (integer) 1
   5) (integer) -1
   6) (integer) 2
   ...
```

```
1) 1) "mget"
   2) (integer) -2
   3) 1) readonly
      2) fast
   4) (integer) 1
   5) (integer) -1
   6) (integer) 1
   ...
```

The step count allows us to find keys' positions. 
For example `MSET`: Its syntax is `MSET _key1_ _val1_ [key2] [val2] [key3] [val3]...`, so the keys are at every other position (step value of _2_).
Unlike `MGET`, which uses a step value of _1_.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec/#arrays): a nested list of command details.

The order of commands in the array is random.

## Examples

The following is `COMMAND`'s output for the `GET` command:

```
1)  1) "get"
    2) (integer) 2
    3) 1) readonly
       2) fast
    4) (integer) 1
    5) (integer) 1
    6) (integer) 1
    7) 1) @read
       2) @string
       3) @fast
    8) (empty array)
    9) 1) 1) "flags"
          2) 1) read
          3) "begin_search"
          4) 1) "type"
             2) "index"
             3) "spec"
             4) 1) "index"
                2) (integer) 1
          5) "find_keys"
          6) 1) "type"
             2) "range"
             3) "spec"
             4) 1) "lastkey"
                2) (integer) 0
                3) "keystep"
                4) (integer) 1
                5) "limit"
                6) (integer) 0
   10) (empty array)
...
```
