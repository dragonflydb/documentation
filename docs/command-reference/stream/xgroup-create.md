---
description:  Learn how to use Redis XGROUP CREATE to create a new consumer group.
---

import PageTitle from '@site/src/components/PageTitle';

# XGROUP CREATE

<PageTitle title="Redis XGROUP CREATE Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `XGROUP CREATE` command is used to create a consumer group associated with a stream.
It sets up a group that can be used to consume messages from the stream with specific guarantees regarding message delivery and processing.
This command is essential for managing distributed message processing systems where consumer groups must handle the workload.

## Syntax

```shell
XGROUP CREATE <key> <groupname> <id | $> [MKSTREAM]
```

## Parameter Explanations

- `<key>`: The key name of the stream.
- `<groupname>`: The name given to the consumer group.
- `<id | $>`: The ID of the last-delivered message. Use `$` to start from the new messages.
- `MKSTREAM` (optional): Automatically create the stream if it does not exist.

## Return Values

- This command usually returns `OK` if the consumer group was created successfully.
- If a consumer group with the same name already exists, it returns an error.

## Code Examples

### Basic Example

Create a consumer group for an existing stream starting with new messages:

```shell
dragonfly$> XGROUP CREATE mystream mygroup $
OK
```

### Consumer Group with Specific ID

Create the consumer group starting from a specific message ID:

```shell
dragonfly$> XGROUP CREATE mystream mygroup 1609459200000-0
OK
```

### `MKSTREAM` Ensures Stream Creation

Create a consumer group while automatically creating the stream if it does not exist:

```shell
dragonfly$> XGROUP CREATE newstream mygroup $ MKSTREAM
OK
```

## Best Practices

- Use `$` for the `<id>` parameter if you want the group to start processing only new messages.
- The `MKSTREAM` option is useful for ensuring that a consumer group is set up correctly even if the stream does not exist.

## Common Mistakes

- Attempting to create a consumer group in a non-existent stream without using `MKSTREAM`.
- Using an incorrect or misspelled stream key or group name when setting up a group.

## FAQs

### What happens if the stream does not exist when I run `XGROUP CREATE`?

If the stream does not exist and you don't use the `MKSTREAM` option, the command will return an error.
With `MKSTREAM`, the stream is automatically created.

### Can I create a consumer group with the same name twice?

No, attempting to create a consumer group with an existing name returns an error.
