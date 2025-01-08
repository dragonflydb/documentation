---
description:  Learn how to use Redis XGROUP SETID to set the last delivered ID of a stream.
---

import PageTitle from '@site/src/components/PageTitle';

# XGROUP SETID

<PageTitle title="Redis XGROUP SETID Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `XGROUP SETID` command is used to change the last delivered ID for a consumer group in a stream.
This command is beneficial when you need to reprocess messages or adjust a consumer group's position in the stream.

## Syntax

```shell
XGROUP SETID <key> <groupname> <id>
```

## Parameter Explanations

- `key`: The key of the stream.
- `groupname`: The name of the consumer group whose last delivered ID is to be set.
- `id`: The ID you want the consumer group to consider as the last delivered ID. You can specify a specific ID or use `$` to set it to the last entry in the stream.

## Return Values

The command returns `OK` if the operation is successful or an error message if it fails.

## Code Examples

### Basic Example

Change the last delivered ID for a consumer group:

```shell

dragonfly$> XGROUP CREATE mystream mygroup $ MKSTREAM
OK
dragonfly$> XADD mystream * field1 value1
"1633022829740-0"
dragonfly$> XGROUP SETID mystream mygroup 1633022829740-0
OK
```

### Setting ID to the Latest Entry

Set the last delivered ID for a consumer group to the latest stream entry:

```shell

dragonfly$> XADD mystream * field2 value2
"1633022830751-0"
dragonfly$> XGROUP SETID mystream mygroup $
OK
```

### Adjusting to an Earlier ID

Adjust the last delivered ID to an earlier entry to reprocess messages:

```shell

dragonfly$> XADD mystream * field3 value3
"1633022831762-0"
dragonfly$> XGROUP SETID mystream mygroup 1633022829740-0
OK
```

## Best Practices

- Use `XGROUP SETID` to manage backlogs and reprocess messages by adjusting the consumer group's last delivered ID.
- Exercise caution when setting the ID to an earlier value, as it can lead to message reprocessing and potential duplication.

## Common Mistakes

- Not specifying the correct stream `key` or `groupname`, which can result in errors.
- Using an invalid `id` that doesn't exist in the stream, which will prevent the consumer group from functioning correctly.

## FAQs

### What happens if the consumer group does not exist?

If the consumer group does not exist, `XGROUP SETID` will return an error.
Ensure that the group is created using `XGROUP CREATE` before setting its ID.

### Can I use the `$` symbol with `XGROUP SETID`?

Yes, using `$` will set the last delivered ID to the latest entry in the stream, effectively catching up the consumer group to the most recent messages.