---
description: Learn how to use Redis DEBUG command for debugging tasks.
---

import PageTitle from '@site/src/components/PageTitle';

# DEBUG

<PageTitle title="Redis DEBUG Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `DEBUG` command in Redis is primarily used for debugging and development purposes. It allows developers to inspect the internal state of the database and manipulate it in ways that are generally not safe for production environments. Typical scenarios include investigating performance issues, testing failure recovery mechanisms, or diagnosing unexpected behavior.

## Syntax

```plaintext
DEBUG <subcommand> [arguments]
```

Common subcommands include:

- `OBJECT <key>`
- `SEGFAULT`
- `RELOAD [ASYNC]`
- `SET-ACTIVE-EXPIRE <yes|no>`

## Parameter Explanations

- `<subcommand>`: Specifies the action to perform. Common values are `OBJECT`, `SEGFAULT`, `RELOAD`, and `SET-ACTIVE-EXPIRE`.
- `<key>`: The key to inspect when using the `OBJECT` subcommand.
- `[ASYNC]`: Optional argument for `RELOAD` to reload asynchronously.
- `<yes|no>`: Argument for `SET-ACTIVE-EXPIRE` to enable or disable active expiration.

## Return Values

- **OBJECT**: Returns detailed information about the given key.
  - Example: `{"refcount":1,"encoding":"raw","lru":12345,"lru_seconds_idle":10}`
- **SEGFAULT**: Does not return; causes Redis to crash (for testing).
- **RELOAD**: Returns a simple string reply indicating success.
  - Example: `"OK"`
- **SET-ACTIVE-EXPIRE**: Acknowledges setting with an integer response.
  - Example: `"(integer) 1"`

## Code Examples

```cli
dragonfly> DEBUG OBJECT mykey
"{\"refcount\":1,\"encoding\":\"raw\",\"lru\":12345,\"lru_seconds_idle\":10}"

dragonfly> DEBUG SEGFAULT
(error message or server crash indication)

dragonfly> DEBUG RELOAD
"OK"

dragonfly> DEBUG RELOAD ASYNC
"OK"

dragonfly> DEBUG SET-ACTIVE-EXPIRE yes
(integer) 1

dragonfly> DEBUG SET-ACTIVE-EXPIRE no
(integer) 1
```

## Best Practices

- Use `DEBUG` commands only in development or staging environments as they can disrupt normal operations and crash the server.
- Always back up your data before performing any debug operations that could affect the data integrity.

## Common Mistakes

- Running `DEBUG SEGFAULT` on a production server, causing it to crash.
- Forgetting to revert changes made by `DEBUG SET-ACTIVE-EXPIRE`.

## FAQs

### What does `DEBUG OBJECT` do?

`DEBUG OBJECT` provides low-level information about a key's internal representation, useful for understanding how Redis manages memory and storage for that key.

### Can I use `DEBUG` commands in a production environment?

It is highly discouraged to use `DEBUG` commands in production due to their potential to disrupt service and corrupt data.
