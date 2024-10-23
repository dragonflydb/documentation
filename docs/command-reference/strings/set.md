---
description: Discover how to use Redis SET command to attach a value to a specific key in the database.
---

import PageTitle from '@site/src/components/PageTitle';

# SET

<PageTitle title="Redis SET Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `SET` command is used to set the value of a string key.
This command may also accept several options for controlling its behavior, such as setting an expiration time or only setting the value if the key doesn't already exist.
It is one of the most fundamental and frequently used commands when storing string data in key-value pairs.

## Syntax

```shell
SET key value [NX|XX] [GET] [EX seconds|PX milliseconds|EXAT timestamp|PXAT milliseconds-timestamp|KEEPTTL]
```

- **Time complexity:** O(1)
- **ACL categories:** @write, @string, @slow

## Parameter Explanations

- `key`: The key where the value will be stored.
- `value`: The value to be set for the given key.
- `NX` (optional): Only set the key if it does not already exist.
- `XX` (optional): Only set the key if it already exists.
- `GET` (optional): Return the old value stored at key before setting to the new value.
- `EX seconds` | `PX milliseconds` (optional): Set the expiration time for the key in seconds or milliseconds, respectively.
- `EXAT timestamp` | `PXAT milliseconds-timestamp` (optional): Set the expiration for the key based on absolute Unix timestamps (seconds or milliseconds).
- `KEEPTTL` (optional): Retain the existing time-to-live (TTL) of the key, resetting only its value.

## Return Values

The command returns `OK` if the operation was successful.

If a conditional option was used (e.g., `NX` or `XX`), and the condition wasn't met, the return value will be `(nil)`.

When using `GET`, the return value will be the old string stored at the key, or `nil` if no previous value existed.

## Code Examples

### Simple `SET` Example

In its simplest form, the `SET` command assigns a string value to a given key:

```shell
dragonfly> SET mykey "hello"
OK
dragonfly> GET mykey
"hello"
```

### Use with `NX` (Set if Not Exists)

This will only set the value if the key does not already exist:

```shell
dragonfly> SET mykey "hello" NX
OK
dragonfly> SET mykey "world" NX
(nil)  # The key already exists, so the second operation doesn't change the value.
dragonfly> GET mykey
"hello"
```

### Use with `XX` (Set if Exists)

Use `SET` with the `XX` option to only set the value if the key already exists:

```shell
dragonfly> SET mykey "initial"
OK
dragonfly> SET mykey "update" XX
OK
dragonfly> GET mykey
"update"
dragonfly> SET nonexistentKey "value" XX
(nil)  # Key doesn't exist, so the value is not set.
```

### Set TTL with `EX` or `PX`

This sets a value with an expiration time in seconds or milliseconds:

```shell
dragonfly> SET mykey "temporary" EX 10
OK
dragonfly> TTL mykey
(integer) 10  # Time to live in seconds
```

You can alternatively use `PX` for a more granular setting in milliseconds:

```shell
dragonfly> SET mykey "infleeting" PX 5000
OK
dragonfly> TTL mykey
(integer) 5  # Time remaining in seconds
```

### Use with `GET` (Return Previous Value)

The command returns the previous value stored at the key before updating it:

```shell
dragonfly> SET mykey "initial"
OK
dragonfly> SET mykey "updated" GET
"initial"
```

### Absolute Expiration with `EXAT` or `PXAT`

Set an expiration as a specific Unix timestamp, instead of after a relative period:

```shell
dragonfly> SET mykey "expiring_soon" EXAT 1700000000
OK
dragonfly> TTL mykey
(integer) 123456789  # TTL is based on the current time and the specified timestamp.
```

For even more precise control, you can specify the expiration in milliseconds using `PXAT`.

### Using `KEEPTTL` to Preserve Existing TTL

This will change the value of the key but retain its original expiration time:

```shell
dragonfly> SET mykey "initial" EX 10
OK
dragonfly> SET mykey "new_value" KEEPTTL
OK
dragonfly> TTL mykey
(integer) 8  # TTL remains unchanged.
```

## Best Practices

- Use `NX` or `XX` when you want to conditionally set values, such as when implementing locking or caching mechanisms.
- When setting expirations, consider if you need relative (`EX`, `PX`) or absolute (`EXAT`, `PXAT`) expiration times, based on your application's needs.
- `SET` with `GET` can be instrumental for atomic get-and-set operations without requiring an additional `GET` command.

## Common Mistakes

- Combining incompatible options, such as using both `NX` and `XX`. These conflict as they apply opposite conditions and cannot be used together.
- Assuming `GET` will return the current value of the key after the new value is set. It returns the old value, _not_ the current one.

## FAQs

### What happens if the key already exists and no options like `NX` or `XX` are used?

If `NX` or `XX` options are not provided, the `SET` command will overwrite the existing value unconditionally.

### Can I set a TTL for an existing key without changing its value?

No, the `SET` command updates both the value and TTL of the key.
To update the TTL only, you should use the `EXPIRE` command.

### What happens to keys with `NX` or `XX` if the condition isn't met?

If `NX` is used and the key exists, or if `XX` is used and the key does not exist, the `SET` command will do nothing and return `(nil)`.

### Can I set both a TTL and use `KEEPTTL` together?

No, `KEEPTTL` retains the current TTL of a key.
It is incompatible with other TTL-related options like `EX`, `PX`, `EXAT`, and `PXAT`.
