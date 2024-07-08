---
description: Learn how to use Redis CLIENT GETNAME command to fetch name of current connection.
---

import PageTitle from '@site/src/components/PageTitle';

# CLIENT GETNAME

<PageTitle title="Redis CLIENT GETNAME Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`CLIENT GETNAME` is a command in Redis that retrieves the name of the current connection as set by `CLIENT SETNAME`. This can be helpful in identifying and debugging client connections in a Redis instance.

## Syntax

```cli
CLIENT GETNAME
```

## Parameter Explanations

This command does not take any parameters. It simply returns the name associated with the current connection.

## Return Values

The command returns a bulk string reply, which is the connection name. If no name has been assigned, it returns a null value.

### Examples:

- If the connection has a name:
  ```
  "my-client-name"
  ```
- If the connection has no name:
  ```
  (nil)
  ```

## Code Examples

```cli
dragonfly> CLIENT SETNAME "my-client"
OK
dragonfly> CLIENT GETNAME
"my-client"
dragonfly> CLIENT SETNAME ""
OK
dragonfly> CLIENT GETNAME
(nil)
```

## Common Mistakes

- Forgetting to set a name for the client before calling `CLIENT GETNAME` will result in a nil response.
- Assuming `CLIENT GETNAME` can retrieve names of other clients rather than the current one.

## FAQs

### What happens if multiple clients have the same name?

Redis does not enforce unique names for clients, so it's possible for multiple clients to have the same name. This might make it harder to distinguish between different clients.

### How can I change the client name after setting it once?

You can use the `CLIENT SETNAME` command again with a new name.
