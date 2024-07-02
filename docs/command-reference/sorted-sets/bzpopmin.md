---
description: Learn to use the Redis BZPOPMIN command to remove and return the smallest score member from sorted sets, plus expert tips beyond the official doRedis docscs.
---

import PageTitle from '@site/src/components/PageTitle';

# BZPOPMIN

<PageTitle title="Redis BZPOPMIN Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`BZPOPMIN` is a blocking variant of the `ZPOPMIN` command in Redis. It removes and returns the member with the smallest score from one or more sorted sets, blocking until one is available if none exist. This command is typically used in scenarios where you need to wait for an element to appear in a sorted set, often for implementing priority queues.

## Syntax

```plaintext
BZPOPMIN key [key ...] timeout
```

## Parameter Explanations

- **key [key ...]**: One or more keys representing the sorted sets from which to pop the minimum element. The command will check these keys in the order they are listed.
- **timeout**: A non-negative integer specifying the maximum number of seconds to block. A timeout of zero can be used to block indefinitely.

## Return Values

The command returns either:

- An array of three elements: the name of the key from which the element was popped, the popped element, and its score.
- `nil` if the timeout is reached without any element being popped.

Examples of possible outputs:

- If an element is successfully popped: `1) "myzset"\n2) "one"\n3) "1"`
- If the timeout is reached: `(nil)`

## Code Examples

```cli
dragonfly> ZADD myzset 1 "one"
(integer) 1
dragonfly> ZADD myzset 2 "two"
(integer) 1
dragonfly> BZPOPMIN myzset 0
1) "myzset"
2) "one"
3) "1"

# If the sorted set is empty and we want to wait (with a timeout of 5 seconds)
dragonfly> BZPOPMIN myzset 5
(nil)
```

## Best Practices

- Ensure that the blocking timeout is appropriate for your application's performance requirements to avoid unnecessary delays.
- Use `BZPOPMIN` when you need to wait for new elements dynamically rather than busy-waiting or polling the sorted set continuously.

## Common Mistakes

- Using a very short timeout without understanding that it may lead to frequent timeout occurrences, thus failing to retrieve elements effectively.
- Blocking indefinitely (`timeout = 0`) without considering potential deadlocks or the overall responsiveness of your application.

## FAQs

### What happens if multiple clients issue `BZPOPMIN` on the same key?

When multiple clients block on the same key, only one client will receive the element when it becomes available. Other clients will continue to block until there is another element to pop.

### Can I use `BZPOPMIN` with multiple keys?

Yes, `BZPOPMIN` supports multiple keys. It will return the first available element from the first non-empty sorted set in the order the keys are specified.
