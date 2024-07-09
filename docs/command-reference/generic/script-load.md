---
description: "Learn to use the Redis SCRIPT LOAD command which loads a script into cache."
---

import PageTitle from '@site/src/components/PageTitle';

# SCRIPT LOAD

<PageTitle title="Redis SCRIPT LOAD Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `SCRIPT LOAD` command in Redis is used to load a Lua script into the script cache without executing it. This command returns a unique SHA1 hash that identifies the script. Typical use cases include preloading scripts that can be executed later using the `EVALSHA` command, which helps in optimizing performance by avoiding repeated script parsing.

## Syntax

```plaintext
SCRIPT LOAD script
```

## Parameter Explanations

- `script`: The Lua script you want to load into the Redis script cache. It must be a valid Lua script written as a string.

## Return Values

The command returns a bulk string reply which is the SHA1 hash of the loaded script.

Example:

```plaintext
"e0e1f9fabfc9d4800c877a703b823ac0578ff8db"
```

## Code Examples

```cli
dragonfly> SCRIPT LOAD "return 'Hello, Redis!'"
"6b1bf4862612e5a4e8b3e82c456ba7c7cb63161d"
dragonfly> SCRIPT LOAD "redis.call('SET', KEYS[1], ARGV[1])"
"51a115905dafe42bd0f2f8a7da767d33765b9c97"
```

## Best Practices

- Always validate your Lua scripts before loading them to avoid runtime errors.
- Store the returned SHA1 hash safely if you plan to use `EVALSHA` for execution.

## Common Mistakes

- Forgetting to store the SHA1 hash after loading the script, making it necessary to reload the script later.
- Loading scripts with syntax errors or invalid commands, leading to failure during execution.

## FAQs

### What happens if I try to load an invalid Lua script?

If the Lua script is invalid, Redis will return an error indicating the issue with the script.

### Can I load the same script multiple times?

Yes, but Redis will return the same SHA1 hash for the same script, so it is unnecessary to do so.
