---
description:  Discover how to use Redis GETEX for fetching a key's value and setting its expiration.
---

import PageTitle from '@site/src/components/PageTitle';

# GETEX

<PageTitle title="Redis GETEX Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `GETEX` command is used to get the value of a key and set a new expiration time in the same operation.
This can be useful when you want to access the current value of a key but also update how long that key will live before automatically being removed from your database.

## Syntax

```shell
GETEX key [EX seconds|PX milliseconds|EXAT timestamp|PXAT milliseconds-timestamp|PERSIST]
```

## Parameter Explanations

- `key`: The key for which the value is to be retrieved and an expiration set.
- `EX seconds`: Set the key to expire in `seconds`.
- `PX milliseconds`: Set the key to expire in `milliseconds`.
- `EXAT timestamp`: Set the key to expire at a specific UNIX timestamp (in seconds).
- `PXAT milliseconds-timestamp`: Set the key to expire at a specific UNIX timestamp (in milliseconds).
- `PERSIST`: Remove the expiration from the key, making it persistent.

## Return Values

The command returns the current value of the key being requested before the expiration is updated.

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

In this example, we first set the value (`"hello"`) to the key `mykey` with a TTL of one hour (3600 seconds).
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
- To optimize storage cleanup, prefer the use of UNIX timestamp options (`EXAT` or `PXAT`) for setting expiration when a precise expiration is required.
  
## Common Mistakes

- Using `GETEX` on non-existent keys will return `nil`, potentially causing confusion if you're not accounting for the absence of the key.
- Misunderstanding expiration is set *before* the value is returned; the expiration might cause a race condition if another command modifies the key before the TTL updates.

## FAQs

### What happens if the key does not exist?

If the key does not exist, `GETEX` will return `nil` and no expiration will be set.

### Does `GETEX` alter the value of the key?

No, `GETEX` only retrieves the value and optionally changes the TTL.
The value stored in the key remains unchanged unless modified by other commands.