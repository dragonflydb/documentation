---
description:  Learn to use Redis RPOPLPUSH to shift elements between two lists and provide basic queueing.
---
import PageTitle from '@site/src/components/PageTitle';

# RPOPLPUSH

<PageTitle title="Redis RPOPLPUSH Command (Documentation) | Dragonfly" />

## Syntax

    RPOPLPUSH source destination

**Time complexity:** O(1)

**ACL categories:** @write, @list, @slow

Atomically returns and removes the last element (tail) of the list stored at
`source`, and pushes the element at the first element (head) of the list stored
at `destination`.

For example: consider `source` holding the list `a,b,c`, and `destination`
holding the list `x,y,z`.
Executing `RPOPLPUSH` results in `source` holding `a,b` and `destination`
holding `c,x,y,z`.

If `source` does not exist, the value `nil` is returned and no operation is
performed.
If `source` and `destination` are the same, the operation is equivalent to
removing the last element from the list and pushing it as first element of the
list, so it can be considered as a list rotation command.

## Return

[Bulk string reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#bulk-strings): the element being popped and pushed.

## Examples

```shell
dragonfly> RPUSH mylist "one"
(integer) 1
dragonfly> RPUSH mylist "two"
(integer) 2
dragonfly> RPUSH mylist "three"
(integer) 3
dragonfly> RPOPLPUSH mylist myotherlist
"three"
dragonfly> LRANGE mylist 0 -1
1) "one"
2) "two"
dragonfly> LRANGE myotherlist 0 -1
1) "three"
```

## Pattern: Reliable queue

Dragonfly can be used as a messaging server to implement processing of background
jobs or other kinds of messaging tasks.
A simple form of queue is often obtained pushing values into a list in the
producer side, and waiting for this values in the consumer side using `RPOP`
(using polling), or `BRPOP` if the client is better served by a blocking
operation.

However in this context the obtained queue is not _reliable_ as messages can
be lost, for example in the case there is a network problem or if the consumer
crashes just after the message is received but before it can be processed.

`RPOPLPUSH` (or `BRPOPLPUSH` for the blocking variant) offers a way to avoid
this problem: the consumer fetches the message and at the same time pushes it
into a _processing_ list.
It will use the `LREM` command in order to remove the message from the
_processing_ list once the message has been processed.

An additional client may monitor the _processing_ list for items that remain
there for too much time, pushing timed out items into the queue
again if needed.

## Pattern: Circular list

Using `RPOPLPUSH` with the same source and destination key, a client can visit
all the elements of an N-elements list, one after the other, in O(N) without
transferring the full list from the server to the client using a single `LRANGE`
operation.

The above pattern works even if one or both of the following conditions occur:

* There are multiple clients rotating the list: they'll fetch different
  elements, until all the elements of the list are visited, and the process
  restarts.
* Other clients are actively pushing new items at the end of the list.

The above makes it very simple to implement a system where a set of items must
be processed by N workers continuously as fast as possible.
An example is a monitoring system that must check that a set of web sites are
reachable, with the smallest delay possible, using a number of parallel workers.

Note that this implementation of workers is trivially scalable and reliable,
because even if a message is lost the item is still in the queue and will be
processed at the next iteration.
