---
description: Learn how to use the Redis JSON.TOGGLE command to invert a boolean value in a JSON document.
---

import PageTitle from '@site/src/components/PageTitle';

# JSON.TOGGLE

<PageTitle title="Redis JSON.TOGGLE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`JSON.TOGGLE` is a Redis command used to toggle the boolean value at a specified path in a JSON document stored within a Redis key. This command is particularly useful in scenarios where JSON structures are frequently updated, such as real-time applications that require quick modifications of feature flags or other boolean settings.

## Syntax

```plaintext
JSON.TOGGLE <key> <path>
```

## Parameter Explanations

- **`<key>`**: The Redis key where the JSON document is stored.
- **`<path>`**: The JSON path specifying the location of the boolean value to be toggled.

## Return Values

The `JSON.TOGGLE` command returns the new boolean value after the toggle operation.

Example return values:

- `(integer) 1` if the previous value was `false` and has been changed to `true`.
- `(integer) 0` if the previous value was `true` and has been changed to `false`.

## Code Examples

```cli
dragonfly> JSON.SET myjson . '{"active":true,"count":5}'
OK
dragonfly> JSON.TOGGLE myjson .active
(integer) 0
dragonfly> JSON.GET myjson
"{\"active\":false,\"count\":5}"
dragonfly> JSON.TOGGLE myjson .active
(integer) 1
dragonfly> JSON.GET myjson
"{\"active\":true,\"count\":5}"
```

## Best Practices

- Ensure that the path points to a valid boolean value; otherwise, the command will not execute as expected.
- Regularly validate your JSON structure to avoid errors due to incorrect paths or data types.

## Common Mistakes

- **Incorrect Path**: Using a path that does not exist or does not point to a boolean value. This will result in an error.
- **Data Type Mismatch**: Attempting to toggle a non-boolean value will lead to failed operations.

## FAQs

### What happens if the path does not exist?

If the specified path does not exist in the JSON document, the command will result in an error.

### Can I use `JSON.TOGGLE` on non-boolean values?

No, `JSON.TOGGLE` only works with boolean values. Attempting to use it on non-boolean values will result in an error.
