---
description: Learn how to use Redis CLIENT TRACKING command to control server-assisted client side caching for the connection.
---

import PageTitle from '@site/src/components/PageTitle';

# CLIENT TRACKING

<PageTitle title="Redis CLIENT TRACKING Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `CLIENT TRACKING` command in Redis is used to enable or disable server-assisted client-side caching. This helps clients maintain coherent caches efficiently by receiving invalidation messages when keys they have cached are modified. It is typically used in scenarios where low-latency access to frequently read data is crucial, such as in web applications with real-time updates.

## Syntax

```plaintext
CLIENT TRACKING on|off [OPTIN] [OPTOUT] [BCAST] [PREFIX prefix] [REDIRECT client-id] [NOLOOP]
```

## Parameter Explanations

- **on/off**: Enables or disables the tracking mode.
- **OPTIN**: Clients need to explicitly indicate which keys they want to track using the `CLIENT CACHING yes` command.
- **OPTOUT**: Clients need to opt out from tracking certain keys.
- **BCAST**: Enables tracking for all keys automatically (broadcast mode).
- **PREFIX prefix**: Tracks keys that start with the specified prefix.
- **REDIRECT client-id**: Redirects invalidation messages to a different client.
- **NOLOOP**: Prevents the client from receiving invalidation messages caused by its own commands.

## Return Values

The command does not return any value directly but affects how clients receive cache invalidation messages. For example:

```cli
dragonfly> CLIENT TRACKING on BCAST
OK
```

## Code Examples

Enable basic client tracking:

```cli
dragonfly> CLIENT TRACKING on
OK
```

Enable client tracking with broadcast mode:

```cli
dragonfly> CLIENT TRACKING on BCAST
OK
```

Enable client tracking for keys with a specific prefix:

```cli
dragonfly> CLIENT TRACKING on PREFIX myprefix
OK
```

Redirect invalidation messages to another client:

```cli
dragonfly> CLIENT TRACKING on REDIRECT 1234
OK
```

## Best Practices

- Use `PREFIX` to limit tracking to specific sets of keys, reducing unnecessary invalidation traffic.
- Combine `NOLOOP` with `REDIRECT` to avoid redundant invalidations in complex client setups.

## Common Mistakes

- Not enabling tracking properly (`CLIENT TRACKING on`) before using advanced options like `BCAST` or `PREFIX`.
- Overlooking the use of `NOLOOP`, leading to performance issues due to self-invalidation.

## FAQs

### How do I stop tracking for a client?

Use `CLIENT TRACKING off` to disable tracking.

### Can I track multiple prefixes?

No, you can specify only one prefix per `CLIENT TRACKING` command. For multiple prefixes, consider redesigning key naming conventions.
