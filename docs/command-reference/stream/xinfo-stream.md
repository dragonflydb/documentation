---
description:  Learn how to use Redis XINFO STREAM command to get information about a stream.
---

import PageTitle from '@site/src/components/PageTitle';

# XINFO STREAM

<PageTitle title="Redis XINFO STREAM Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `XINFO STREAM` command provides information about a specific stream.
This is particularly useful for monitoring and debugging streams, as it helps you understand the structure and state of a stream.

## Syntax

```shell
XINFO STREAM key
```

## Parameter Explanations

- `key`: The key of the stream for which information is to be retrieved.

## Return Values

The command returns a list of key-value pairs providing information about the specified stream's state and elements.

## Code Examples

### Retrieve Stream Information

Get information about a stream:

```shell
dragonfly$> XADD mystream * sensor-id 1234 temperature 19.8
"1632494980015-0"
dragonfly$> XINFO STREAM mystream
 1) "length"
 2) (integer) 1
 3) "radix-tree-keys"
 4) (integer) 1
 5) "radix-tree-nodes"
 6) (integer) 2
 7) "groups"
 8) (integer) 0
 9) "last-generated-id"
10) "1632494980015-0"
11) "first-entry"
12) 1) "1632494980015-0"
    2) 1) "sensor-id"
       2) "1234"
       3) "temperature"
       4) "19.8"
13) "last-entry"
14) 1) "1632494980015-0"
    2) 1) "sensor-id"
       2) "1234"
       3) "temperature"
       4) "19.8"
```

## Best Practices

- Regularly use `XINFO STREAM` to monitor the health and performance of streams.
- Analyze the output to optimize memory and understand stream usage patterns.

## Common Mistakes

- Not grasping the meaning of each output field; ensure you understand terms like "radix-tree-keys" and "last-generated-id".
- Forgetting that `XINFO STREAM` only queries data and does not modify the stream content.

## FAQs

### What does "radix-tree-keys" signify?

"radix-tree-keys" indicates the number of entries in the underlying radix tree data structure, which can help assess memory use.

### How do I interpret "first-entry" and "last-entry"?

"first-entry" and "last-entry" give you the stream's start and end records, which are important for identifying the current pattern of data.