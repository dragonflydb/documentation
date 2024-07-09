---
description: Learn how to use Redis JSON.NUMINCRBY command to increment a number inside a JSON document.
---

import PageTitle from '@site/src/components/PageTitle';

# JSON.NUMINCRBY

<PageTitle title="Redis JSON.NUMINCRBY Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`JSON.NUMINCRBY` is a command in the Redis module `RedisJSON`, which allows for the manipulation of numeric values within a JSON document. It is used to increment a numerical value at a specified path within a JSON structure. Typical scenarios include incrementing counters, updating scores, or modifying numerical fields within complex JSON documents.

## Syntax

```plaintext
JSON.NUMINCRBY key path increment
```

## Parameter Explanations

- **key**: The key under which the JSON document is stored.
- **path**: The JSONPath expression specifying the location of the number within the JSON document to be incremented.
- **increment**: The numeric value by which to increment the target value. Can be an integer or floating-point number.

## Return Values

The command returns the new value after the increment operation. If the specified path does not contain a number, an error is returned.

### Example Outputs

1. Incrementing a number:

   ```cli
   dragonfly> JSON.SET mydoc $ '{"counter": 5}'
   OK
   dragonfly> JSON.NUMINCRBY mydoc $.counter 3
   (integer) 8
   ```

2. Incrementing a floating-point number:
   ```cli
   dragonfly> JSON.SET mydoc $ '{"score": 12.5}'
   OK
   dragonfly> JSON.NUMINCRBY mydoc $.score 2.5
   "15"
   ```

## Code Examples

Incrementing an integer field within a JSON document:

```cli
dragonfly> JSON.SET mydoc $ '{"views": 100}'
OK
dragonfly> JSON.NUMINCRBY mydoc $.views 10
(integer) 110
```

Incrementing a floating-point field within a JSON document:

```cli
dragonfly> JSON.SET mydoc $ '{"rating": 4.5}'
OK
dragonfly> JSON.NUMINCRBY mydoc $.rating 0.5
"5"
```

## Best Practices

- Ensure that the path specified points to a numerical value; otherwise, the command will return an error.
- Use this command when you need atomic increments within a JSON document, avoiding the need to fetch-modify-store.

## Common Mistakes

- **Non-numeric Paths**: Attempting to increment a non-numeric value will result in an error.

  ```cli
  dragonfly> JSON.SET mydoc $ '{"name": "John"}'
  OK
  dragonfly> JSON.NUMINCRBY mydoc $.name 1
  (error) ERR wrong type of path value - expected a number but found string
  ```

- **Incorrect Path Specification**: Ensure the JSONPath accurately points to the intended numerical value.

## FAQs

### What happens if the path does not exist?

If the specified path does not exist within the JSON document, the command will return an error indicating that no matching path was found.

### Can I use JSON.NUMINCRBY on nested JSON structures?

Yes, you can use JSONPath to target deeply nested numerical values within a complex JSON structure.
