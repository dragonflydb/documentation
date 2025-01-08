---
description: Learn how to use Redis XSETID to set the last delivered ID for streams.
---

import PageTitle from '@site/src/components/PageTitle';

# XSETID

<PageTitle title="Redis XSETID Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `XSETID` command is used to set the ID of an existing consumer group in a stream.
This command allows you to manually manage the last delivered ID of a consumer group, which can be particularly useful in scenarios where you need precise control over message processing.

## Syntax

```shell
XSETID key groupname id
```

## Parameter Explanations

- `key`: The key of the stream for which you want to set the consumer group ID.
- `groupname`: The name of the consumer group whose last delivered ID you want to set.
- `id`: The new ID you want to assign as the last delivered ID of the consumer group. This should be a valid stream ID.

## Return Values

The command returns `OK` if the ID for the consumer group is successfully set.

## Code Examples

### Basic Example

Set the last delivered ID for a consumer group:

```shell
dragonfly$> XGROUP CREATE mystream mygroup 0
OK
# Assuming some entries have been added to the stream...
dragonfly$> XSETID mystream mygroup 1526569495631-0
OK
```

### Changing the Last Delivered ID

Imagine you have read up to a certain message ID, and you want to mark this as the new last delivered ID:

```shell
# Add some entries to the stream
dragonfly$> XADD mystream * message "Hello World"
1526569495631-0
dragonfly$> XADD mystream * message "Another Message"
1526569495632-0

# Now change the last delivered ID for `mygroup`
dragonfly$> XSETID mystream mygroup 1526569495632-0
OK
```

This ensures that the consumer group acknowledges up to the specified message ID.

### Error Handling

Attempt to set a last delivered ID that doesn't exist:

```shell
dragonfly$> XSETID mystream mygroup 9999999999999-0
(error) ERR The specified ID is greater than the maximal ID in the stream
```

## Best Practices

- Ensure the provided `id` exists in the stream; otherwise, the command will return an error.
- Use `XSETID` carefully, as setting the wrong ID can lead to message delivery inconsistencies.

## Common Mistakes

- Setting an ID that does not exist in the stream.
- Overwriting the last delivered ID in a way that skips some messages unintentionally.

## FAQs

### What happens if the consumer group does not exist?

If the consumer group does not exist, `XSETID` will return an error because there is no group to set the ID for.

### Can I use wildcard or relative IDs?

No, you must specify an exact stream ID that exists in the stream.
