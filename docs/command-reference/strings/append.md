---
description: Learn to extend a string value in Redis using the APPEND command.
---

import PageTitle from '@site/src/components/PageTitle';

# APPEND

<PageTitle title="Redis APPEND Explained (Better Than Official Docs)" />

## Introduction

The `APPEND` command in Redis is used to add a specified value to the end of a string stored at a given key. If the key doesn't exist, it creates it and initializes it with an empty string before appending. This command is particularly useful for accumulating logs or constructing strings incrementally.

## Syntax

```cli
APPEND key value
```

## Parameter Explanations

- `key`: The key of the string you wish to append to. It should already exist as a string type, or it will be created as a new string.
- `value`: The string value to append to the existing string at the key.

## Return Values

- An integer indicating the length of the string after the append operation.

### Example Outputs

- `(integer) 11` when the resulting string length is 11.

## Code Examples

### Basic Example

Appending a value to an existing key:

```cli
dragonfly> SET mystring "Hello"
OK
dragonfly> APPEND mystring " World"
(integer) 11
dragonfly> GET mystring
"Hello World"
```

### Logging Use Case

Accumulating log entries for a simple logging mechanism:

```cli
dragonfly> APPEND log "2023-07-26 10:00:00 - User login\n"
(integer) 33
dragonfly> APPEND log "2023-07-26 10:05:00 - User logout\n"
(integer) 66
dragonfly> GET log
"2023-07-26 10:00:00 - User login\n2023-07-26 10:05:00 - User logout\n"
```

### Incremental Data Construction

Building a configuration file or script incrementally:

```cli
dragonfly> APPEND config "server {\n"
(integer) 9
dragonfly> APPEND config "  listen 80;\n"
(integer) 22
dragonfly> APPEND config "}\n"
(integer) 24
dragonfly> GET config
"server {\n  listen 80;\n}\n"
```

## Best Practices

- Ensure that the key being appended to is of string type to avoid errors.
- Use `APPEND` for operations where string concatenation is frequent but data volume is manageable.

## Common Mistakes

- Appending to a key that holds a non-string value can result in an error. Always ensure the data type compatibility.
  ```cli
  dragonfly> LPUSH mylist "item"
  (integer) 1
  dragonfly> APPEND mylist "string"
  (error) WRONGTYPE Operation against a key holding the wrong kind of value
  ```

## FAQs

### What happens if the key does not exist?

If the key does not exist, `APPEND` will create it as an empty string and then append the provided value.

### Can I use `APPEND` with non-string keys?

No, `APPEND` only works with keys that hold string values. Attempting to use it with other data types will result in an error.
