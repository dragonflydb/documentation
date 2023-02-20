---
description: Set the string value of a key and return its old value
---

# GETSET

## Syntax

    GETSET key value

**Time complexity:** O(1)

Atomically sets `key` to `value` and returns the old value stored at `key`.
Returns an error when `key` exists but does not hold a string value.  Any 
previous time to live associated with the key is discarded on successful 
`SET` operation.

## Design pattern

`GETSET` can be used together with `INCR` for counting with atomic reset.
For example: a process may call `INCR` against the key `mycounter` every time
some event occurs, but from time to time we need to get the value of the counter
and reset it to zero atomically.
This can be done using `GETSET mycounter "0"`:

```shell
dragonfly> INCR mycounter
(integer) 1
dragonfly> GETSET mycounter "0"
"1"
dragonfly> GET mycounter
"0"
```

## Return

[Bulk string reply](https://redis.io/docs/reference/protocol-spec#resp-bulk-strings): the old value stored at `key`, or `nil` when `key` did not exist.

## Examples

```shell
dragonfly> SET mykey "Hello"
"OK"
dragonfly> GETSET mykey "World"
"Hello"
dragonfly> GET mykey
"World"
```
