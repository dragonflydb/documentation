---
description: Learn how to use Redis XLEN to get the length of a stream.
---

import PageTitle from '@site/src/components/PageTitle';

# XLEN

<PageTitle title="Redis XLEN Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`XLEN` is a Redis command used to get the length of a stream. This command is particularly useful in scenarios where you need to monitor the size of the stream, implement logic based on the number of entries, or perform housekeeping tasks.

## Syntax

```cli
XLEN key
```

## Parameter Explanations

- `key`: The name of the stream for which you want to obtain the length. This is a required parameter and must be a valid stream key.

## Return Values

`XLEN` returns the number of entries in the stream. If the stream does not exist, it returns 0.

**Example Output:**

- When the stream has entries: `(integer) 5`
- When the stream does not exist: `(integer) 0`

## Code Examples

```cli
dragonfly> XADD mystream * field1 value1 field2 value2
"1684749275426-0"
dragonfly> XADD mystream * field1 value3 field2 value4
"1684749281234-0"
dragonfly> XLEN mystream
(integer) 2
dragonfly> XLEN nonexistingstream
(integer) 0
```

## Best Practices

- Regularly monitor the length of streams to keep track of data growth and manage resources effectively.
- Implement checks using `XLEN` to trigger actions when a stream exceeds a certain size.

## Common Mistakes

- Using `XLEN` on a key that is not a stream will result in an error. Always ensure the key is associated with a stream data type.

## FAQs

### What happens if I use `XLEN` on a key that is not a stream?

You will receive an error message indicating that the key is not a stream type. Make sure to validate the key's data type before using `XLEN`.

### Can `XLEN` return a negative value?

No, `XLEN` will always return a non-negative integer. If the stream does not exist, it returns 0.
