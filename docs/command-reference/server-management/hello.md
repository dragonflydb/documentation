---
description: Learn how to use Redis HELLO command as a handshake for the Redis protocol.
---

import PageTitle from '@site/src/components/PageTitle';

# HELLO

<PageTitle title="Redis HELLO Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `HELLO` command in Redis is used to initiate connections with specific protocol versions or to switch between different protocol versions during an active connection. It is particularly useful for clients that need to ensure they are communicating using a specific protocol version, typically RESP2 or RESP3.

## Syntax

```plaintext
HELLO [protover [AUTH username password] [SETNAME clientname]]
```

## Parameter Explanations

- `protover`: Specifies the protocol version (e.g., 2 for RESP2 or 3 for RESP3).
- `AUTH username password`: Optionally provide credentials if authentication is required. Both `username` and `password` must be supplied.
- `SETNAME clientname`: Optionally set the name of the client connection.

## Return Values

The `HELLO` command returns information about the server in a nested array format, including details such as the protocol version, server ID, and available modules.

Example outputs:

- When switching to RESP3 without authentication:
  ```plaintext
  1) "proto"
  2) (integer) 3
  3) "id"
  4) (integer) 12345
  5) "modules"
  6) (empty array)
  ```
- When switching to RESP2:
  ```plaintext
  "OK"
  ```

## Code Examples

```cli
dragonfly> HELLO 3
1) "proto"
2) (integer) 3
3) "id"
4) (integer) 12345
5) "modules"
6) (empty array)

dragonfly> HELLO 2
"OK"

dragonfly> HELLO 3 AUTH default mypassword SETNAME myclient
1) "proto"
2) (integer) 3
3) "id"
4) (integer) 12346
5) "modules"
6) (empty array)
```

## Best Practices

- Ensure you use the correct protocol version for your application's compatibility needs.
- Use the `AUTH` option securely by not hardcoding credentials in your application code.
- Set meaningful client names with `SETNAME` for easier tracking and debugging of client connections.

## Common Mistakes

- Switching protocol versions without ensuring client support can cause unexpected behavior.
- Using incorrect or outdated credentials when `AUTH` is necessary will result in authentication failure.

## FAQs

### What happens if I omit the `protover` parameter?

If `protover` is omitted, Redis responds with information about the current connection using the existing protocol.

### Can I switch from RESP3 back to RESP2?

Yes, you can switch between RESP2 and RESP3 by issuing the `HELLO` command with the desired `protover`.
