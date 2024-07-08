---
description: Learn how to use Redis XGROUP CREATE to create a new consumer group.
---

import PageTitle from '@site/src/components/PageTitle';

# XGROUP CREATE

<PageTitle title="Redis XGROUP CREATE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`XGROUP CREATE` is a Redis command used to create a consumer group associated with a stream. The purpose of this command is to enable message consumption by multiple consumers from a single stream, ensuring that each message is processed only once by a single consumer within the group. Typical use cases include real-time data processing, task distribution, and event sourcing systems.

## Syntax

```plaintext
XGROUP CREATE <stream> <groupname> <id or $>
```

## Parameter Explanations

- `<stream>`: The name of the stream for which the consumer group will be created.
- `<groupname>`: The name of the consumer group to create.
- `<id or $>`: The ID from which the group should start reading messages. Use `$` to start from the latest entry in the stream or an explicit entry ID to start from a specific point.

## Return Values

- `OK`: If the consumer group was successfully created.
- An error message if the stream does not exist or the group already exists.

## Code Examples

```cli
dragonfly> XADD mystream * field1 value1
"1688519600365-0"
dragonfly> XGROUP CREATE mystream mygroup $
OK
dragonfly> XGROUP CREATE mystream mygroup $
(error) BUSYGROUP Consumer Group name already exists
dragonfly> XGROUP CREATE mystream newgroup 0
OK
```

## Common Mistakes

- Trying to create a consumer group on a non-existing stream results in an error.
- Attempting to create a consumer group with an existing name without handling the `BUSYGROUP` error.

## FAQs

### What should I do if the stream does not exist yet?

You can use the `MKSTREAM` option with commands like `XADD` to ensure the stream is created if it does not already exist.

### How do I delete a consumer group?

You can use the `XGROUP DESTROY <stream> <groupname>` command to delete a consumer group.
