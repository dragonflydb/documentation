---
description: Learn how to use Redis COMMAND for information about all other commands.
---

import PageTitle from '@site/src/components/PageTitle';

# COMMAND

<PageTitle title="Redis COMMAND Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `COMMAND` command in Redis provides detailed information about all available Redis commands. This includes the arity (number of arguments), the command's flags, and other metadata. It is particularly useful for clients and developers who need to understand the capabilities or constraints of Redis commands programmatically.

## Syntax

```plaintext
COMMAND
COMMAND INFO [command-name ...]
COMMAND COUNT
COMMAND GETKEYS [command-and-args ...]
COMMAND GETKEYSANDFLAGS [command-and-args ...]
```

## Parameter Explanations

- **COMMAND**: Without any arguments, it returns a list with details of all Redis commands.
- **INFO [command-name ...]**: Provides detailed information about specific commands.
- **COUNT**: Returns the total number of commands in the Redis server.
- **GETKEYS [command-and-args ...]**: Extracts keys from the given command and arguments.
- **GETKEYSANDFLAGS [command-and-args ...]**: Extracts keys and their flags from the given command and arguments.

## Return Values

- **COMMAND**: Returns an array where each element is a nested array containing metadata about a command.
- **INFO [command-name ...]**: Returns an array of command details for the specified commands.
- **COUNT**: Returns an integer representing the number of commands.
- **GETKEYS [command-and-args ...]**: Returns an array of keys extracted from the command.
- **GETKEYSANDFLAGS [command-and-args ...]**: Returns an array of arrays, each containing a key and its associated flags.

## Code Examples

```cli
dragonfly> COMMAND COUNT
(integer) 178

dragonfly> COMMAND INFO SET
1) 1) "set"
   2) (integer) -3
   3) 1) write
      2) denyoom
   4) (integer) 1
   5) (integer) 1
   6) (integer) 1
   7) (integer) 1

dragonfly> COMMAND GETKEYS SET mykey myvalue
1) "mykey"

dragonfly> COMMAND GETKEYSANDFLAGS SET mykey myvalue
1) 1) "mykey"
   2) (empty array)
```

## Best Practices

- Use `COMMAND INFO` to dynamically understand the nature of specific commands, especially when building custom Redis clients.
- Utilize `COMMAND GETKEYS` to correctly identify which keys a complex command will operate on, aiding in scripting and debugging.

## Common Mistakes

- **Incorrect Arity Handling**: Failing to account for the arity of commands, which can lead to improper command usage.
- **Overlooking Command Flags**: Ignoring command flags like `write` or `denyoom` that dictate how commands behave under certain conditions.

## FAQs

### How can I find out how many commands my Redis instance supports?

You can use the `COMMAND COUNT` command to get the total number of commands supported by your Redis instance.

### Can I dynamically fetch which keys a command will affect?

Yes, you can use the `COMMAND GETKEYS` or `COMMAND GETKEYSANDFLAGS` commands to dynamically determine the keys involved in a command.
