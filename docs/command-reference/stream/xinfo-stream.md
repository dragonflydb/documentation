---
description:  Learn how to use Redis XINFO STREAM command to get information about a stream.
---

import PageTitle from '@site/src/components/PageTitle';

# XINFO STREAM

<PageTitle title="Redis XINFO STREAM Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `XINFO STREAM` command provides information about a specific stream.
This command can be used to monitor and debug streams, as it helps you understand the structure and state of a stream.

## Syntax

```shell
XINFO STREAM key [FULL [COUNT count]]
```

## Parameter Explanations

- `key`: The key of the stream for which information is to be retrieved.
- `FULL` (optional): If specified, the command returns additional details about the stream.
- `COUNT count` (optional): If `FULL` is specified, this parameter limits the number of returned stream and PEL entries returned.
  `COUNT` is default to `10`. Setting `COUNT` to `0` returns all entries, which should be used with caution as it increases execution time for large streams.

## Return Values

- The command returns a list of information about the specified stream's state and entries.

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

- Forgetting that `XINFO STREAM` only queries data and does not modify the stream content.
- Not grasping the meaning of each output field; ensure you understand terms like `radix-tree-keys` and `last-generated-id` in the context of streams.

## FAQs

### What does `radix-tree-keys` signify?

`radix-tree-keys` indicates the number of entries in the underlying radix tree data structure for streams.

### How do I interpret `first-entry` and `last-entry`?

`first-entry` and `last-entry` give you the stream's start and end records, which helps to identify the pattern of data.
