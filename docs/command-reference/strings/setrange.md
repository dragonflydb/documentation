---
description: Learn how to use Redis SETRANGE to overwrite part of a string at the specified key.
---

import PageTitle from '@site/src/components/PageTitle';

# SETRANGE

<PageTitle title="Redis SETRANGE Explained (Better Than Official Docs)" />

## Introduction

The `SETRANGE` command in Redis is used to overwrite part of a string at a specified offset. It is particularly useful for modifying substrings within a larger string without replacing the entire value. This command ensures atomicity, so concurrent modifications will not interfere with each other.

## Syntax

```plaintext
SETRANGE key offset value
```

## Parameter Explanations

- **key**: The name of the string key where the substring will be modified.
- **offset**: An integer specifying the position within the string where the modification begins. Zero-based index.
- **value**: The substring that will overwrite the existing data starting from the specified offset.

## Return Values

- **Integer**: Returns the length of the string after the modification.

Example:

```cli
(integer) 11
```

## Code Examples

### Basic Example

Overwriting a substring in an existing string value.

```cli
dragonfly> SET mystring "Hello World"
OK
dragonfly> SETRANGE mystring 6 "Redis"
(integer) 11
dragonfly> GET mystring
"Hello Redis"
```

### Updating a Log Entry

Appending a timestamp to a log entry while preserving the initial part of the log.

```cli
dragonfly> SET logentry "User123 login at "
OK
dragonfly> SETRANGE logentry 16 "2024-07-26 12:34:56"
(integer) 35
dragonfly> GET logentry
"User123 login at 2024-07-26 12:34:56"
```

### Padding a String

Ensure a fixed-length record by padding spaces or other characters.

```cli
dragonfly> SET record "Name: John"
OK
dragonfly> SETRANGE record 10 "            Address: Unknown"
(integer) 40
dragonfly> GET record
"Name: John             Address: Unknown"
```

## Best Practices

- Ensure the offset does not exceed the current length of the string to avoid creating large gaps filled with null characters.
- Use `GETRANGE` to verify changes when working with critical strings.

## Common Mistakes

- Using a negative offset. Redis does not support negative offsets for `SETRANGE`.
- Expecting `SETRANGE` to work on non-string types. Ensure the key holds a string value.

## FAQs

### What happens if the offset is beyond the current length of the string?

If the offset is greater than the length of the string, Redis pads the intermediate space with null characters (represented as `\x00`).

### Can `SETRANGE` be used on keys of types other than string?

No, `SETRANGE` only works with string values. Attempting to use it on other types like lists, sets, or hashes will result in an error.
