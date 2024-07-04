---
description: Learn how to use Redis GETDEL to retrieve and delete a key’s value.
---

import PageTitle from '@site/src/components/PageTitle';

# GETDEL

<PageTitle title="Redis GETDEL Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`GETDEL` is a Redis command that retrieves the value of a key and deletes the key in one atomic operation. This command is useful in scenarios where you need to fetch a key's value and ensure that it no longer exists afterward, such as processing a task stored in Redis and guaranteeing it won't be processed again.

## Syntax

```cli
GETDEL key
```

## Parameter Explanations

- `key`: The key whose value you want to get and delete. It must be a string type.

## Return Values

- If the key exists, it returns the value stored at the key.
- If the key does not exist, it returns `nil`.

### Examples:

- Key exists:

  ```cli
  dragonfly> SET mykey "Hello"
  OK
  dragonfly> GETDEL mykey
  "Hello"
  ```

- Key does not exist:
  ```cli
  dragonfly> GETDEL nonexistkey
  (nil)
  ```

## Code Examples

```cli
dragonfly> SET task:123 "process this task"
OK
dragonfly> GETDEL task:123
"process this task"
dragonfly> GETDEL task:123
(nil)
```

## Best Practices

- Use `GETDEL` for tasks or data that should be accessed and removed atomically to avoid race conditions.
- Ensure that the application logic accounts for the possibility of the key being absent (`nil` response).

## Common Mistakes

- Using `GETDEL` on a key that might be needed later can lead to data loss since it deletes the key after retrieval.
- Not handling the potential `nil` return value can cause null reference errors in some applications.

## FAQs

### What happens if I use `GETDEL` on a non-existent key?

You'll receive a `nil` response, indicating that the key did not exist.

### Can I use `GETDEL` with keys of types other than strings?

No, `GETDEL` is designed to work with string keys only.
