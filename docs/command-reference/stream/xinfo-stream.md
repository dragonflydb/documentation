---
description: Learn how to use Redis XINFO STREAM command to get information about a stream.
---

import PageTitle from '@site/src/components/PageTitle';

# XINFO STREAM

<PageTitle title="Redis XINFO STREAM Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`XINFO STREAM` provides detailed information about a Redis stream, including the length of the stream, the first and last entry IDs, and various other statistics. It is typically used for monitoring, debugging, and understanding the state of a Redis stream.

## Syntax

```cli
XINFO STREAM <key>
```

## Parameter Explanations

- `<key>`: The name of the stream to retrieve information from. This parameter is required.

## Return Values

The command returns a list of key-value pairs representing various pieces of information about the stream. For example:

- `length`: The number of entries in the stream.
- `radix-tree-keys`: Number of radix tree nodes.
- `radix-tree-nodes`: Number of radix tree nodes.
- `groups`: Number of consumer groups associated with the stream.
- `last-generated-id`: The ID of the last entry added to the stream.
- `first-entry` and `last-entry`: Details of the first and last entries, respectively.

Example output:

```plaintext
1) "length"
2) (integer) 10
3) "radix-tree-keys"
4) (integer) 5
5) "radix-tree-nodes"
6) (integer) 10
7) "groups"
8) (integer) 2
9) "last-generated-id"
10) "1609459200000-0"
11) "first-entry"
12) 1) "1609459200000-0"
    2) 1) "field1"
       2) "value1"
13) "last-entry"
14) 1) "1609459201000-0"
    2) 1) "field2"
       2) "value2"
```

## Code Examples

```cli
dragonfly> XADD mystream * field1 value1
"1609459200000-0"
dragonfly> XADD mystream * field2 value2
"1609459201000-0"
dragonfly> XINFO STREAM mystream
1) "length"
2) (integer) 2
3) "radix-tree-keys"
4) (integer) 1
5) "radix-tree-nodes"
6) (integer) 2
7) "groups"
8) (integer) 0
9) "last-generated-id"
10) "1609459201000-0"
11) "first-entry"
12) 1) "1609459200000-0"
    2) 1) "field1"
       2) "value1"
13) "last-entry"
14) 1) "1609459201000-0"
    2) 1) "field2"
       2) "value2"
```

## Best Practices

- Regularly monitor your streams using `XINFO STREAM` to ensure they are functioning as expected and to identify any potential issues early on.
- Use this command alongside other stream commands to gain a comprehensive view of stream health and performance.

## Common Mistakes

- Forgetting that the key parameter is mandatory. Always specify the stream key you want to inspect.
- Misinterpreting the output structure; ensure correct parsing to extract meaningful data.

## FAQs

### Why does `XINFO STREAM` return zero groups even though I have consumers reading from the stream?

`XINFO STREAM` shows the number of consumer groups, not individual consumers. Ensure you have created consumer groups explicitly using `XGROUP CREATE`.

### Can `XINFO STREAM` be used to check if a stream exists?

Yes, if the stream does not exist, `XINFO STREAM` will return an error, indicating the stream's absence.
