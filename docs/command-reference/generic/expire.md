---
description: "Learn Redis EXPIRE command that sets a key's time-to-live in seconds."
---

import PageTitle from '@site/src/components/PageTitle';

# EXPIRE

<PageTitle title="Redis EXPIRE Command (Documentation) | Dragonfly" />

## Syntax

    EXPIRE key seconds [NX | XX | GT | LT]

**Time complexity:** O(1)

**ACL categories:** @keyspace, @write, @fast

Set a timeout on `key`.
After the timeout has expired, the key will automatically be deleted.
A key with an associated timeout is often said to be _volatile_ in Dragonfly
terminology.

The timeout will only be cleared by commands that delete or overwrite the
contents of the key, including `DEL`, `SET`, `GETSET` and all the `*STORE`
commands.
This means that all the operations that conceptually _alter_ the value stored at
the key without replacing it with a new one will leave the timeout untouched.
For instance, incrementing the value of a key with `INCR`, pushing a new value
into a list with `LPUSH`, or altering the field value of a hash with `HSET` are
all operations that will leave the timeout untouched.

The timeout can also be cleared, turning the key back into a persistent key,
using the `PERSIST` command.

If a key is renamed with `RENAME`, the associated time to live is transferred to
the new key name.

If a key is overwritten by `RENAME`, like in the case of an existing key `Key_A`
that is overwritten by a call like `RENAME Key_B Key_A`, it does not matter if
the original `Key_A` had a timeout associated or not, the new key `Key_A` will
inherit all the characteristics of `Key_B`.

Note that calling `EXPIRE`/`PEXPIRE` with a non-positive timeout or
`EXPIREAT`/`PEXPIREAT` with a time in the past will result in the key being
[deleted][del] rather than expired (accordingly, the emitted [key event][ntf]
will be `del`, not `expired`).

[del]: ./del.md
[ntf]: https://redis.io/topics/notifications

## Options

- `NX`: Expiry will only be set if the key has no expiry.
- `XX`: Expiry will only be set if the key has an existing expiry.
- `GT`: Expiry will only be set if the new expiry is greater than current one.
- `LT`: Expiry will only be set if the new expiry is less than current one.

## Refreshing Expiries

It is possible to call `EXPIRE` using as argument a key that already has an
existing expiry set.
In this case the time to live of a key is **updated** to the new value.
There are many useful applications for this, an example is documented in the
**Navigation Session** pattern section below.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers), specifically:

- `1` if the timeout was set.
- `0` if the timeout was not set. e.g. key doesn't exist, or operation skipped due to the provided arguments.

## Examples

```shell
dragonfly> SET mykey "Hello"
OK
dragonfly> EXPIRE mykey 10
(integer) 1
dragonfly> TTL mykey
(integer) 10
dragonfly> SET mykey "Hello World"
OK
dragonfly> TTL mykey
(integer) -1
```

## Pattern: Navigation Session

Imagine you have a web service and you are interested in the latest N pages
**recently** visited by your users, such that each adjacent page view was not
performed more than 60 seconds after the previous.
Conceptually you may consider this set of page views as a **navigation session**
of your user, that may contain interesting information about what kind of
products he or she is looking for currently, so that you can recommend related
products.

You can easily model this pattern in Dragonfly using the following strategy: every
time the user does a page view you call the following commands:

```
MULTI
RPUSH pagewviews.user:<userid> http://.....
EXPIRE pagewviews.user:<userid> 60
EXEC
```

If the user will be idle more than 60 seconds, the key will be deleted and only
subsequent page views that have less than 60 seconds of difference will be recorded.
This pattern can also be easily modified to use counters (i.e., `INCR`) instead of lists.

---

## Appendix: Dragonfly Expiries

### Keys with an Expiry

Normally Dragonfly keys are created without an associated time to live.
The key will simply live forever, unless it is removed by the user in an
explicit way, for instance, using the `DEL` command.

The `EXPIRE` family of commands is able to associate an expiry to a given key,
at the cost of some additional memory used by the key.
When a key has an expiry set, Dragonfly will make sure to remove the key when the
specified amount of time has elapsed.

The key time to live can be updated or entirely removed using the `EXPIRE` and
`PERSIST` commands (or other strictly related commands).

### Expiry Accuracy

Dragonfly expiry accuracy is in order of milliseconds.

### How Dragonfly Expires Keys

Dragonfly keys expire in two ways: a passive way and an active way.

A key is passively expired simply when some client tries to access it, and the
key is found to be timed out.

Of course this is not enough, as there are expired keys that will never be
accessed again.
These keys should be expired anyway, so periodically Dragonfly tests a few keys at
random among keys with an expire set.
All the keys that are already expired are deleted from the keyspace.

### How Expiries Are Handled in the Replication Link

In order to obtain a correct behavior without sacrificing consistency, when a
key expires, a `DEL` operation is sent to all the attached replica nodes.
This way the expiration process is centralized in the master instance, and there
is no chance of consistency errors.

However, while the replicas connected to a master will not expire keys
independently (but will wait for the `DEL` coming from the master), they'll
still take the full state of the expiries existing in the dataset, so when a
replica is elected to master, it will be able to expire the keys independently,
fully acting as a master.
