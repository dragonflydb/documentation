---
description: Learn how to use Redis PSETEX to set key's value and expiration in milliseconds.
---

import PageTitle from '@site/src/components/PageTitle';

# PSETEX

<PageTitle title="Redis PSETEX Explained (Better Than Official Docs)" />

## Introduction

The `PSETEX` command in Redis sets a key to hold a string value and sets the key to expire after a specified number of milliseconds. It's an atomic operation that combines setting the value and setting the expiration time, ensuring consistency and reliability for time-sensitive data.

## Syntax

```plaintext
PSETEX key milliseconds value
```

## Parameter Explanations

- **key**: The name of the key. This is a string.
- **milliseconds**: The expiration time in milliseconds. Must be a positive integer.
- **value**: The value to be set at the key. Can be any valid string.

## Return Values

- **OK**: If the command successfully sets the key and its expiration.

## Code Examples

### Basic Example

Set a key with a value and an expiration time of 2000 milliseconds (2 seconds).

```cli
dragonfly> PSETEX mykey 2000 "Hello"
"OK"
dragonfly> GET mykey
"Hello"
```

(After 2 seconds)

```cli
dragonfly> GET mykey
(nil)
```

### Session Management

Using `PSETEX` to manage user sessions with a timeout of 30 minutes (1800000 milliseconds).

```cli
dragonfly> PSETEX session:12345 1800000 "user_data"
"OK"
```

To retrieve the session data before it expires:

```cli
dragonfly> GET session:12345
"user_data"
```

### Temporary Caching

Implementing temporary caching for a frequently accessed but non-critical piece of data, such as user search results, with a 5-minute expiration.

```cli
dragonfly> PSETEX search_results:user42 300000 "search results data"
"OK"
```

Fetching the cached search results:

```cli
dragonfly> GET search_results:user42
"search results data"
```

## Best Practices

- Use `PSETEX` when you need to ensure both setting a value and its expiration atomically, avoiding race conditions.
- Choose appropriate expiration times based on the use case to prevent unnecessary memory usage due to forgotten keys.

## Common Mistakes

- Providing a negative or zero value for milliseconds, which will result in an error.
- Forgetting that the key will expire and assuming it will be available indefinitely, leading to potential issues in your application logic.

## FAQs

### What happens if I set a very large expiration time?

Redis supports very large expiration times, but setting unnecessarily large values can result in keys lingering longer than intended, consuming memory.

### Can I update the value without resetting the expiration?

No, `PSETEX` sets both the value and expiration together. Use `SETEX` or separate `SET` and `PEXPIRE` commands to handle these operations separately.
