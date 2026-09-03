---
description: "Learn to use the Dragonfly RM command to scan and delete keys matching a pattern."
---

import PageTitle from '@site/src/components/PageTitle';

# RM

<PageTitle title="Dragonfly RM Command (Documentation) | Dragonfly" />

## Syntax

    RM cursor [MATCH pattern] [TYPE type] [COUNT count]

**ACL categories:** @keyspace, @write, @slow, @dangerous

`RM` is a Dragonfly-specific command that combines the cursor-based iteration of `SCAN` with key deletion: it scans the keyspace and deletes every key it visits that matches the given filters, without requiring the caller to first collect and then delete the matching keys themselves.

This command is Dragonfly-specific.

## RM basic usage

Like `SCAN`, `RM` is a cursor-based iterator. Each call returns an updated cursor that must be passed to the next call to continue the operation. An iteration starts when the cursor is set to 0, and terminates when the cursor returned by the server is 0.

```shell
dragonfly> mset key:1 a key:2 b key:3 c
OK
dragonfly> rm 0 MATCH key:*
1) "0"
2) (integer) 3
dragonfly> exists key:1 key:2 key:3
(integer) 0
```

Unlike `SCAN`, the second element of the reply is not an array of matched elements, but an integer: the number of keys deleted during that call.

## The MATCH option

Similarly to `SCAN` and `KEYS`, `RM` accepts a `MATCH <pattern>` option to only delete keys matching a glob-style pattern. As with `SCAN`, the pattern is applied after keys are visited internally, so calls may delete zero keys even though matching keys still exist elsewhere in the keyspace.

## The TYPE option

The `TYPE` option restricts deletion to keys of a given type, using the same type names returned by the `TYPE` command.

```shell
dragonfly> set str:1 hello
OK
dragonfly> lpush list:1 a b c
(integer) 3
dragonfly> rm 0 TYPE string
1) "0"
2) (integer) 1
dragonfly> exists str:1
(integer) 0
dragonfly> exists list:1
(integer) 1
```

## The COUNT option

`COUNT` hints at the amount of work to perform per call, exactly as it does for `SCAN`. The default `COUNT` is 10. A single call is additionally bounded internally by a short wall-clock time budget, so a very large `COUNT` will not cause a single call to block for an unbounded amount of time; instead, the call returns early with a non-zero cursor to continue the operation on a subsequent call.

## Guarantees and caveats

`RM` inherits the same weak iteration guarantees as `SCAN`: a full iteration (from cursor 0 back to cursor 0) is guaranteed to visit every key that was present for the entire duration of the iteration, but keys added or removed mid-iteration may or may not be visited.

Because `RM` deletes as it scans, calling it repeatedly with the same filters until the cursor returns to 0 is the recommended way to remove all keys matching a pattern, similar in spirit to combining `SCAN` with `DEL`/`UNLINK`, but without the round trip of returning key names to the client first.

## Return value

`RM` returns a two-element array reply:

- The first element is a string representing an unsigned 64-bit number (the cursor).
- The second element is an [integer reply](https://valkey.io/topics/protocol/#integers): the number of keys deleted during this call.

## Additional examples

```shell
dragonfly> mset a:1 1 a:2 2 b:1 1
OK
dragonfly> rm 0 MATCH a:* COUNT 100
1) "0"
2) (integer) 2
dragonfly> keys *
1) "b:1"
```
