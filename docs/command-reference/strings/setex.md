---
description: Discover how to use Redis SETEX for setting key-value pairs with an expiration time.
---

import PageTitle from '@site/src/components/PageTitle';

# SETEX

<PageTitle title="Redis SETEX Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `SETEX` command is used to set the value for a key and specify an expiration time in seconds.
It is a convenient way to atomically set the value and ensure that the key expires after a fixed duration.
This can be particularly useful for use cases like caching, session management, or any temporary data storage where a key needs to automatically expire after a specific duration.

## Syntax

```shell
SETEX key seconds value
```

- **Time complexity:** O(1)
- **ACL categories:** @write, @string, @slow

## Parameter Explanations

- `key`: The key to set the value for.
- `seconds`: The expiration time of the key, in seconds.
- `value`: The value to be stored in the specified key.

## Return Values

The command returns `OK` if the operation was successful.

## Code Examples

### Basic Example with Expiration

Set a key with a value and a 10-second expiration:

```shell
dragonfly> SETEX mykey 10 "my_value"
OK
```

After 10 seconds, the key will automatically expire, and trying to access it will return `nil`:

```shell
dragonfly> GET mykey
(nil)
```

### Example with Short Expiration

Set a key that expires in 2 seconds:

```shell
dragonfly> SETEX anotherkey 2 "temporary_data"
OK
```

If you query the key immediately, you will get the stored value:

```shell
dragonfly> GET anotherkey
"temporary_data"
```

However, after 2 seconds, the key will no longer exist:

```shell
dragonfly> GET anotherkey
(nil)
```

### Caching Example with Automatic Expiration

Let's use `SETEX` to store the result of an expensive database query, and ensure it expires after 30 seconds to keep the cache fresh:

```shell
dragonfly> SETEX cached_query_result 30 "{\"user\": \"john_doe\", \"age\": 30}"
OK
```

For the next 30 seconds, you can retrieve this cached result:

```shell
dragonfly> GET cached_query_result
"{\"user\": \"john_doe\", \"age\": 30}"
```

After 30 seconds, the key will no longer be available, and the cache will need to be refreshed:

```shell
dragonfly> GET cached_query_result
(nil)
```

## Best Practices

- Use `SETEX` for caching purposes where you want the cached data to automatically expire after a specific time.
- For short-lived session data, `SETEX` is ideal as it sets the expiration atomically without needing further commands.
- Be careful when choosing the expiration time. Too short, and the data might expire before it is useful; too long, and the data might become stale before it expires.

## Common Mistakes

- Overlooking that the expiration time is in seconds, not milliseconds.
- Using a very low expiration time (like 1 or 2 seconds) for critical data might result in expired keys before they are accessed.
- Accidentally setting the wrong expiration time can cause unexpected data availability or unintentional early expiration.

## FAQs

### What happens if the key already exists?

If the key already exists, `SETEX` will overwrite the existing value and reset the expiration time to the new value specified in the command.

### Can I use milliseconds as the expiration time?

No, `SETEX` only accepts expiration time in seconds.
For millisecond precision, use the `PSETEX` command.

### Will the value set with `SETEX` persist if the server restarts?

If persistence is configured correctly (using RDB or AOF), the value and its expiration time will be saved on disk.
However, the expiration timer resumes counting from the time of server restarts, not from the time of setting the key.
