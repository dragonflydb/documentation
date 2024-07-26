---
description: Discover how to use Redis SETEX for setting key-value pairs with an expiration time.
---

import PageTitle from '@site/src/components/PageTitle';

# SETEX

<PageTitle title="Redis SETEX Explained (Better Than Official Docs)" />

## Introduction

The `SETEX` command in Redis is used to set a key with a specific value and an expiration time, measured in seconds. It combines the functionality of `SET` and `EXPIRE`, making it useful for caching scenarios where you want data to expire automatically after a certain period.

## Syntax

```cli
SETEX key seconds value
```

## Parameter Explanations

- **key**: The name of the key where the value should be stored.
- **seconds**: The lifetime of the key, specified in seconds. After this time, the key will be automatically deleted.
- **value**: The value to be stored at the given key.

## Return Values

- **OK**: If the operation is successful.

Example:

```cli
dragonfly> SETEX mykey 10 "myvalue"
"OK"
```

## Code Examples

### Basic Example

Setting a key with a value that expires in 10 seconds.

```cli
dragonfly> SETEX mykey 10 "Hello, World!"
"OK"
dragonfly> GET mykey
"Hello, World!"
// Wait for 10 seconds
dragonfly> GET mykey
(nil)
```

### Caching API Token

Using `SETEX` to cache an API token that expires in 3600 seconds (1 hour).

```cli
dragonfly> SETEX api_token 3600 "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
"OK"
dragonfly> GET api_token
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
// After 1 hour
dragonfly> GET api_token
(nil)
```

### Temporary User Session

Storing temporary user session data that should last for 30 minutes.

```cli
dragonfly> SETEX user_session:12345 1800 "{\"username\": \"johndoe\", \"role\": \"admin\"}"
"OK"
dragonfly> GET user_session:12345
"{\"username\": \"johndoe\", \"role\": \"admin\"}"
// After 30 minutes
dragonfly> GET user_session:12345
(nil)
```

## Best Practices

- **Use Meaningful Key Names**: Include context in your key names (e.g., `user_session:12345`) to avoid conflicts and make keys easily identifiable.
- **Appropriate Expiration Times**: Set expiration times based on the use case to balance between memory usage and data freshness.

## Common Mistakes

- **Incorrect Expiration Time Units**: Ensure the time is in seconds. Using milliseconds or other units will not work as expected.
- **Overwriting Existing Keys Without Notice**: Be cautious as `SETEX` will overwrite existing keys without warning.

## FAQs

### What happens if I use `SETEX` on an existing key?

`SETEX` will overwrite the existing key's value and reset its expiration time.

### Can I use `SETEX` to store complex data structures?

Yes, but remember that the value must be serialized into a string format (e.g., JSON) before storing.
