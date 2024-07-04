---
description: Discover how to use Redis GETEX for fetching a key's value and setting its expiration.
---

import PageTitle from '@site/src/components/PageTitle';

# GETEX

<PageTitle title="Redis GETEX Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `GETEX` command in Redis is used to get the value of a key and optionally set its expiration. This command is particularly useful when you need to retrieve the value of a key while simultaneously updating its time-to-live (TTL). Typical scenarios include caching mechanisms where you want to extend the TTL of frequently accessed items without additional commands.

## Syntax

```plaintext
GETEX key [EX seconds] [PX milliseconds] [EXAT timestamp-seconds] [PXAT timestamp-milliseconds] [PERSIST]
```

## Parameter Explanations

- `key`: The key whose value you want to retrieve.
- `EX seconds`: Sets the expiration time of the key in seconds.
- `PX milliseconds`: Sets the expiration time of the key in milliseconds.
- `EXAT timestamp-seconds`: Sets the expiration time of the key as a Unix timestamp in seconds.
- `PXAT timestamp-milliseconds`: Sets the expiration time of the key as a Unix timestamp in milliseconds.
- `PERSIST`: Removes the expiration time from the key.

## Return Values

The `GETEX` command returns the value of the specified key if it exists, or `nil` if the key does not exist.

### Examples:

- If the key exists:
  ```plaintext
  "value"
  ```
- If the key does not exist:
  ```plaintext
  (nil)
  ```

## Code Examples

```cli
dragonfly> SET mykey "Hello"
OK
dragonfly> GETEX mykey EX 10
"Hello"
dragonfly> TTL mykey
(integer) 10
dragonfly> GETEX mykey PX 5000
"Hello"
dragonfly> TTL mykey
(integer) 5
dragonfly> GETEX mykey PERSIST
"Hello"
dragonfly> TTL mykey
(integer) -1
dragonfly> GETEX nonexistingkey EX 10
(nil)
```

## Best Practices

- Use the `GETEX` command to minimize the number of operations needed for cache access and TTL updates, improving performance and reducing complexity.
- Be mindful of setting appropriate expiration times to balance between cache freshness and resource utilization.

## Common Mistakes

- Forgetting that if the key does not exist, `GETEX` will return `nil`, which can lead to unexpected null value handling if not properly checked.
- Misunderstanding TTL values, especially when switching between seconds and milliseconds, which may cause keys to expire sooner or later than intended.

## FAQs

### What happens if no expiration parameter is given?

If no expiration parameter is provided, `GETEX` behaves like the `GET` command and returns the value without modifying the TTL.

### Can I use `GETEX` on non-string data types?

No, `GETEX` is designed to work with string values. Using it on other data types will result in an error.
