---
description: Learn how to use Redis XLEN to get the length of a stream.
---

import PageTitle from '@site/src/components/PageTitle';

# XLEN

<PageTitle title="Redis XLEN Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `XLEN` command in Redis is used to get the length of a stream. This command is particularly useful when working with streams, allowing you to determine how many entries are present in a given stream. Typical scenarios include monitoring the size of the stream for processing purposes or for managing memory usage.

## Syntax

```cli
XLEN <stream>
```

## Parameter Explanations

- `<stream>`: The name of the stream whose length you want to retrieve. This parameter is mandatory.

## Return Values

The `XLEN` command returns an integer representing the number of entries in the specified stream.

**Example:**

```cli
(integer) 4
```

## Code Examples

```cli
dragonfly> XADD mystream * sensor-id 1234 temperature 19.8
"1657896745800-0"
dragonfly> XADD mystream * sensor-id 1235 temperature 21.2
"1657896746800-0"
dragonfly> XADD mystream * sensor-id 1236 temperature 22.1
"1657896747800-0"
dragonfly> XLEN mystream
(integer) 3
```

## Best Practices

- Ensure that the stream exists before using the `XLEN` command to avoid unnecessary errors.
- Use `XLEN` in monitoring scripts to keep track of the stream size and manage resources effectively.

## Common Mistakes

- **Non-existent Stream**: Running `XLEN` on a non-existent stream will return `0`. Always verify if the stream exists if `0` is not an expected outcome.

## FAQs

### What happens if I use `XLEN` on an empty stream?

If you use `XLEN` on a stream that has been created but contains no entries, the command will correctly return `(integer) 0`.

### Can `XLEN` be used with other data types?

No, `XLEN` is specifically designed for streams. Using it on other data types will result in an error.
