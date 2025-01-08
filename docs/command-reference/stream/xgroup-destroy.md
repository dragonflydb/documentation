---
description:  Learn how to use Redis XGROUP DESTROY to remove a consumer group.
---

import PageTitle from '@site/src/components/PageTitle';

# XGROUP DESTROY

<PageTitle title="Redis XGROUP DESTROY Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `XGROUP DESTROY` command is utilized to delete a consumer group from a specified stream.
This can be particularly beneficial if the consumer group is no longer needed, thereby freeing up resources.
**The consumer group will be destroyed regardless of active consumers and pending messages.
Use this command only when absolutely necessary.**

## Syntax

```shell
XGROUP DESTROY key group
```

## Parameter Explanations

- `key`: The name of the stream from which the consumer group will be deleted.
- `group`: The name of the consumer group to be deleted.

## Return Values

- The command returns `1` if the consumer group is successfully deleted.
- The command returns `0` if the consumer group does not exist.

## Code Examples

### Basic Example

Delete a consumer group named `mygroup` from `mystream`:

```shell
dragonfly$> XADD mystream * name "Alice"
"1736315194818-0"

dragonfly$> XGROUP CREATE mystream mygroup 0
OK

# Delete the consumer group 'mygroup'.
# Since the group exists, the command returns 1.
dragonfly$> XGROUP DESTROY mystream mygroup
(integer) 1

# Attempting to delete the group again will return 0.
dragonfly$> XGROUP DESTROY mystream mygroup
(integer) 0
```

## Best Practices

- **Ensure that you no longer need the consumer group** before using `XGROUP DESTROY`.
- **Verify the group's dependencies or any critical data processed by the group to avoid accidental data loss.**

## Common Mistakes

- Not assessing dependencies before deletion, which might disrupt the processing workflow.

## FAQs

### What happens if the stream does not exist?

An error will be thrown if the stream does not exist.

### Can `XGROUP DESTROY` be used on active consumer groups?

Yes, you can delete active consumer groups, but it is advised to ensure they are no longer needed to prevent disruptions.
