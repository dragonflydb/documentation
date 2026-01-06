---
description:  Learn how to use Redis COMMAND for information about all other commands.
---

import PageTitle from '@site/src/components/PageTitle';

# COMMAND

<PageTitle title="Redis COMMAND Command (Documentation) | Dragonfly" />

## Syntax

    COMMAND

**Time complexity:** O(N) where N is the total number of Dragonfly commands

**ACL categories:** @slow, @connection

Return an array with details about every Dragonfly command.

The `COMMAND` command is introspective.
Its reply describes all commands that the server can process.
Clients can call it to obtain the server's runtime capabilities during the handshake.

## Subcommands

- [`COMMAND HELP`](./command-help.md): Show usage information for supported subcommands.
- [`COMMAND COUNT`](./command-count.md): Return the total number of commands.
- [`COMMAND INFO`](./command-info.md): Return details about a specific command.

Unsupported in Dragonfly:

- `COMMAND DOCS`: Not implemented. The server returns an error.

---

## Return

[Array reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#arrays): a nested list of command details.
The order of commands in the array is random.

The reply is an array with **an element per command**.
Each element that describes a Dragonfly command is represented as a fixed-length array by itself.
The exact number of elements in the command's array depends on the server's version.

1. Name
2. Arity
3. Flags
4. First key
5. Last key
6. Step
7. ACL categories

### Name

This is the command's name. Note that command names are case-insensitive.

### Arity

Arity is the number of arguments a command expects.
It follows a simple pattern:

- A positive integer means a fixed number of arguments.
- A negative integer means a minimal number of arguments.

Command arity **always includes** the command's name itself (and the subcommand when applicable).
For example:

- `GET`'s arity is `2` since the command only accepts one argument and always has the format `GET key`.
- `MGET`'s arity is `-2` since the command accepts at least one argument but possibly multiple ones: `MGET key [key ...]`.

### Flags

Command flags are returned as an array. It can contain the following simple strings (status reply):

- `admin`: The command is an administrative command.
- `blocking`: The command may block the requesting client.
- `denyoom`: The command is rejected if the server's memory usage is too high
  (see the [`maxmemory`](../../managing-dragonfly/flags#--maxmemory) configuration directive).
- `fast`: The command operates in constant or log(N) time.
- `loading`: The command is allowed while the database is loading.
- `noscript`: The command can't be called from [scripts](https://redis.io/docs/latest/develop/interact/programmability/eval-intro/).
- `readonly`: The command doesn't modify data.
- `write`: The command may modify data.

### First key

The position of the command's first key name argument.
For most commands, the first key's position is `1`.
Position `0` is always the command name itself.

### Last key

The position of the command's last key name argument.
Commands usually accept one, two, or multiple number of keys.
- Commands that accept a single key have both the **first key** and the **last key** set to `1`.
- Commands that accept two key name arguments (e.g., `SMOVE`) have this value set to the position of their second key.
- Multi-key commands that accept an arbitrary number of keys (e.g., `MSET`) have the value `-1`.

### Step

The step, or increment, between the first key and the position of the next key.
Consider the following two examples:

```bash
dragonfly> COMMAND
# ...
1) MSET
2) (integer) -3
3) 1) write
   2) denyoom
   3) interleaved-keys
   4) custom-journal
4) (integer) 1
5) (integer) -1
6) (integer) 2
7) 1) @WRITE
   2) @STRING
   3) @SLOW
# ...
```

```bash
dragonfly> COMMAND
# ...
1) MGET
2) (integer) -2
3) 1) readonly
   2) fast
   3) idempotent
4) (integer) 1
5) (integer) -1
6) (integer) 1
7) 1) @READ
   2) @STRING
   3) @FAST
# ...
```

The step count allows us to find keys' positions.
- For example, the `MSET` command has a syntax of `MSET key1 val1 [key2] [val2] [key3] [val3]...`,
  so the keys are at every other position, which has a step value of `2`.
- For the `MGET` command with a syntax of `MGET key1 [key2] [key3]...`, it uses a step value of `1`.

### ACL categories

Command ACL categories are returned as an array.
For instance, the `MSET` command shown above is categorized as `@write`, `@string`, and `@slow` from the ACL perspective.
Learn more about [ACL rules](../acl/setuser.md) to control your data store access.

---

## Examples

The following is `COMMAND`'s output for the `GET` command:

```bash
dragonfly> COMMAND
# ...
1) GET         # Name
2) (integer) 2 # Arity
3) 1) readonly # Flags (array)
   2) fast
4) (integer) 1 # First key
5) (integer) 1 # Last key
6) (integer) 1 # Step
7) 1) @READ    # ACL categories (array)
   2) @STRING
   3) @FAST
# ...
```

## Tips

- Command names are case-insensitive.
- Hidden commands (with the `HIDDEN` flag) are not returned.
- Use [`COMMAND HELP`](./command-help.md) to discover supported subcommands.
