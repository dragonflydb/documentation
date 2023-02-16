---
description: Return the current server time
---

# TIME

## Syntax

    TIME 

**Time complexity:** O(1)

The `TIME` command returns the current server time as a two items lists: a Unix
timestamp and the amount of microseconds already elapsed in the current second.
Basically the interface is very similar to the one of the `gettimeofday` system
call.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays), specifically:

A multi bulk reply containing two elements:

* unix time in seconds.
* microseconds.

## Examples

```cli
TIME
TIME
```
