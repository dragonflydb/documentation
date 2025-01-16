---
description:  Learn how to use Redis XGROUP SETID to set the last delivered ID of a stream.
---

import PageTitle from '@site/src/components/PageTitle';

# XGROUP SETID

<PageTitle title="Redis XGROUP SETID Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `XGROUP SETID` command is used to **change the last delivered ID for a consumer group** in a stream.
This command is beneficial when you need to reprocess messages or adjust a consumer group's position in the stream.

## Syntax

```shell
XGROUP SETID key group <id | $>
```

## Parameter Explanations

- `key`: The key of the stream.
- `group`: The name of the consumer group whose last delivered ID is to be set.
- `<id | $>`: The ID you want the consumer group to consider as the last delivered ID.
  - Use `$` to set it to the last entry in the stream.
  - Use `0` to set the ID to the very first message in the stream.
  - You can use a specific ID. **If the ID does not exist in the stream, it is set to the next ID greater than the specified ID.**

## Return Values

- The command returns `OK` if the operation is successful or an error message if it fails.

## Code Examples

### Basic Example

Change the last delivered ID for a consumer group using a specific ID:

```shell
dragonfly$> XGROUP CREATE mystream mygroup $ MKSTREAM
OK

dragonfly$> XADD mystream * field1 value1
"1736318170000-0" # The first message ID.

dragonfly$> XADD mystream * field2 value2
"1736318179999-0" # The second message ID.

# Set the last delivered ID the a value that is
# greater than the first message ID, but less than the second message ID.
dragonfly$> XGROUP SETID mystream mygroup "1736318175555-0"
OK

# Read a message from the stream using a consumer.
# You can see that it starts to read from the second message.
dragonfly$> XREADGROUP GROUP mygroup consumer-1 COUNT 1 STREAMS mystream >
1) 1) "mystream"
   2) 1) 1) "1736318179999-0"
         2) 1) "field2"
            2) "value2"
```

### Setting ID to the Latest Entry

Set the last delivered ID for a consumer group to the latest stream entry:

```shell
dragonfly$>XGROUP CREATE mystream mygroup $ MKSTREAM
OK

dragonfly$> XADD mystream * field1 value1
"1736318170000-0"

dragonfly$> XADD mystream * field2 value2
"1736318179999-0"

# Set the last delivered ID to the latest entry in the stream.
dragonfly$> XGROUP SETID mystream mygroup $
OK

# Read a message from the stream using a consumer.
# Since there are no new messages, the consumer does not read any messages.
dragonfly$> XREADGROUP GROUP mygroup consumer-1 COUNT 1 STREAMS mystream >
(nil)
```

### Setting ID to the First Entry

Set the ID to the very first message in the stream in order to reprocess all messages:

```shell
dragonfly$> XGROUP CREATE mystream mygroup $ MKSTREAM
OK

dragonfly$> XADD mystream * field1 value1
"1736318170000-0"

dragonfly$> XADD mystream * field2 value2
"1736318179999-0"

# Set the last delivered ID to the first message in the stream.
dragonfly$> XGROUP SETID mystream mygroup 0
OK

# Read a message from the stream using a consumer.
# You can see that it starts to read from the very first message.
dragonfly$> XREADGROUP GROUP mygroup consumer-1 COUNT 1 STREAMS mystream >
1) 1) "mystream"
   2) 1) 1) "1736318170000-0"
         2) 1) "field1"
            2) "value1"
```

## Best Practices

- Use `XGROUP SETID` to manage backlogs and reprocess messages by adjusting the consumer group's last delivered ID.
- Exercise caution when setting the ID to an earlier value, as it can lead to message reprocessing and potential duplication.
- It is always crucial that **your application logic ensures idempotency when necessary**.

## Common Mistakes

- Not specifying the correct stream `key` or `group`, which can result in errors.

## FAQs

### What happens if the stream or consumer group does not exist?

If the stream or consumer group does not exist, `XGROUP SETID` will return an error.
Ensure that the group is created using [`XGROUP CREATE`](xgroup-create.md) before setting its ID.

### Can I use the `$` symbol with `XGROUP SETID`?

Yes, using `$` will set the last delivered ID to the latest entry in the stream, effectively catching up the consumer group to the most recent messages.
