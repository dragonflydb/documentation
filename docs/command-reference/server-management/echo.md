---
description: Learn how to use Redis ECHO command to display provided string.
---

import PageTitle from '@site/src/components/PageTitle';

# ECHO

<PageTitle title="Redis ECHO Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `ECHO` command in Redis is used to return the given string. It's mainly utilized for testing, debugging, or monitoring purposes to ensure that the connection to the Redis server is working correctly.

## Syntax

```cli
ECHO message
```

## Parameter Explanations

- `message`: The string you want Redis to return. It can contain any text, including spaces and special characters.

## Return Values

The command returns the same string that was sent as the `message` parameter.

Example:

```cli
dragonfly> ECHO "Hello, Redis!"
"Hello, Redis!"
```

## Code Examples

```cli
dragonfly> ECHO "Hello, World!"
"Hello, World!"
dragonfly> ECHO "Testing 123"
"Testing 123"
dragonfly> ECHO "Special characters !@#$%^&*()"
"Special characters !@#$%^&*()"
```

## Best Practices

- Use the `ECHO` command to verify that your Redis client is properly connected to the server.
- Utilize it in scripts to check connectivity before performing more complex operations.

## Common Mistakes

- Forgetting to enclose the message in quotes if it contains spaces or special characters. For example, `ECHO Hello, World!` will result in a syntax error. Instead, use `ECHO "Hello, World!"`.

## FAQs

### Can I use `ECHO` to check if the Redis server is running?

Yes, `ECHO` can be used to quickly verify the server's responsiveness by checking if it returns the expected message.

### Does `ECHO` support multiline strings?

No, `ECHO` only supports single-line strings. To handle multiline strings, consider storing them in a key using commands like `SET` and then retrieving them with `GET`.
