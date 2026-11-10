---
description: Learn to use the Dragonfly PREPEND command to add a value to the beginning of the string stored at a key.
---

import PageTitle from '@site/src/components/PageTitle';

# PREPEND

<PageTitle title="Dragonfly PREPEND Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, the `PREPEND` command adds a value to the beginning of the string stored at a key.
It is the counterpart of [`APPEND`](./append.md), which adds the value to the end.
If the key does not exist, `PREPEND` creates it with the given value.

This command is Dragonfly-specific: Valkey and Redis have no `PREPEND` command.

## Syntax

```shell
PREPEND key value
```

- **Time complexity:** O(N) where N is the length of the resulting string, because Dragonfly copies the existing value on every call.
- **ACL categories:** @fast, @string, @write

## Parameter Explanations

- `key`: The key of the string to prepend to.
  If the key does not exist, it is created. If it exists, it must hold a string.
- `value`: The string to add before the current value.

## Return Values

- [Integer reply](https://valkey.io/topics/protocol/#integers): the length of the string **after** the prepend operation.

## Code Examples

### Basic Example

Prepending a value to an existing key:

```shell
dragonfly> SET greeting world
OK
dragonfly> PREPEND greeting "hello "
(integer) 11
dragonfly> GET greeting
"hello world"
```

### Missing Key

If the key does not exist, `PREPEND` creates it:

```shell
dragonfly> PREPEND newkey abc
(integer) 3
dragonfly> GET newkey
"abc"
```

### Building a Path

Adding parent directories in front of a file name:

```shell
dragonfly> SET path report.txt
OK
dragonfly> PREPEND path 2026/
(integer) 15
dragonfly> PREPEND path /archive/
(integer) 24
dragonfly> GET path
"/archive/2026/report.txt"
```

## Best Practices

- Ensure that the key holds a string, or does not exist yet, to avoid errors.
- Every call copies the whole value, so building a large string from many small `PREPEND` calls is expensive. Assemble it in the client and write it with one `SET` when you can.

## Common Mistakes

Prepending to a key that holds a non-string value returns an error:

```shell
dragonfly> RPUSH mylist item
(integer) 1
dragonfly> PREPEND mylist text
(error) WRONGTYPE Operation against a key holding the wrong kind of value
```

## FAQs

### What happens if the key does not exist?

`PREPEND` creates the key with the given value and returns its length.
This happens even when the value is an empty string: the key is then created with an empty value and the reply is `0`.

### Is `PREPEND` related to the Memcached `prepend` command?

Yes. In [Memcached mode](../../managing-dragonfly/memcached-mode.md), Dragonfly executes the Memcached `prepend` command through `PREPEND`, but with Memcached semantics:
on a missing key, Memcached `prepend` replies `NOT_STORED` and does not create the key.
