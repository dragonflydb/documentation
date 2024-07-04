---
description: Discover the use of Redis DECR for decrementing the integer value of a key.
---

import PageTitle from '@site/src/components/PageTitle';

# DECR

<PageTitle title="Redis DECR Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `DECR` command in Redis is used to decrement the value of a key by 1. It is commonly used for counters, such as tracking the number of remaining attempts in an application or managing stock levels in inventory systems.

## Syntax

```cli
DECR key
```

## Parameter Explanations

- **key**: The name of the key whose value you want to decrement. This key must hold a string that can be represented as an integer.

## Return Values

- **Integer**: The value of the key after the decrement operation.

### Examples:

If the key does not exist, it is set to 0 before performing the operation.

## Code Examples

```cli
dragonfly> SET counter 10
OK
dragonfly> DECR counter
(integer) 9
dragonfly> DECR counter
(integer) 8
dragonfly> GET counter
"8"
dragonfly> DECR non_existent_key
(integer) -1
dragonfly> GET non_existent_key
"-1"
```

## Best Practices

- Ensure that the key holds a value that can be interpreted as an integer.
- When using `DECR` on keys that might not exist, design your application logic to handle cases where a missing key starts from 0.

## Common Mistakes

- Using `DECR` on a key holding non-integer values will cause an error.
- Assuming `DECR` will only work on pre-existing keys; if the key does not exist, Redis initializes it to 0 and then decrements it.

## FAQs

### What happens if I use `DECR` on a key that contains a string?

An error will be returned because `DECR` expects the key to contain an integer value.

### Can `DECR` create a key if it doesn't exist?

Yes, if the key does not exist, Redis will create the key with a value of `0` and then perform the decrement operation.
