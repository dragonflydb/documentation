---
description: Discover how to use Redis SET command to attach a value to a specific key in the database.
---

import PageTitle from '@site/src/components/PageTitle';

# SET

<PageTitle title="Redis SET Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `SET` command in Redis is used to set the value of a key. This command will create the key if it does not already exist or overwrite the existing value if the key is already present. Typical use cases include caching data, storing session information, or maintaining simple counters.

## Syntax

```plaintext
SET key value [EX seconds] [PX milliseconds] [NX|XX] [KEEPTTL] [GET]
```

## Parameter Explanations

- `key`: The name of the key you wish to set.
- `value`: The value you want to associate with the key.
- `EX seconds`: Set the specified expire time, in seconds.
- `PX milliseconds`: Set the specified expire time, in milliseconds.
- `NX`: Only set the key if it does not already exist.
- `XX`: Only set the key if it already exists.
- `KEEPTTL`: Retain the existing TTL associated with the key.
- `GET`: Return the old value stored at the key, when replacing it with a new value.

## Return Values

- If `GET` option is used: The old value stored at the key, or `nil` if the key did not exist.
- Otherwise: A simple string reply `OK`.

### Examples of possible outputs:

```plaintext
OK
(nil)
"old_value"
```

## Code Examples

```cli
dragonfly> SET mykey "Hello"
"OK"
dragonfly> SET mykey "World" EX 10
"OK"
dragonfly> SET mykey "NewValue" NX
(nil)
dragonfly> SET mykey "AnotherValue" XX
"OK"
dragonfly> GET mykey
"AnotherValue"
dragonfly> SET mykey "FinalValue" GET
"AnotherValue"
"OK"
dragonfly> GET mykey
"FinalValue"
```

## Best Practices

- Utilize the `NX` or `XX` options to avoid unintentional overwrites.
- Use `EX` or `PX` for setting automatic expiration times on keys that should not persist indefinitely.

## Common Mistakes

- Overlooking the optional parameters like `EX`, `PX`, `NX`, and `XX`, which can lead to unintended key overwrites and persistence.
- Forgetting to handle the return values when using `GET` option, especially when expecting old values for logic operations.

## FAQs

### Can I use both `EX` and `PX` together?

No, you must choose either `EX` for seconds or `PX` for milliseconds, but not both simultaneously.

### What happens if I use `NX` and `XX` together?

Using `NX` and `XX` together is contradictory. Redis will return an error since a key cannot both exist and not exist at the same time.

### How do I retain the existing TTL of a key?

Use the `KEEPTTL` option to keep the current TTL (Time-To-Live) unchanged when setting a new value.
