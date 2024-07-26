---
description: Discover how to use Redis GETEX for fetching a key's value and setting its expiration.
---

import PageTitle from '@site/src/components/PageTitle';

# GETEX

<PageTitle title="Redis GETEX Explained (Better Than Official Docs)" />

## Introduction

The `GETEX` command in Redis fetches the value of a key and sets its expiration time simultaneously. This command is essential when you want to retrieve the value of a key but also ensure that it's automatically removed after a specified period.

## Syntax

```cli
GETEX key [EX seconds|PX milliseconds|EXAT unix-time-seconds|PXAT unix-time-milliseconds|PERSIST]
```

## Parameter Explanations

- **key**: The name of the key you want to fetch and set the expiration for.
- **EX seconds**: Set the expiration time in seconds.
- **PX milliseconds**: Set the expiration time in milliseconds.
- **EXAT unix-time-seconds**: Set the expiration time as a Unix timestamp in seconds.
- **PXAT unix-time-milliseconds**: Set the expiration time as a Unix timestamp in milliseconds.
- **PERSIST**: Remove the existing expiration of the key, making it persistent.

## Return Values

- **String**: The value of the key if it exists.
- **nil**: If the key does not exist.

#### Example Outputs

- If the key exists:
  ```cli
  "value"
  ```
- If the key does not exist:
  ```cli
  (nil)
  ```

## Code Examples

### Basic Example

Fetch the value of a key and set its expiration time to 10 seconds.

```cli
dragonfly> SET mykey "Hello"
OK
dragonfly> GETEX mykey EX 10
"Hello"
dragonfly> TTL mykey
(integer) 9
```

### Use Case: Session Management

Automatically expire user sessions after inactivity.

```cli
dragonfly> SET session:user123 "session_data"
OK
dragonfly> GETEX session:user123 EX 300
"session_data"
dragonfly> TTL session:user123
(integer) 299
```

### Use Case: Cache Control

Refresh cache data and extend its expiration without losing the original value.

```cli
dragonfly> SET cache:item123 "cached_value"
OK
dragonfly> GETEX cache:item123 PX 15000
"cached_value"
dragonfly> PTTL cache:item123
(integer) 14999
```

### Use Case: Persistent Data with Occasional Expiry

Set a temporary expiration on a key and later remove the expiration.

```cli
dragonfly> SET temp:data "important"
OK
dragonfly> GETEX temp:data EX 60
"important"
dragonfly> TTL temp:data
(integer) 59
dragonfly> GETEX temp:data PERSIST
"important"
dragonfly> TTL temp:data
(integer) -1
```

## Best Practices

- Use `GETEX` to manage session lifecycles efficiently by setting appropriate expiration times.
- Combine `GETEX` with other commands like `SET` to maintain cache freshness without manual intervention.

## Common Mistakes

- Forgetting to provide an expiration option (`EX`, `PX`, etc.) will result in an error since the expiration modifier is required unless using `PERSIST`.
- Misunderstanding Unix timestamps for `EXAT` and `PXAT` can lead to incorrect expiration times. Ensure correct conversion.

## FAQs

### What happens if I use `GETEX` on a non-existing key?

`GETEX` will return `(nil)` if the key does not exist, and no expiration will be set since there is no value to associate it with.

### Can I use `GETEX` to make a key persistent?

Yes, using `GETEX key PERSIST` removes the expiration, making the key persistent while returning its current value.
