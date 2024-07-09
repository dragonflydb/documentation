---
description: "Learn how to use Redis HSTRLEN command to get the length of a hash field value. A helpful command for data size calculations."
---

import PageTitle from '@site/src/components/PageTitle';

# HSTRLEN

<PageTitle title="Redis HSTRLEN Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`HSTRLEN` is a Redis command used to determine the length of the string value associated with a specified field in a hash. It's typically used to validate or monitor the size of data stored within a hash field, particularly in applications where storage or transmission costs are concerned.

## Syntax

```
HSTRLEN key field
```

## Parameter Explanations

- `key`: The name of the hash.
- `field`: The specific field within the hash for which you want to get the length of the string value.

## Return Values

The command returns an integer representing the length of the string value associated with the specified field. If the field does not exist, it returns 0.

Examples:

- If the field exists: `(integer) <length>`
- If the field does not exist: `(integer) 0`

## Code Examples

```cli
dragonfly> HSET myhash field1 "Hello"
(integer) 1
dragonfly> HSTRLEN myhash field1
(integer) 5
dragonfly> HSTRLEN myhash field2
(integer) 0
```

## Best Practices

It’s good practice to check if the field exists before using `HSTRLEN` if there is uncertainty about its existence.

## Common Mistakes

- Using `HSTRLEN` on a non-existing key will result in 0, which might be mistakenly interpreted as the field having an empty string value.

## FAQs

### What happens if the key itself does not exist?

If the key does not exist, `HSTRLEN` returns 0, as there is no field to measure.

### Can `HSTRLEN` be used on fields that store non-string values?

`HSTRLEN` should only be used on fields storing string values, as it measures string length. Using it on non-string values can lead to unexpected results.
