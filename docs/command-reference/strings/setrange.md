---
description: Learn how to use Redis SETRANGE to overwrite part of a string at the specified key.
---

import PageTitle from '@site/src/components/PageTitle';

# SETRANGE

<PageTitle title="Redis SETRANGE Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `SETRANGE` command is used to overwrite part of a string starting at a specified offset with the given value.
It extends or truncates the string as needed, ensuring that the string is updated accordingly.
`SETRANGE` is especially valuable when you only need to update a subset of a string rather than replacing it entirely.

## Syntax

```shell
SETRANGE key offset value
```

- **Time complexity:** O(1), not counting the time taken to copy the new string in place. Usually, this string is very small so the amortized complexity is O(1). Otherwise, complexity is O(M) with M being the length of the value argument.
- **ACL categories:** @write, @string, @slow

## Parameter Explanations

- `key`: The key of the string to modify.
- `offset`: The zero-based index at which the modification should start.
- `value`: The substring that will replace bytes in the original string, starting from the specified offset.

## Return Values

The command returns the length of the string after it has been modified.

## Code Examples

### Basic Example

Overwrite part of a string at a specific offset:

```shell
dragonfly> SET mykey "Hello World"
OK
dragonfly> SETRANGE mykey 6 "Dragonfly"
(integer) 15

# Updated string: "Hello Dragonfly"
dragonfly> GET mykey
"Hello Dragonfly"
```

In this example, we replaced `"World"` starting at offset 6 with `"Dragonfly"`, and the new length of the string is 15.

### Expanding the String

If the `offset` is beyond the current length of the string, `SETRANGE` pads the string with null characters (`\x00`):

```shell
dragonfly> SET mykey "Hello"
OK
dragonfly> SETRANGE mykey 10 "Redis"
(integer) 15

# Updated string with padding: "Hello\x00\x00\x00\x00Redis"
dragonfly> GET mykey
"Hello\x00\x00\x00\x00Redis"
```

Note that the string is expanded with null bytes to accommodate the value `"Redis"` starting at offset 10, making the final string length 15.

### Overwriting Only Part of a String

You can choose to overwrite only a part of the original string, preserving the rest:

```shell
dragonfly> SET mykey "Dragonfly"
OK
dragonfly> SETRANGE mykey 0 "Fly"
(integer) 9

# Updated string: "Flygonfly"
dragonfly> GET mykey
"Flygonfly"
```

In this case, the first three characters `"Dra"` are replaced by `"Fly"`, leaving the rest of the string intact.

## Best Practices

- When working with large strings, use `SETRANGE` to efficiently update only the relevant bytes rather than resetting the entire string.
- Use `SETRANGE` for resource-efficient operations like modifying logs, altering specific fields in a custom protocol, or updating feature flags without reshuffling everything.

## Common Mistakes

- Using an `offset` larger than the existing string length without accounting for the fact that null characters will be introduced automatically.
- Assuming that `SETRANGE` modifies only the specified substring; it may affect string length, as `SETRANGE` pads or truncates the string to accommodate the new value.

## FAQs

### What happens if the key does not exist?

If the key does not exist, `SETRANGE` creates a new string filled with null characters up to the specified offset, before inserting the `value`.

### Can the `offset` parameter be negative?

No, the `offset` parameter must be a non-negative integer. If a negative value is provided, an error will result.
