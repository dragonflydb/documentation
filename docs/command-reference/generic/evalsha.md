---
description: "Get insights on Redis EVALSHA command for executing Lua scripts using SHA-1."
---

import PageTitle from '@site/src/components/PageTitle';

# EVALSHA

<PageTitle title="Redis EVALSHA Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `EVALSHA` command in Redis is used to evaluate a script cached on the server by its SHA1 digest. It is particularly useful for executing pre-loaded Lua scripts, enhancing performance by avoiding the need to re-send the script text over the network. Typical scenarios include performing complex transactions atomically, computation-heavy operations, or multi-key access patterns that require fine-grained control.

## Syntax

```cli
EVALSHA sha1 numkeys key [key ...] arg [arg ...]
```

## Parameter Explanations

- **sha1**: The SHA1 checksum of the script stored on the server.
- **numkeys**: Number of keys that the script will access.
- **key [key ...]**: The list of keys involved in the script execution.
- **arg [arg ...]**: Additional arguments required by the script.

## Return Values

The return type varies depending on the executed script's result:

- Integer reply for numeric results.
- Bulk string reply for single-string results.
- Array reply for multiple values.
- Error reply if the script does not exist or another error occurs.

Example outputs:

- `(integer) 42`
- `"Hello, world"`
- `1) "value1" 2) "value2"`

## Code Examples

```cli
dragonfly> SCRIPT LOAD "return redis.call('set', KEYS[1], ARGV[1])"
"e0e1f9fabfc9d4800c877a703b823ac0578ff8db"
dragonfly> EVALSHA e0e1f9fabfc9d4800c877a703b823ac0578ff8db 1 mykey myvalue
"OK"
dragonfly> GET mykey
"myvalue"

dragonfly> SCRIPT LOAD "return tonumber(redis.call('get', KEYS[1])) + tonumber(ARGV[1])"
"f0e1f9fabfc9d4800c877a703b823ac0578ff8dc"
dragonfly> SET mynumber 10
"OK"
dragonfly> EVALSHA f0e1f9fabfc9d4800c877a703b823ac0578ff8dc 1 mynumber 5
(integer) 15
dragonfly> GET mynumber
"10"
```

## Best Practices

- Always check if the script exists on the server before using `EVALSHA`. If it doesn't, use `SCRIPT LOAD` to load it first.
- Cache the SHA1 digest of your scripts in your application to avoid recomputing it frequently.
- Keep your Lua scripts concise to maintain readability and debug more efficiently.

## Common Mistakes

- Providing an incorrect number of keys (`numkeys`) can lead to unexpected behavior.
- Using strings for arithmetic operations without converting them properly inside the Lua script.

## FAQs

### What happens if the script is not found?

If the script identified by the given SHA1 digest does not exist on the server, Redis returns an error. You should handle this case gracefully by loading the script using `SCRIPT LOAD` and retrying the `EVALSHA` command.

### Can I use `EVALSHA` for all Redis commands?

No, `EVALSHA` is intended for running Lua scripts that can call Redis commands internally. It is not a direct replacement for individual Redis commands but rather a way to execute complex logic server-side.
