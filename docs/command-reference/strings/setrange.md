---
description: Overwrite part of a string at key starting at the specified offset
---

# SETRANGE

## Syntax

    SETRANGE key offset value

**Time complexity:** O(1), not counting the time taken to copy the new string in place. Usually, this string is very small so the amortized complexity is O(1). Otherwise, complexity is O(M) with M being the length of the value argument.

**ACL categories:** @write, @string, @slow

Overwrites part of the string stored at _key_, starting at the specified offset,
for the entire length of _value_.
If the offset is larger than the current length of the string at _key_, the
string is padded with zero-bytes to make _offset_ fit.
Non-existing keys are considered as empty strings, so this command will make
sure it holds a string large enough to be able to set _value_ at _offset_.

**Warning**: When setting the last possible byte (with large _offset_), and the string value stored at _key_ does not holds a value (or holds a small string), the operation will take some time, as Dragonfly is required to allocate all memory leading to that bit. Subsequent calls will not have the performance penalty.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers): the length of the string after it was modified by the command.

## Patterns

Thanks to `SETRANGE` and the analogous `GETRANGE` commands, you can use Redis
strings as a linear array with O(1) random access.
This is a very fast and efficient storage in many real world use cases.


## Examples

Basic usage:

```shell
dragonfly> SET key1 "Hello World"
"OK"
dragonfly> SETRANGE key1 6 "Dragonfly"
(integer) 15
dragonfly> GET key1
"Hello Dragonfly"
```

Example of zero padding:

```shell
dragonfly> SETRANGE key2 6 "Dragonfly"
(integer) 15
dragonfly> GET key2
"\x00\x00\x00\x00\x00\x00Dragonfly
```

where `\x00`  stands for the NUL character, inserted by the zero padding.
