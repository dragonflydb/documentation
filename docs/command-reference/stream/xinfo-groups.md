---
description: Learn how to use Redis XINFO GROUPS to get information about consumer groups of a stream.
---

import PageTitle from '@site/src/components/PageTitle';

# XINFO GROUPS

<PageTitle title="Redis XINFO GROUPS Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `XINFO GROUPS` command provides information about consumer groups associated with a specific stream.
This command is essential for monitoring and managing stream processing tasks, providing insights into consumer group configurations and activity.

## Syntax

```shell
XINFO GROUPS key
```

## Parameter Explanations

- `key`: The key of the stream for which consumer groups information is requested.

## Return Values

The command returns a list of dictionaries, each dictionary representing a consumer group and its details.
The details include fields such as `name`, `consumers`, `pending`, `last-delivered-id`, etc.

## Code Examples

### Basic Example

Get information about consumer groups for a stream:

```shell
dragonfly$> XGROUP CREATE mystream mygroup $
OK
dragonfly$> XINFO GROUPS mystream
1) 1) "name"
   2) "mygroup"
   3) "consumers"
   4) (integer) 0
   5) "pending"
   6) (integer) 0
   7) "last-delivered-id"
   8) "0-0"
```

### Monitor Multiple Consumer Groups

Creating and monitoring multiple consumer groups:

```shell
dragonfly$> XGROUP CREATE mystream group1 $
OK
dragonfly$> XGROUP CREATE mystream group2 $
OK
dragonfly$> XINFO GROUPS mystream
1) 1) "name"
   2) "group1"
   3) "consumers"
   4) (integer) 0
   5) "pending"
   6) (integer) 0
   7) "last-delivered-id"
   8) "0-0"
2) 1) "name"
   2) "group2"
   3) "consumers"
   4) (integer) 0
   5) "pending"
   6) (integer) 0
   7) "last-delivered-id"
   8) "0-0"
```

## Best Practices

- Regularly use `XINFO GROUPS` to check on the health and status of consumer groups in your stream processing architecture.
- Ensure consumer groups are correctly created with unique and descriptive names to avoid confusion and manage them effectively.

## Common Mistakes

- Omitting the `key` parameter, which is necessary to identify the stream for which group information is needed.
- Assuming that `XINFO GROUPS` modifies consumer groups; it only retrieves information.

## FAQs

### What happens if the stream key does not exist?

If the stream key does not exist, `XINFO GROUPS` returns an empty list as there are no consumer groups associated with a nonexistent stream.

### Can `XINFO GROUPS` be used on keys that are not streams?

No, `XINFO GROUPS` is specific to streams, and attempting to use it on a non-stream key will result in an error.
