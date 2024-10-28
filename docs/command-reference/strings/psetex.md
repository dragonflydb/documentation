---
description: Learn how to use Redis PSETEX to set key's value and expiration in milliseconds.
---

import PageTitle from '@site/src/components/PageTitle';

# PSETEX

<PageTitle title="Redis PSETEX Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `PSETEX` command is used to set a value in a key and simultaneously set an expiration time for that key in milliseconds.
This command is similar to the [`SETEX`](setex.md) command, with the key difference being that the expiration time is specified in milliseconds instead of seconds.
Use cases include situations where precise control over key expiration is required, such as fine-grained cache management or coordination between nodes in a distributed system.
Note that both [`SETEX`](setex.md) and [`PSETEX`](psetex.md) commands can be replaced by the [`SET`](set.md) command with the `EX` or `PX` options, respectively.

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

The command returns `OK` if the operation was successful.

## Code Examples

### Basic Example

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

### Expire for Inactivity

Imagine an e-commerce system where carts expire after 10 minutes of inactivity.
You can set each user's cart data with a precise expiration time using the `PSETEX` command.
In the meantime, if the user interacts with the cart, you can update the expiration time to prevent it from expiring.
As you can see in the example below, `PSETEX` can be replaced by the [`SET`](set.md) command with the `PX` option.

```shell
# Set cart data to expire after 10 minutes (600,000 milliseconds).
dragonfly> PSETEX cart:user123 600000 "cart_payload"
OK

# Adding an item to the cart updates the expiration time to 10 minutes from now.
dragonfly> SET cart:user123 "updated_cart_payload" PX 600000

# After 10 minutes, the cart data is automatically removed.
dragonfly> GET cart:user123
(nil)
```

## Best Practices

- Use `PSETEX` when you need millisecond precision to expire temporary data.
  It is especially useful in distributed environments where low latency network communication requires precise control over key expiration times.
- For keys that need expiration times above a second but for which millisecond precision is not strictly necessary, consider using the [`SETEX`](setex.md) command to keep your code simpler.
- Consider using the [`SET`](set.md) command with `PX` option to replace `PSETEX`.

## Common Mistakes

- Providing an invalid number of milliseconds (for example, a negative or non-integer value).
  This will result in an error.
- Not considering the possible effects of network delays when setting very short expiration times.
  If you're setting an expiration time in single-digit milliseconds, network latency may cause unexpected behavior where the key expires sooner than expected.

## FAQs

### Can I modify the expiration time of an existing key?

Yes, `PSETEX` will overwrite the existing key's value and expiration time with the new value and expiration time.
If you want to change the expiration time only, without modifying the value, consider using the [`PEXPIRE`](../generic/pexpire.md) or [`EXPIRE`](../generic/expire.md) commands.

### What happens if the key already exists?

When you run `PSETEX`, the value in the key is overwritten, and the expiration time is updated to the specified milliseconds.
The previous value and its expiration time (if any) are lost.

### Does an expiration of `0` milliseconds work?

No, attempting to set an expiration of `0` or a negative value results in an error.
