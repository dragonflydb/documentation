---
description: Understand Redis JSON.NUMMULTBY command to multiply a numeric value within a JSON document.
---

import PageTitle from '@site/src/components/PageTitle';

# JSON.NUMMULTBY

<PageTitle title="Redis JSON.NUMMULTBY Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`JSON.NUMMULTBY` is a Redis command used with the RedisJSON module to multiply a numeric value in a JSON document by a specified multiplier. This command is particularly useful for applications that need to perform atomic updates on numeric fields stored within JSON structures, ensuring data consistency and reducing the need for additional application logic.

## Syntax

```plaintext
JSON.NUMMULTBY <key> <path> <number>
```

## Parameter Explanations

- **key**: The key under which the JSON document is stored.
- **path**: The path to the numeric value within the JSON document that should be multiplied. This can use dot notation to traverse nested objects.
- **number**: The multiplier, which must be a valid numeric value.

## Return Values

The `JSON.NUMMULTBY` command returns the new value of the multiplied number after the operation is successfully completed.

### Example Outputs:

- If the operation is successful and the resulting value is `10`, the output will be:

  ```plaintext
  "10"
  ```

- If the path does not exist or is not numeric, an error message will be returned.

## Code Examples

```cli
dragonfly> JSON.SET mydoc '$' '{"count":5}'
OK
dragonfly> JSON.NUMMULTBY mydoc '$.count' 2
"10"
dragonfly> JSON.GET mydoc '$.count'
"10"
```

## Best Practices

- Ensure the path points to a numeric value; otherwise, the command will fail.
- Use `JSON.GET` before and after `JSON.NUMMULTBY` to verify the changes.

## Common Mistakes

- Applying `JSON.NUMMULTBY` on non-numeric values will result in an error.
- Using an incorrect path syntax can lead to failed operations or unexpected results.

## FAQs

### What happens if I try to multiply a non-numeric value?

You will receive an error indicating that the specified path does not resolve to a numeric value.

### Can I use negative numbers as multipliers?

Yes, you can use negative numbers, zero, and decimal values as multipliers.
