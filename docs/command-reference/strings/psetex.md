---
description: Learn how to use Redis PSETEX to set key's value and expiration in milliseconds.
---

import PageTitle from '@site/src/components/PageTitle';

# PSETEX

<PageTitle title="Redis PSETEX Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `PSETEX` command is used to set a value in a key and simultaneously set an expiration time for that key in milliseconds.
This command is similar to the `SETEX` command, with the key difference being that the expiration time is specified in milliseconds instead of seconds.
Use cases include situations where precise control over key expiration is required, such as fine-grained cache management or coordination between nodes in a distributed system.

## Syntax

```shell
PSETEX key milliseconds value
```

- **Time complexity:** O(1)
- **ACL categories:** @write, @string, @slow

## Parameter Explanations

- `key`: The key where the value will be set.
- `milliseconds`: The expiration time in milliseconds.
- `value`: The string value to associate with the key.

## Return Values

The command returns `OK` if the operation is successful.

## Code Examples

### Basic Example: Set a Key with Expiration in Milliseconds

In this example, we set the key `mykey` with the value `"hello"` and an expiration time of 2000 milliseconds (2 seconds):

```shell
dragonfly> PSETEX mykey 2000 "hello"
OK
```

To verify the key expires after 2 seconds:

```shell
dragonfly> GET mykey
"hello"
# Wait for more than 2 seconds
dragonfly> GET mykey
(nil)
```

### Example with Dynamic Expiration

Setting a key with a dynamically computed expiration time (e.g., 1 minute or 60000 milliseconds):

```shell
# Set with a value and expiration time of 60,000 ms (1 minute)
dragonfly> PSETEX session:1234 60000 "session_data"
OK

# Check if the key exists immediately
dragonfly> GET session:1234
"session_data"

# After a minute, the session data will disappear
# Upon waiting, it will eventually return nil:
dragonfly> GET session:1234
(nil)
```

### Using `PSETEX` in an E-Commerce Cart System

Imagine an e-commerce system where carts expire after 10 minutes of inactivity.
You can set each user's cart data with a precise expiration time like so:

```shell
# Set cart data to expire after 10 minutes (600,000 milliseconds)
dragonfly> PSETEX cart:user123 600000 "cart_payload"
OK

# Fetching it immediately before expiration
dragonfly> GET cart:user123
"cart_payload"

# After 10 minutes, the cart data is automatically removed
dragonfly> GET cart:user123
(nil)
```

## Best Practices

- Use `PSETEX` when you need millisecond precision to expire temporary data.
  It is especially useful in distributed environments where low latency network communication requires precise control over key expiration times.
- For keys that need expiration times above a second but for which millisecond precision is not strictly necessary, consider using the `SETEX` command to keep your code simpler.

## Common Mistakes

- Providing an invalid number of milliseconds (for example, a negative or non-integer value).
  This will result in an error.
- Not considering the possible effects of network delays when setting very short expiration times.
  If you're setting an expiration time in single-digit milliseconds, network latency may cause unexpected behavior where the key expires sooner than expected.

## FAQs

### Can I modify the expiration time of an existing key?

No, `PSETEX` will overwrite any existing key and its expiration.
If you want to change the expiration time without modifying the value itself, consider using the `PEXPIRE` or `EXPIRE` commands.

### What happens if the key already exists?

When you run `PSETEX`, the value in the key is overwritten, and the expiration time is updated to the specified milliseconds.
The previous value and its expiration time (if any) are lost.

### Does an expiration of `0` milliseconds work?

No, attempting to set an expiration of `0` or a negative value results in an error.
