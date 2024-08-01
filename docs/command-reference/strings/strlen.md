---
description: Learn how to use Redis STRLEN to get the length of the string stored in a key.
---

import PageTitle from '@site/src/components/PageTitle';

# STRLEN

<PageTitle title="Redis STRLEN Explained (Better Than Official Docs)" />

## Introduction

The `STRLEN` command in Redis is used to get the length of the value stored at a specified key. This command is particularly useful for verifying the size of string data, which can help in managing memory and optimizing performance.

## Syntax

```plaintext
STRLEN key
```

## Parameter Explanations

- **key**: The key whose value's length you want to retrieve. The key must be associated with a string value.

## Return Values

- Returns the length of the string at the given key.
- If the key does not exist, it returns 0.
- If the key holds a non-string value, an error is returned.

## Code Examples

### Basic Example

Check the length of a simple string stored at a key:

```cli
dragonfly> SET mykey "Hello, Redis!"
OK
dragonfly> STRLEN mykey
(integer) 13
```

### Length of a Non-Existent Key

Attempting to get the length of a non-existent key returns 0:

```cli
dragonfly> STRLEN nonExistentKey
(integer) 0
```

### Handling Binary Data

Storing binary data and checking its length:

```cli
dragonfly> SET binaryKey "\x00\x01\x02\x03"
OK
dragonfly> STRLEN binaryKey
(integer) 4
```

### Error on Non-String Value

Trying to use `STRLEN` on a key holding a non-string value results in an error:

```cli
dragonfly> LPUSH mylist "item1"
(integer) 1
dragonfly> STRLEN mylist
(error) WRONGTYPE Operation against a key holding the wrong kind of value
```

## Best Practices

- Ensure the key holds a string value before using `STRLEN` to avoid errors.
- Use `STRLEN` for quick checks on data size instead of retrieving and measuring in client code, which saves bandwidth.

## Common Mistakes

- Using `STRLEN` on keys with non-string values will result in an error.
- Forgetting that `STRLEN` on a non-existent key returns 0, which might be misinterpreted as the key having an empty string.

## FAQs

### What happens if I use STRLEN on a key that does not exist?

`STRLEN` will return 0 if the key does not exist.

### Can I use STRLEN on keys with list or set data types?

No, `STRLEN` can only be used on keys storing string values. Using it on other data types will result in an error.

### Does STRLEN count binary characters?

Yes, `STRLEN` counts all characters, including binary characters.
