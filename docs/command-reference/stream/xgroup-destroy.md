---
description:  Learn how to use Redis XGROUP DESTROY to remove a consumer group.
---

import PageTitle from '@site/src/components/PageTitle';

# XGROUP DESTROY

<PageTitle title="Redis XGROUP DESTROY Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `XGROUP DESTROY` command is utilized to delete a consumer group from a specified stream.
This can be particularly beneficial if the consumer group is no longer needed, thereby freeing up resources.

## Syntax

```shell
XGROUP DESTROY stream groupname
```

## Parameter Explanations

- `stream`: The name of the stream from which the consumer group will be deleted.
- `groupname`: The name of the consumer group to be deleted.

## Return Values

The command returns `1` if the consumer group was successfully deleted and `0` if the consumer group does not exist.

## Code Examples

### Basic Example of Deleting a Consumer Group

Delete a consumer group named 'group1' from the 'mystream' stream:

```shell
dragonfly> XGROUP DESTROY mystream group1
(integer) 1
```

### Attempt to Delete a Non-Existent Consumer Group

Attempt to delete a consumer group named 'nonexistent' from the 'mystream' stream:

```shell
dragonfly> XGROUP DESTROY mystream nonexistent
(integer) 0
```

## Best Practices

- Ensure that you no longer need the consumer group before using `XGROUP DESTROY`.
- Verify the group’s dependencies or any critical data processed by the group to avoid accidental data loss.

## Common Mistakes

- Attempting to use `XGROUP DESTROY` on a consumer group that does not exist, which will result in a return value of `0`.
- Not assessing dependencies before deletion, which might disrupt the processing workflow.

## FAQs

### What happens if the stream does not exist?

If the stream does not exist, the command will return `0` because the consumer group cannot exist without its associated stream.

### Can `XGROUP DESTROY` be used on active consumer groups?

Yes, you can delete active consumer groups, but it is advised to ensure they are no longer needed to prevent disruptions.