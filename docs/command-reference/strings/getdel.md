---
description: Learn how to use Redis GETDEL to retrieve and delete a key’s value.
---

import PageTitle from '@site/src/components/PageTitle';

# GETDEL

<PageTitle title="Redis GETDEL Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `GETDEL` command is used to retrieve the value of a key and simultaneously delete that key from the database.
This atomically combines two operations — one to get the value of the key, and another to remove the key—making it more efficient than running the individual `GET` and `DEL` commands in sequence.

## Syntax

```shell
GETDEL key
```

- **Time complexity:** O(1)
- **ACL categories:** @write, @string, @fast

## Parameter Explanations

- `key`: The key of the value you want to retrieve and delete.

## Return Values

The command returns the value stored at the given key if the key exists.
If the key does not exist, `nil` is returned.
After the operation, the key is guaranteed to be deleted from the database.

## Code Examples

### Basic Example

Retrieve the value and delete the key:

```shell
dragonfly$> SET mykey "Hello, Dragonfly!"
OK

dragonfly$> GETDEL mykey
"Hello, Dragonfly!"

dragonfly$> GET mykey
(nil)
```

In this example, the value `"Hello, Dragonfly!"` is returned by `GETDEL` and the `mykey` is deleted from the database, as verified by the subsequent `GET`.

### Retrieving and Deleting a Non-Existent Key

If the key does not exist, `GETDEL` will return `nil` without throwing an error:

```shell
dragonfly$> GETDEL nonexistent_key
(nil)
```

Since `nonexistent_key` does not exist, the return is `nil`, and no other action is taken.

## Best Practices

- Use `GETDEL` when you need to retrieve and simultaneously delete a key in a single atomic operation. This can prevent race conditions that might occur if retrieving and deleting are done separately.
- Ideal for scenarios such as caching systems, where fetching and invalidating cache must happen instantly. Or something like an OTP (one-time password) feature that allows a user to verify only once—if they fail, another OTP must be resent to their email or phone after a period of time.

## Common Mistakes

- Forgetting that after calling `GETDEL`, the key will no longer exist.
  If subsequent operations depend on the key being available, you might need to handle it differently.
- Assuming `GETDEL` will work on non-string data types like hashes, lists, or sets.
  `GETDEL` only works on keys storing string values.

## FAQs

### What happens if the key does not exist?

If the key does not exist, `GETDEL` returns `nil`, and no other action is performed.

### Can `GETDEL` operate on non-string data types?

No, `GETDEL` is intended for string keys only.
If you attempt to use it on a non-string type, an error will be generated.
For retrieving and deleting non-string data types, you will need to use other Redis commands.
