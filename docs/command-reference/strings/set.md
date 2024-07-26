---
description: Discover how to use Redis SET command to attach a value to a specific key in the database.
---

import PageTitle from '@site/src/components/PageTitle';

# SET

<PageTitle title="Redis SET Explained (Better Than Official Docs)" />

## Introduction

The `SET` command is one of the most fundamental commands in Redis, used to set the value of a key. If the key already holds a value, it is overwritten. The `SET` command also supports various options for setting expiration and conditional operations, making it versatile for a range of use cases.

## Syntax

```plaintext
SET key value [NX|XX] [EX seconds|PX milliseconds|EXAT timestamp|PXAT timestampms|KEEPTTL] [GET]
```

## Parameter Explanations

- **key**: The name of the key to set.
- **value**: The string value to set.
- **NX**: Only set the key if it does not already exist.
- **XX**: Only set the key if it already exists.
- **EX seconds**: Set the specified expire time, in seconds.
- **PX milliseconds**: Set the specified expire time, in milliseconds.
- **EXAT timestamp**: Set the specified Unix time at which the key will expire, in seconds.
- **PXAT timestampms**: Set the specified Unix time at which the key will expire, in milliseconds.
- **KEEPTTL**: Retain the existing TTL (time to live) of the key.
- **GET**: Return the old value stored at key, or nil when key did not exist.

## Return Values

- **OK**: Returns "OK" if `SET` was successful.
- **nil**: Returns nil if the operation was not performed due to NX/XX conditions.

### Examples:

- Successful `SET`:

  ```cli
  dragonfly> SET mykey "Hello"
  OK
  ```

- Conditional `SET` with NX:
  ```cli
  dragonfly> SET mykey "World" NX
  (nil)
  ```

## Code Examples

### Basic Example

Set a simple key-value pair.

```cli
dragonfly> SET mykey "Hello"
OK
dragonfly> GET mykey
"Hello"
```

### Using NX Option

Set a key only if it does not already exist.

```cli
dragonfly> SET newkey "New Value" NX
OK
dragonfly> SET newkey "Another Value" NX
(nil)
```

### Using EX Option

Set a key with an expiry of 10 seconds.

```cli
dragonfly> SET tempkey "Temporary" EX 10
OK
dragonfly> TTL tempkey
(integer) 10
```

### Using GET Option

Get the old value while setting a new one.

```cli
dragonfly> SET mykey "Hello"
OK
dragonfly> SET mykey "World" GET
"Hello"
dragonfly> GET mykey
"World"
```

### Cache Implementation

Using `SET` with EX to implement a cache that expires after 30 seconds.

```cli
dragonfly> SET user:1001 '{"name":"Alice"}' EX 30
OK
dragonfly> GET user:1001
"{\"name\":\"Alice\"}"
```

## Best Practices

- Use specific expiration options (EX, PX) to avoid memory bloat from long-lived keys.
- Combine `SET` with NX/XX to ensure atomicity in distributed systems.

## Common Mistakes

- Forgetting to set an expiration on temporary data, leading to unnecessary memory usage.
- Misusing NX/XX options without understanding their conditional logic.

## FAQs

### What happens if I use both NX and XX options together?

Using both NX (set if not exists) and XX (set if exists) together makes no sense and `SET` will return an error.

### Can I use `SET` to update the expiration time of an existing key?

Yes, you can use `SET` with the KEEPTTL option to update the value without altering the original TTL.
