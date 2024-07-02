---
description: Learn how to use the Redis BZPOPMAX command to remove and return the highest score member from sorted sets, plus expert tips beyond the official Redis docs.
---

import PageTitle from '@site/src/components/PageTitle';

# BZPOPMAX

<PageTitle title="Redis BZPOPMAX Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `BZPOPMAX` command is used in Redis to remove and return the member with the highest score from one or more sorted sets. If the sorted sets are empty, it can block the connection until a member becomes available. This command is useful in scenarios where you need to process elements in order of their priority, such as task queues that handle tasks with varying importance.

## Syntax

```plaintext
BZPOPMAX key [key ...] timeout
```

## Parameter Explanations

- **key**: One or more sorted set keys from which the highest scoring member will be popped.
- **timeout**: The maximum number of seconds the client will block if no members are available. A timeout of 0 means to block indefinitely.

## Return Values

The command returns an array with three elements:

1. The name of the key where the member was popped.
2. The member itself.
3. The score of the member.

If the timeout is reached without a member becoming available, it returns a `nil`.

### Example Outputs

- When an element is successfully popped:
  ```plaintext
  1) "myzset"
  2) "one"
  3) "1"
  ```
- When the timeout is reached without any members becoming available:
  ```plaintext
  (nil)
  ```

## Code Examples

```cli
dragonfly> ZADD myzset1 1 "one" 2 "two" 3 "three"
(integer) 3
dragonfly> ZADD myzset2 4 "four" 5 "five"
(integer) 2
dragonfly> BZPOPMAX myzset1 myzset2 1
1) "myzset2"
2) "five"
3) "5"
dragonfly> BZPOPMAX myzset1 myzset2 1
1) "myzset2"
2) "four"
3) "4"
dragonfly> BZPOPMAX myzset1 myzset2 1
1) "myzset1"
2) "three"
3) "3"
dragonfly> BZPOPMAX myzset1 myzset2 1
(nil)
```

## Best Practices

- Ensure timeout values are carefully chosen based on your application's real-time requirements to avoid unnecessary blocking.
- Always provide multiple keys when possible to increase the chances of immediate availability of members.

## Common Mistakes

- Using a very short timeout might cause the command to frequently return `nil`, which may not be desirable for certain applications.
- Not handling the `nil` response properly, which could lead to unexpected application behavior.

## FAQs

### What happens if all specified keys are empty?

If all specified keys are empty and the timeout expires, the command returns `nil`.

### Can `BZPOPMAX` be used with only one key?

Yes, `BZPOPMAX` can be used with a single key, but specifying multiple keys increases the chances of the operation succeeding without blocking.

### Is there a non-blocking version of this command?

Yes, the non-blocking version of this command is `ZPOPMAX`.
