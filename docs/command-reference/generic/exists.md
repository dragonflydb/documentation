---
description: "Learn how Redis EXISTS command checks if a key exists."
---

import PageTitle from '@site/src/components/PageTitle';

# EXISTS

<PageTitle title="Redis EXISTS Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `EXISTS` command in Redis is used to determine if one or more keys exist in the database. This command is commonly used to check the presence of keys before performing operations that depend on their existence, such as conditional updates or deletions.

## Syntax

```plaintext
EXISTS key [key ...]
```

## Parameter Explanations

- **key**: One or more keys for which the existence needs to be checked. Multiple keys can be provided separated by spaces.

## Return Values

The command returns an integer representing the number of keys that exist among the ones specified.

Example outputs:

- `(integer) 0`: None of the specified keys exist.
- `(integer) 1`: One of the specified keys exists.
- `(integer) N`: N keys exist among the specified keys.

## Code Examples

```cli
dragonfly> SET key1 "value1"
OK
dragonfly> EXISTS key1
(integer) 1
dragonfly> EXISTS key2
(integer) 0
dragonfly> EXISTS key1 key2 key3
(integer) 1
dragonfly> SET key2 "value2"
OK
dragonfly> EXISTS key1 key2 key3
(integer) 2
```

## Best Practices

- Combine `EXISTS` with other commands to implement logic that depends on the presence or absence of keys.
- When checking multiple keys, understand that using `EXISTS` will return the count of existing keys which can be efficiently used to manage resources or make decisions.

## Common Mistakes

- Providing no keys. The command requires at least one key.
- Misunderstanding the return value. The command returns the count of existing keys, not a boolean indicating if all specified keys exist.

## FAQs

### What happens if I check for the same key multiple times in the `EXISTS` command?

Each occurrence of the key is counted separately. For instance, `EXISTS key1 key1 key2` will return 2 if `key1` exists, regardless of whether `key2` exists or not.

### Can `EXISTS` check for pattern-matching keys like with wildcards?

No, `EXISTS` checks for the exact keys specified. To match patterns, consider using the `KEYS` command.
