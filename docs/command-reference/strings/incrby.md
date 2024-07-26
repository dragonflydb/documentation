---
description: Learn to use Redis INCRBY to increase the integer value of a key by a given amount.
---

import PageTitle from '@site/src/components/PageTitle';

# INCRBY

<PageTitle title="Redis INCRBY Explained (Better Than Official Docs)" />

## Introduction

The `INCRBY` command in Redis is used to increment the integer value of a key by a specified amount. This atomic operation ensures that increments can happen safely even when multiple clients are accessing the same key concurrently. It is particularly useful in scenarios like counters, rate limiting, and ensuring accurate counts.

## Syntax

```plaintext
INCRBY key increment
```

## Parameter Explanations

- `key`: The name of the key whose value you want to increment. This key must contain an integer.
- `increment`: The integer value by which the key's value will be increased. It can be positive or negative.

## Return Values

The command returns the value of the key after the increment operation.

```cli
(integer) new_value
```

### Example Outputs:

- If the original value is 5 and the increment is 3, the new value will be 8.
- If the key does not exist, it is set to `0` before performing the operation, and then incremented.

## Code Examples

### Basic Example

Increment the value by 5:

```cli
dragonfly> SET mycounter 10
OK
dragonfly> INCRBY mycounter 5
(integer) 15
```

### Page View Counter

Track page views for a specific URL:

```cli
dragonfly> INCRBY page:home 1
(integer) 1
dragonfly> INCRBY page:home 1
(integer) 2
dragonfly> INCRBY page:about 1
(integer) 1
```

### Rate Limiting

Implementing a simple rate limiter based on API calls:

```cli
dragonfly> INCRBY user:123:api_calls 1
(integer) 1
dragonfly> INCRBY user:123:api_calls 1
(integer) 2
```

### Event Counting

Count occurrences of particular events:

```cli
dragonfly> INCRBY event:login 1
(integer) 1
dragonfly> INCRBY event:purchase 1
(integer) 1
```

## Best Practices

- Always ensure that the key's value is initialized to an integer. Use `SET key 0` if necessary.
- Use meaningful key names to avoid collisions and make debugging easier.

## Common Mistakes

- Using `INCRBY` on a key that contains a non-integer value will result in an error.
- Forgetting to initialize the key if you expect it to start at zero. Redis will handle this gracefully by assuming it starts from 0, but it's good practice to initialize.

## FAQs

### What happens if the key does not exist?

If the key does not exist, Redis treats it as if it has a value of `0`, performs the increment, and sets the key to the new value.

### Can `INCRBY` handle negative increments?

Yes, you can use negative values to decrement the key's value.

```cli
dragonfly> SET mycounter 10
OK
dragonfly> INCRBY mycounter -3
(integer) 7
```
