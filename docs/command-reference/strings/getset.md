---
description: Learn how Redis GETSET sets a new value for a key & returns the old value.
---

import PageTitle from '@site/src/components/PageTitle';

# GETSET

<PageTitle title="Redis GETSET Explained (Better Than Official Docs)" />

## Introduction

The `GETSET` command in Redis retrieves the current value of a key and simultaneously sets it to a new value. This atomic operation is particularly useful for scenarios where you need to read and update a value in one go, ensuring consistency without race conditions.

## Syntax

```cli
GETSET key value
```

## Parameter Explanations

- **key**: The name of the key whose value you want to get and set. Must be a string.
- **value**: The new value to set for the specified key. Can be any string.

## Return Values

The `GETSET` command returns the old value stored at the key. If the key did not exist, it returns `nil`.

### Example Outputs

- If the key exists:
  ```cli
  "old_value"
  ```
- If the key does not exist:
  ```cli
  (nil)
  ```

## Code Examples

### Basic Example

Set a key-value pair and then use `GETSET` to update its value while retrieving the old value.

```cli
dragonfly> SET mykey "hello"
OK
dragonfly> GETSET mykey "world"
"hello"
dragonfly> GET mykey
"world"
```

### Caching with Expiry

Use `GETSET` to refresh a cached value only if it has expired or needs updating.

```cli
# Set key with an initial value
dragonfly> SET cache_key "initial_value"
OK

# After some time, update the value and retrieve the old one
dragonfly> GETSET cache_key "updated_value"
"initial_value"

# Confirm the new value is set
dragonfly> GET cache_key
"updated_value"
```

### Rate Limiting

Implement simple rate limiting by tracking the last access time of a user and updating it atomically.

```cli
# Simulate user accessing a resource
dragonfly> GETSET user:last_access 1627300000
(nil) # first access, no previous timestamp

# Subsequent access, updating the timestamp
dragonfly> GETSET user:last_access 1627300050
"1627300000" # previous access timestamp
```

## Best Practices

- Use `GETSET` when atomicity is crucial, as it ensures that getting and setting values happen in a single step.
- Ensure keys used with `GETSET` are correctly managed to avoid unexpected nil returns.

## Common Mistakes

- **Misunderstanding nil Returns**: If the key doesn't exist, `GETSET` will return `nil`. Make sure your application logic handles this scenario properly.
- **Non-string Values**: `GETSET` is designed for string values. Using it with non-string data types can lead to errors or unexpected behavior.

## FAQs

### Can `GETSET` be used with non-string data types?

No, `GETSET` is intended for use with string values. Using it with other data types can result in errors.

### What happens if the key does not exist?

If the key does not exist, `GETSET` will return `nil` and create the key with the new value.
