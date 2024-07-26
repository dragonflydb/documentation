---
description: Learn how to use Redis GETDEL to retrieve and delete a key’s value.
---

import PageTitle from '@site/src/components/PageTitle';

# GETDEL

<PageTitle title="Redis GETDEL Explained (Better Than Official Docs)" />

## Introduction

The `GETDEL` command in Redis retrieves the value of a specified key and then deletes the key. This atomic operation is useful for scenarios where you need to read and immediately remove a key, ensuring no other operations intervene between the get and delete actions.

## Syntax

```plaintext
GETDEL key
```

## Parameter Explanations

- **key**: The key whose value needs to be retrieved and deleted. It must be a string type key.

## Return Values

- If the key exists: returns the value of the key.
- If the key does not exist: returns `nil`.

## Code Examples

### Basic Example

```cli
dragonfly> SET mykey "Hello"
OK
dragonfly> GETDEL mykey
"Hello"
dragonfly> GET mykey
(nil)
```

### Session Handling

Using `GETDEL` to retrieve and delete session data after processing.

```cli
dragonfly> SET session:user123 '{"user_id":123, "name":"John Doe"}'
OK
dragonfly> GETDEL session:user123
"{\"user_id\":123, \"name\":\"John Doe\"}"
dragonfly> GET session:user123
(nil)
```

### One-time Access Token Retrieval

Generate one-time access tokens that are invalidated after being read.

```cli
dragonfly> SET onetime:token "secret-data"
OK
dragonfly> GETDEL onetime:token
"secret-data"
dragonfly> GET onetime:token
(nil)
```

### Processing Temporary Data

Reading and deleting temporary status updates for real-time applications.

```cli
dragonfly> SET temp:status "processing"
OK
dragonfly> GETDEL temp:status
"processing"
dragonfly> GET temp:status
(nil)
```

## Best Practices

- Use `GETDEL` when atomicity is crucial. This prevents race conditions where multiple clients may read or delete the same key simultaneously.
- Ensure keys accessed with `GETDEL` are meant to be transient since their deletion is irreversible.

## Common Mistakes

- Using `GETDEL` on non-existent keys without handling the `nil` response can lead to application errors.
- Misunderstanding the atomicity of `GETDEL` might lead to incorrect assumptions about the state of the key at different points in time.

## FAQs

### How is `GETDEL` different from running `GET` followed by `DEL`?

`GETDEL` is atomic, meaning it guarantees no other commands can intervene between the get and delete operations. Running `GET` followed by `DEL` separately does not offer this guarantee and could lead to race conditions.

### What happens if the key doesn't exist?

If the key does not exist, `GETDEL` returns `nil`.
