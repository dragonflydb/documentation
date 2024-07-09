---
description: "Get insights on how to use the Redis SCRIPT command for managing Lua scripts."
---

import PageTitle from '@site/src/components/PageTitle';

# SCRIPT

<PageTitle title="Redis SCRIPT Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `SCRIPT` command in Redis is used for scripting operations with Lua. It is primarily employed to load, run, and manage Lua scripts on the Redis server. Typical use cases include executing complex operations atomically or extending Redis commands with bespoke logic.

## Syntax

```plaintext
SCRIPT subcommand [arguments]
```

## Parameter Explanations

- `subcommand`: Specifies the action to be taken. Common subcommands include:
  - `LOAD`: Loads a script into the script cache without executing it.
  - `FLUSH`: Removes all the scripts from the script cache.
  - `EXISTS`: Checks if specific scripts exist in the script cache.
  - `KILL`: Terminates a currently running script.
- `arguments`: Additional arguments needed based on the subcommand used.

## Return Values

- `SCRIPT LOAD <script>`: Returns the SHA1 digest of the loaded script.
- `SCRIPT FLUSH`: Returns `OK` after clearing the script cache.
- `SCRIPT EXISTS <sha1> [sha1 ...]`: Returns an array of integers representing the existence (1) or non-existence (0) of the scripts.
- `SCRIPT KILL`: Returns `OK` if a script was terminated, or an error if no script was running.

## Code Examples

```cli
dragonfly> SCRIPT LOAD "return 'Hello, World!'"
"e0e1f9c8b8b2d3e599f1afbf22e4b7de03b5a281"
dragonfly> SCRIPT FLUSH
OK
dragonfly> SCRIPT EXISTS e0e1f9c8b8b2d3e599f1afbf22e4b7de03b5a281
(integer) 0
dragonfly> EVALSHA e0e1f9c8b8b2d3e599f1afbf22e4b7de03b5a281 0
(error) NOSCRIPT No matching script. Please use EVAL.
dragonfly> SCRIPT LOAD "return 'Hello, again!'"
"e0e1f9c8b8b2d3e599f1afbf22e4b7de03b5a282"
dragonfly> SCRIPT EXISTS e0e1f9c8b8b2d3e599f1afbf22e4b7de03b5a282
(integer) 1
```

## Best Practices

- Always use `SCRIPT LOAD` to pre-load scripts, especially if you intend to use them frequently. This reduces the overhead of sending the entire script repeatedly.
- Use `EVALSHA` instead of `EVAL` once a script is loaded, as it avoids retransmitting the script body and reduces network bandwidth usage.

## Common Mistakes

- Forgetting to handle potential script timeouts and not providing adequate fallbacks can lead to issues. Always design your scripts to be idempotent and fail-safe.
- Failing to clear the script cache (`SCRIPT FLUSH`) when scripts are no longer needed can result in memory issues on the Redis server.

## FAQs

### What happens if a script runs for too long?

Redis enforces a maximum execution time for scripts. If a script exceeds this limit, it will be terminated, and an error will be returned.

### Can I pass arguments to Lua scripts in Redis?

Yes, you can pass both keys and arguments to Lua scripts using the `EVAL` command by specifying the number of keys followed by the keys and then the arguments.
