---
description: Remove and get the first element in a list, or block until one is available
---

# BLPOP

## Syntax

    BLPOP key [key ...] timeout

**Time complexity:** O(N) where N is the number of provided keys.

`BLPOP` is a blocking list pop primitive.
It is the blocking version of `LPOP` because it blocks the connection when there
are no elements to pop from any of the given lists.
An element is popped from the head of the first list that is non-empty, with the
given keys being checked in the order that they are given.

**Note** that the unblock order can differ from the one used by Redis. See [below](#what-key-is-served-first-what-client-what-element-priority-ordering-details) for more details.

## Non-blocking behavior

When `BLPOP` is called, if at least one of the specified keys contains a
non-empty list, an element is popped from the head of the list and returned to
the caller together with the `key` it was popped from.

Keys are checked in the order that they are given.
Let's say that the key `list1` doesn't exist and `list2` and `list3` hold
non-empty lists.
Consider the following command:

```
BLPOP list1 list2 list3 0
```

`BLPOP` guarantees to return an element from the list stored at `list2` (since
it is the first non empty list when checking `list1`, `list2` and `list3` in
that order).

## Blocking behavior

If none of the specified keys exist, `BLPOP` blocks the connection until another
client performs an `LPUSH` or `RPUSH` operation against one of the keys.

Once new data is present on one of the lists, the client returns with the name
of the key unblocking it and the popped value.

When `BLPOP` causes a client to block and a non-zero timeout is specified,
the client will unblock returning a `nil` multi-bulk value when the specified
timeout has expired without a push operation against at least one of the
specified keys.

**The timeout argument is interpreted as a double value specifying the maximum number of seconds to block**.
A timeout of zero can be used to block indefinitely.

## What key is served first? What client? What element? Priority ordering details.

* If the client tries to block on mulitiple keys, but at least one key is not empty, the result is taken from the first key from left to right that has one or more elements. In this case the client is not blocked. For example, the command `BLPOP key1 key2 key3 key4 0`, assuming that both `key2` and `key4` are non-empty, will always return an element from `key2`.

* If multiple clients are blocked for the same key, the first client to be served is the one that was waiting the longest (the first that blocked for the key). Once a client is unblocked, it does not retain any priority when it blocks again with the next call to `BLPOP`. It will be served accordingly to the number of clients already blocked for the same key.

* If a client is blocked on multiple keys, it will unblock on the key that first recevied a push operation. If multiple push operations on different keys happened within a single `MULTI`/`EXEC` transaction or a single script invocation, then the resulting key, in the general case, is not determined.

## Behavior of `BLPOP` when multiple elements are pushed inside a list.

Its possible for a single command to add multiple elements to a single list:

* Variadic push operations such as `LPUSH mylist a b c`.
* After an `EXEC` of a `MULTI` block with multiple push operations against the same list.
* Executing a Lua Script with multiple push operations against the same list.

If a command performing multiple pushes is executed, *only after* the execution of the command,
the blocked clients are served. Consider this sequence of commands.

    Client A:   BLPOP foo 0
    Client B:   LPUSH foo a b c

Client **A** will be served with the `c` element, because after the `LPUSH` command the list contains `c,b,a`, so taking an element from the left means to return `c`.

Note that for the same reason a Lua script or a `MULTI/EXEC` block may push elements into a list and afterward **delete the list**. In this case the blocked clients will not be served at all and will continue to be blocked as long as no data is present on the list after the execution of a single command, transaction, or script.

## Behavior of `BLPOP` when elements are pushed inside `MULTI`/`EXEC` transactions or scripts

Dragonfly can potentially parallelize the execution of a single `MULTI`/`EXEC` transaction or script, which makes it impossible to determine what key will receive a new elemenet first. Because of this, `BLPOP` can return an element from any of the listed keys that have become non-empty after the last `MULTI`/`EXEC` transaction or script.

To disable parallel execution, `multi_exec_squash=false` and `lua_auto_async=false` flags should be used. This will make `BLPOP` return an element from the first key that 
received a new element.

For example, let's assume a client is blocked on `BLPOP c b a` and the following sequence of commands is run:

```
MULTI
LPUSH a 1
LPUSH b 2
LPUSH c 3
EXEC
```

By default, BLPOP can return any element. If parallel execution is disabled, it's guaranteed to return `a 1`.

## `BLPOP` inside a `MULTI` / `EXEC` transaction

`BLPOP` can be used with pipelining (sending multiple commands and
reading the replies in batch), however this setup makes sense almost solely
when it is the last command of the pipeline.

Using `BLPOP` inside a `MULTI` / `EXEC` block does not make a lot of sense
as it would require blocking the entire server in order to execute the block
atomically, which in turn does not allow other clients to perform a push
operation. For this reason the behavior of `BLPOP` inside `MULTI` / `EXEC` when the list is empty is to return a `nil` multi-bulk reply, which is the same
thing that happens when the timeout is reached.

If you like science fiction, think of time flowing at infinite speed inside a
`MULTI` / `EXEC` block...

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays): specifically:

* A `nil` multi-bulk when no element could be popped and the timeout expired.
* A two-element multi-bulk with the first element being the name of the key
  where an element was popped and the second element being the value of the
  popped element.

## Examples

```shell
dragonfly> DEL list1 list2
(integer) 0
dragonfly> RPUSH list1 a b c
(integer) 3
dragonfly> BLPOP list1 list2 0
1) "list1"
2) "a"
```

## Reliable queues

When `BLPOP` returns an element to the client, it also removes the element from the list. This means that the element only exists in the context of the client: if the client crashes while processing the returned element, it is lost forever.

This can be a problem with some application where we want a more reliable messaging system. When this is the case, please check the `BRPOPLPUSH` command, that is a variant of `BLPOP` that adds the returned element to a target list before returning it to the client.

## Pattern: Event notification

Using blocking list operations it is possible to mount different blocking
primitives.
For instance for some application you may need to block waiting for elements
into a Set, so that as far as a new element is added to the Set, it is
possible to retrieve it without resort to polling.
This would require a blocking version of `SPOP` that is not available, but using
blocking list operations we can easily accomplish this task.

The consumer will do:

```
LOOP forever
    WHILE SPOP(key) returns elements
        ... process elements ...
    END
    BRPOP helper_key
END
```

While in the producer side we'll use simply:

```
MULTI
SADD key element
LPUSH helper_key x
EXEC
```
