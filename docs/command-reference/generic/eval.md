---
description: "Learn how to use Redis EVAL command to execute a Lua script."
---

import PageTitle from '@site/src/components/PageTitle';

# EVAL

<PageTitle title="Redis EVAL Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `EVAL` command in Redis is used to execute Lua scripts on the server side. This allows for complex operations to be performed atomically, which can enhance performance and consistency. Typical scenarios include transactions, batch operations, and custom commands that aren't natively supported by Redis.

## Syntax

```plaintext
EVAL script numkeys key [key ...] arg [arg ...]
```

## Parameter Explanations

- **script**: The Lua script to execute.
- **numkeys**: The number of keys that the script will interact with.
- **key [key ...]**: The actual keys that the script will operate on.
- **arg [arg ...]**: Additional arguments to pass to the script, accessible within Lua.

## Return Values

The return value of `EVAL` depends on what the Lua script returns:

- If the script returns a Redis data type, it's converted to its respective type (e.g., string, list, set).
- If the script returns an error, `EVAL` will propagate this error to the client.

Example outputs:

- A number: `(integer) 10`
- A string: `"Hello, World!"`
- A table: `[ "1", "2", "3" ]`

## Code Examples

```cli
dragonfly> EVAL "return redis.call('SET', KEYS[1], ARGV[1])" 1 mykey "myvalue"
"OK"

dragonfly> EVAL "return redis.call('GET', KEYS[1])" 1 mykey
"myvalue"

dragonfly> EVAL "return {ARGV[1], ARGV[2]}" 0 "arg1" "arg2"
1) "arg1"
2) "arg2"
```

## Best Practices

- Always validate and sanitize your Lua scripts to avoid security vulnerabilities.
- Minimize the complexity of Lua scripts to improve performance and maintainability.
- Use the `redis.call` function for Redis commands to ensure atomicity within scripts.

## Common Mistakes

- Not setting `numkeys` correctly, which leads to errors.
- Ignoring error handling within Lua scripts.
- Using blocking commands like `BLPOP` inside Lua scripts, which can cause performance issues.

## FAQs

### What happens if the script has an error?

If the Lua script encounters an error, the `EVAL` command will return an error message describing the issue.

### Can I use all Redis commands within a Lua script?

Most Redis commands can be used within Lua scripts through `redis.call`, but some blocking commands are not allowed.

### How do I debug a failing Lua script?

To debug, you can use `redis.log` within your Lua script to output messages to the Redis log.
