---
description: Learn how to use Redis MGET to retrieve the values of all specified keys.
---

import PageTitle from '@site/src/components/PageTitle';

# MGET

<PageTitle title="Redis MGET Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `MGET` command is used to retrieve the values of multiple keys in a single request.
It simplifies fetching values from several keys at once, making it highly efficient for batch retrieval.
If a key does not exist, `MGET` returns `nil` for that key instead of an error.

## Syntax

```shell
MGET key [key ...]
```

- **Time complexity:** O(N) where N is the number of keys to retrieve.
- **ACL categories:** @read, @string, @fast

## Parameter Explanations

- `key`: The key(s) whose values you want to retrieve.
- You can specify multiple keys, and their values will be retrieved in the order they were provided.

## Return Values

The command returns an array of values corresponding to the list of keys.
If a key does not exist, `nil` is returned for that particular key.

## Code Examples

### Basic Example: Retrieving Multiple Keys

Retrieve values from multiple keys:

```shell
dragonfly> SET key1 "value1"
OK
dragonfly> SET key2 "value2"
OK
dragonfly> SET key3 "value3"
OK
dragonfly> MGET key1 key2 key3
1) "value1"
2) "value2"
3) "value3"
```

### When Some Keys Do Not Exist

If one or more keys do not exist, `MGET` will return `nil` for the missing keys:

```shell
dragonfly> MGET key1 key_non_existent key3
1) "value1"
2) (nil)
3) "value3"
```

### Using `MGET` for Bulk Retrieval

In scenarios where you are managing session data for multiple users, you can use `MGET` to efficiently retrieve their session information in one operation:

```shell
dragonfly> SET session:user1 "data1"
OK
dragonfly> SET session:user2 "data2"
OK
dragonfly> SET session:user3 "data3"
OK
dragonfly> MGET session:user1 session:user2 session:user3
1) "data1"
2) "data2"
3) "data3"
```

### Example with Keys that Expire

If some of the keys have expired or are nearing expiration, `MGET` will still retrieve available keys but return `nil` for those that no longer exist:

```shell
dragonfly> SET key_expiring "temp_value" EX 1  # Expires in 1 second
OK
dragonfly> SET key_persistent "persistent_value"
OK
dragonfly> MGET key_expiring key_persistent
1) "temp_value"
2) "persistent_value"

# After 1 second
dragonfly> MGET key_expiring key_persistent
1) (nil)
2) "persistent_value"
```

## Best Practices

- Use `MGET` to minimize network round trips when retrieving values from multiple keys at once.
- Combine keys logically when possible to facilitate batch retrieval, which can significantly improve application performance.
- If some keys are expected to frequently expire, account for `nil` values in the application logic to avoid unnecessary errors.

## Common Mistakes

- Forgetting that `MGET` doesn't throw an error if keys don't exist, which might lead to unexpected `nil` values in the returned results.
- Assuming `MGET` will throw an exception for expired or missing keys—it silently returns `nil` for those keys instead.
- Not handling possible `nil` results when operating on keys subject to expiration.

## FAQs

### Does `MGET` return an error if one of the keys does not exist?

No, if one or more keys do not exist or have expired, `MGET` returns `nil` for those keys without throwing an error.

### Can I use `MGET` with binary data?

Yes, `MGET` works with binary strings, just as it does with normal strings.
It can retrieve any data stored in a binary-safe manner.

### Is there a limit to how many keys I can fetch using `MGET`?

There isn't a strict limit enforced by Dragonfly, Redis, or Valkey, though practical limitations such as memory or maximum payload size may apply based on available system resources.
