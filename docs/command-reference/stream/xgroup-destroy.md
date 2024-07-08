---
description: Learn how to use Redis XGROUP DESTROY to remove a consumer group.
---

import PageTitle from '@site/src/components/PageTitle';

# XGROUP DESTROY

<PageTitle title="Redis XGROUP DESTROY Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `XGROUP DESTROY` command is used in Redis to delete a consumer group from a specific stream. This is particularly useful when you want to clean up or reconfigure your stream processing setup by removing outdated or unused consumer groups.

## Syntax

```plaintext
XGROUP DESTROY <key> <groupname>
```

## Parameter Explanations

- `<key>`: The name of the stream key from which the consumer group will be deleted.
- `<groupname>`: The name of the consumer group to be destroyed.

## Return Values

- `(integer) 1`: Indicates that the consumer group was successfully deleted.
- `(integer) 0`: Indicates that the consumer group did not exist.

## Code Examples

```cli
dragonfly> XGROUP CREATE mystream mygroup $ MKSTREAM
OK
dragonfly> XGROUP DESTROY mystream mygroup
(integer) 1
dragonfly> XGROUP DESTROY mystream nonexistinggroup
(integer) 0
```

## Best Practices

- Always ensure that the consumer group you intend to delete is no longer needed, as this action cannot be undone.
- It’s good practice to check if the consumer group exists before attempting to delete it to avoid unnecessary commands.

## Common Mistakes

- Trying to delete a consumer group from a non-existent stream will result in an error.
- Misspelling the stream key or group name can lead to unexpected results.

## FAQs

### What happens if I try to delete a consumer group that doesn't exist?

You will receive a return value of `(integer) 0`, indicating that the consumer group does not exist.

### Can I recreate a consumer group after deleting it?

Yes, you can use the `XGROUP CREATE` command to create a new consumer group with the same name after deletion.
