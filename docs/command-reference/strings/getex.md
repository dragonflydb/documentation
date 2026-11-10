---
description: Discover how to use Redis GETEX for fetching a key's value and setting its expiration.
---

import PageTitle from '@site/src/components/PageTitle';

# GETEX

<PageTitle title="Redis GETEX Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `GETEX` command is used to get the value of a key and set a new expiration time in the same operation.
This can be useful when you want to access the current value of a key but also update how long that key will live before automatically being removed from your database.

## Syntax

```shell
GETEX key [EX seconds | PX milliseconds | EXAT timestamp |PXAT milliseconds-timestamp | PERSIST]
```

- **Time complexity:** O(1)
- **ACL categories:** @write, @string, @fast

## Parameter Explanations

- `key`: The key for which the value is to be retrieved and an expiration set.
- `EX seconds`: Set the key to expire in `seconds`.
- `PX milliseconds`: Set the key to expire in `milliseconds`.
- `EXAT timestamp`: Set the key to expire at a specific UNIX timestamp (in seconds).
- `PXAT milliseconds-timestamp`: Set the key to expire at a specific UNIX timestamp (in milliseconds).
- `PERSIST`: Remove the expiration from the key, making it persistent.

## Return Values

The command returns the value of the key before the expiration is updated. Since the command is atomic, the value retrieved is unaffected by the expiration update and reflects the value of the key at the time of the `GETEX` operation.

If the key does not exist, `GETEX` returns `nil`.

## Code Examples

### Basic Example

Get the current value of a key and set a new TTL (in seconds):

```shell
dragonfly> SET mykey "hello" EX 3600
OK
dragonfly> GETEX mykey EX 1200
"hello"
```

In this example, we first set the value (`"hello"`) to the key `mykey` with a TTL of 3600 seconds (one hour).
Then, we retrieve the value with `GETEX` and update the TTL to 1200 seconds (20 minutes).

### Using Milliseconds for Expiration

Set the expiration time in milliseconds:

```shell
dragonfly> SET mykey "data"
OK
dragonfly> GETEX mykey PX 15000
"data"
```

Here, the key `mykey` has its value retrieved (`"data"`) while the expiration time is updated to 15,000 milliseconds (15 seconds).

### Setting Expiration at a Specific UNIX Timestamp

Set an expiration using a UNIX timestamp in seconds:

```shell
dragonfly> SET report "yearly"
OK
dragonfly> GETEX report EXAT 1699999999
"yearly"
```

In this case, the key `report` is set to expire at the specified UNIX timestamp (`1699999999`), while we retrieve its current value.

### Removing Expiration Using `PERSIST`

Remove the key's expiration:

```shell
dragonfly> SET session "active" EX 1800
OK
dragonfly> GETEX session PERSIST
"active"
```

Here, the key `session` had an expiration of 30 minutes, but with `GETEX ... PERSIST`, we not only retrieve the value but also make the key persistent, removing its expiration.

## Best Practices

- Use `GETEX` when you need to read a key's value and update its expiration simultaneously.
- Choose the options (`EX/PX`, or `EXAT/PXAT`) wisely based on your use case. For instance, in a user authentication system utilizing access tokens and refresh tokens, access tokens typically have a fixed, short-lived expiration time. Whereas for refresh tokens utilizing the sliding expiration strategy, we may extend the expiration each time it's used.

## Common Mistakes

- Using `GETEX` on non-existent keys will return `nil`, which could lead to confusion if your code doesn't handle missing keys appropriately.
- Misinterpreting the atomic nature of `GETEX`—the expiration is set at the same time as retrieving the value, so no race condition occurs.

## FAQs

### What happens if the key does not exist?

If the key does not exist, `GETEX` will return `nil` and no expiration will be set.

### Does `GETEX` alter the value of the key?

No, `GETEX` only retrieves the value and optionally changes the TTL.
The value stored in the key remains unchanged unless modified by other commands.

### Is `GETEX` equivalent to `GET` when no options are supplied?

Yes, when `GETEX` is used without any expiration options, it functions the same as a `GET` command, retrieving the current value without modifying the expiration time.
