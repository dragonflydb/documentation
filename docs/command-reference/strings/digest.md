---
description: Learn how to use Redis DIGEST command to compute hash digest of string values.
---

import PageTitle from '@site/src/components/PageTitle';

# DIGEST

<PageTitle title="Redis DIGEST Command (Documentation) | Dragonfly" />

## Introduction

The `DIGEST` command returns a hash digest for the value stored at a specified key.
It uses the XXH3 hashing algorithm to compute a 64-bit hash and returns it as a 16-character hexadecimal string.
This command is useful for comparing values without transferring the full content, implementing checksums, or detecting changes.

**Availability:** Dragonfly v1.37.0 and later.

## Syntax

```shell
DIGEST key
```

**Time complexity:** O(N) where N is the length of the string value

**ACL categories:** @read, @string, @fast

## Parameter Explanations

- `key`: The key whose value should be hashed. Must be a string type.

## Return Values

- Returns a 16-character hexadecimal string representing the XXH3 64-bit hash of the value.
- Returns `nil` if the key does not exist.
- Returns an error if the key exists but holds a non-string value type.

## Code Examples

### Basic Example

Compute digest of a string value:

```shell
dragonfly$> SET mykey "Hello, Dragonfly!"
OK
dragonfly$> DIGEST mykey
"063b4909128e92b7"
```

### Non-Existent Key

If the key does not exist, `DIGEST` returns `nil`:

```shell
dragonfly$> DIGEST non_existent_key
(nil)
```

### Digest Consistency

The same value always produces the same digest:

```shell
dragonfly$> SET key1 "test"
OK
dragonfly$> SET key2 "test"
OK
dragonfly$> DIGEST key1
"9ec9f7918d7dfc40"
dragonfly$> DIGEST key2
"9ec9f7918d7dfc40"
```

### Different Values Produce Different Digests

```shell
dragonfly$> SET key1 "hello"
OK
dragonfly$> SET key2 "world"
OK
dragonfly$> DIGEST key1
"9555e8555c62dcfd"
dragonfly$> DIGEST key2
"d6476c25083d69be"
```

### Error on Wrong Type

```shell
dragonfly$> LPUSH mylist "item"
(integer) 1
dragonfly$> DIGEST mylist
(error) WRONGTYPE Operation against a key holding the wrong kind of value
```

## Best Practices

- Use `DIGEST` to compare values efficiently without transferring full content over the network.
- Implement change detection mechanisms by storing and comparing digests.
- Use with [`DELEX`](../generic/delex.md) `IFDEQ`/`IFDNE` for conditional deletions based on digest matching.

## Common Mistakes

- Attempting to use `DIGEST` on non-string keys will result in a `WRONGTYPE` error.
- Assuming different values might produce the same digest (hash collisions are extremely rare with XXH3).

## FAQs

### What hashing algorithm does DIGEST use?

`DIGEST` uses the XXH3 algorithm, which is a fast, non-cryptographic hash function that produces a 64-bit hash value.

### Is DIGEST suitable for cryptographic purposes?

No, `DIGEST` uses XXH3 which is not a cryptographic hash function. For cryptographic purposes, use dedicated cryptographic hash functions.

### Can DIGEST work with compressed or integer-encoded strings?

Yes, `DIGEST` handles all string encodings including raw strings, integer-encoded strings, and compressed strings.
