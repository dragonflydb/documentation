---
description: Learn how to use Redis MGET to retrieve the values of all specified keys.
---

import PageTitle from '@site/src/components/PageTitle';

# MGET

<PageTitle title="Redis MGET Explained (Better Than Official Docs)" />

## Introduction

The `MGET` command in Redis is used to retrieve the values of multiple keys in a single call. This is efficient for fetching data as it minimizes the number of round trips between the client and server. It’s essential when dealing with scenarios where you require the values of several keys simultaneously, such as caching or bulk reads.

## Syntax

```plaintext
MGET key [key ...]
```

## Parameter Explanations

- `key`: The key for which the value needs to be retrieved. Multiple keys can be specified, separated by spaces.

## Return Values

The command returns an array of values corresponding to the specified keys.

#### Example Outputs

- If all keys exist: An array of values.
- If some keys do not exist: An array containing `nil` at the positions of the nonexistent keys.

## Code Examples

### Basic Example

Fetching values of multiple keys:

```cli
dragonfly> SET key1 "value1"
OK
dragonfly> SET key2 "value2"
OK
dragonfly> MGET key1 key2 key3
1) "value1"
2) "value2"
3) (nil)
```

### Caching User Profiles

Retrieve user profile data stored in multiple keys:

```cli
dragonfly> MGET user:1000:name user:1000:email user:1000:age
1) "Alice"
2) "alice@example.com"
3) "30"
```

### Fetching Configuration Settings

Retrieve application configuration settings stored in separate keys:

```cli
dragonfly> MGET config:timeout config:max_connections config:debug_mode
1) "300"
2) "100"
3) "true"
```

### Task Management

Retrieve status information for multiple tasks:

```cli
dragonfly> MGET task:1:status task:2:status task:3:status
1) "completed"
2) "in-progress"
3) (nil)
```

## Best Practices

- Use `MGET` to reduce the number of round trips to the Redis server when you need multiple values.
- Ensure that the keys requested in `MGET` are related and often needed together to maximize efficiency.

## Common Mistakes

- Requesting a large number of keys without considering the network overhead and latency.
- Assuming that all keys will exist; always handle `nil` values in your application logic.

## FAQs

### What happens if a key does not exist?

If a key does not exist, `MGET` returns `nil` for that particular key.

### Is `MGET` atomic?

No, `MGET` itself is not atomic. However, Redis guarantees that the command will fetch all specified keys consistently within the same logical operation.
