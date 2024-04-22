---
description:  Discover how to use Redis SET command to attach a value to a specific key in the database.
---

import PageTitle from '@site/src/components/PageTitle';

# SET

<PageTitle title="Redis SET Command (Documentation) | Dragonfly" />

## Syntax

    SET key value [NX | XX] [GET] [EX seconds | PX milliseconds | EXAT unix-time-seconds | PXAT unix-time-milliseconds | KEEPTTL]

**Time complexity:** O(1)

**ACL categories:** @write, @string, @slow

Set `key` to hold the string `value`.
If `key` already holds a value, it is overwritten, regardless of its type.
Any previous time to live associated with the key is discarded on successful `SET` operation.

## Options

The `SET` command supports a set of options that modify its behavior:

* `EX` *seconds* -- Set the specified expire time, in seconds.
* `PX` *milliseconds* -- Set the specified expire time, in milliseconds.
* `EXAT` *timestamp-seconds* -- Set the specified Unix time at which the key will expire, in seconds.
* `PXAT` *timestamp-milliseconds* -- Set the specified Unix time at which the key will expire, in milliseconds.
* `NX` -- Only set the key if it does not already exist.
* `XX` -- Only set the key if it already exist.
* `KEEPTTL` -- Retain the time to live associated with the key.
* `GET` -- Return the old string stored at key, or nil if key did not exist. An error is returned and `SET` aborted if the value stored at key is not a string.

Note: Since the `SET` command options can replace `SETNX`, `SETEX`, `PSETEX`, `GETSET`, it is possible that in future versions these commands will be deprecated and finally removed.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec/#simple-strings): `OK` if `SET` was executed correctly.

[Null reply](https://redis.io/docs/reference/protocol-spec/#bulk-strings): `(nil)` if the `SET` operation was not performed because the user specified the `NX` or `XX` option but the condition was not met.

If the command is issued with the `GET` option, the above does not apply. It will instead reply as follows, regardless if the `SET` was actually performed:

[Bulk string reply](https://redis.io/docs/reference/protocol-spec/#bulk-strings): the old string value stored at key.

[Null reply](https://redis.io/docs/reference/protocol-spec/#bulk-strings): `(nil)` if the key did not exist.

## Examples

```shell
dragonfly> SET mykey "Hello"
OK
dragonfly> GET mykey
"Hello"
dragonfly> SET anotherkey "will expire in a minute" EX 60
OK
dragonfly> SET mykey "World" GET
"Hello"
```

## Patterns

**Note:** The following pattern is discouraged in favor of [the Redlock algorithm](https://redis.io/topics/distlock) which is only a bit more complex to implement, but offers better guarantees and is fault tolerant.

The command `SET resource-name anystring NX EX max-lock-time` is a simple way to implement a locking system with Redis.

A client can acquire the lock if the above command returns `OK` (or retry after some time if the command returns Nil), and remove the lock just using `DEL`.

The lock will be auto-released after the expire time is reached.

It is possible to make this system more robust modifying the unlock schema as follows:

* Instead of setting a fixed string, set a non-guessable large random string, called token.
* Instead of releasing the lock with `DEL`, send a script that only removes the key if the value matches.

This avoids that a client will try to release the lock after the expire time deleting the key created by another client that acquired the lock later.

An example of unlock script would be similar to the following:

    if redis.call("get",KEYS[1]) == ARGV[1]
    then
        return redis.call("del",KEYS[1])
    else
        return 0
    end

The script should be called with `EVAL ...script... 1 resource-name token-value`
