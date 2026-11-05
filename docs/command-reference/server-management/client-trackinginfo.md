---
description: Learn how to use Redis CLIENT TRACKINGINFO command to check the server-assisted client-side caching state of the current connection.
---

import PageTitle from '@site/src/components/PageTitle';

# CLIENT TRACKINGINFO

<PageTitle title="Redis CLIENT TRACKINGINFO Command (Documentation) | Dragonfly" />

## Syntax

    CLIENT TRACKINGINFO

**Time complexity:** O(1)

**ACL categories:** @connection, @slow

**Availability:** Dragonfly v2.1.0 and later.

The `CLIENT TRACKINGINFO` command returns the server-assisted client-side caching state of the current connection:
whether tracking is enabled with [`CLIENT TRACKING`](./client-tracking.md), which options were used,
and whether a [`CLIENT CACHING`](./client-caching.md) override is pending.

Unlike `CLIENT TRACKING` and `CLIENT CACHING`, which require RESP3, `CLIENT TRACKINGINFO` also works on RESP2 connections.

## Return

[Map reply](https://valkey.io/topics/protocol/#maps) on RESP3, or a flat [Array reply](https://valkey.io/topics/protocol/#arrays)
of three field/value pairs on RESP2, with the following fields:

- `flags`: a [Set reply](https://valkey.io/topics/protocol/#sets) (an array on RESP2) of tracking flags:
  - `off`: tracking is disabled.
  - `on`: tracking is enabled.
  - `optin` or `optout`: tracking was enabled with the `OPTIN` or `OPTOUT` option.
  - `noloop`: tracking was enabled with the `NOLOOP` option.
  - `caching-yes` (with `optin`) or `caching-no` (with `optout`): the one-shot override set by `CLIENT CACHING YES` or `CLIENT CACHING NO` is pending.
- `redirect`: an [Integer reply](https://valkey.io/topics/protocol/#integers), `-1` when tracking is off and `0` when it is on.
- `prefixes`: an [Array reply](https://valkey.io/topics/protocol/#arrays) that is always empty.

Dragonfly does not support the `REDIRECT`, `BCAST` and `PREFIX` options of `CLIENT TRACKING`.
As a result, `redirect` never holds a client ID, `prefixes` never lists a prefix,
and the Valkey flags `bcast` and `broken_redirect` never appear.

Passing any argument returns `ERR syntax error`.

## Pending CLIENT CACHING overrides

`CLIENT CACHING YES` and `CLIENT CACHING NO` affect only the next command on the connection.
In Dragonfly, `CLIENT TRACKINGINFO` counts as that command: it reports `caching-yes` or `caching-no` and uses up the override.
If you call `CLIENT TRACKINGINFO` between `CLIENT CACHING` and the read the override was meant for,
the read is handled according to the plain `OPTIN` or `OPTOUT` mode.

## Examples

A new connection uses RESP2, so the reply is a flat array. Tracking is off:

```shell
dragonfly> CLIENT TRACKINGINFO
1) "flags"
2) 1) "off"
3) "redirect"
4) (integer) -1
5) "prefixes"
6) (empty array)
```

Switch the connection to RESP3, enable tracking, and check its state.
The `id` field of the `HELLO` reply varies between connections.

```shell
dragonfly> HELLO 3
1# "server" => "redis"
2# "version" => "7.4.0"
3# "dragonfly_version" => "df-v2.1"
4# "proto" => (integer) 3
5# "id" => (integer) 57
6# "mode" => "standalone"
7# "role" => "master"
dragonfly> CLIENT TRACKING ON
OK
dragonfly> CLIENT TRACKINGINFO
1# "flags" => 1~ "on"
2# "redirect" => (integer) 0
3# "prefixes" => (empty array)
```

In `OPTIN` mode, the first `CLIENT TRACKINGINFO` call after `CLIENT CACHING YES` reports `caching-yes` and uses up the override,
so the second call no longer reports it:

```shell
dragonfly> HELLO 3
1# "server" => "redis"
2# "version" => "7.4.0"
3# "dragonfly_version" => "df-v2.1"
4# "proto" => (integer) 3
5# "id" => (integer) 58
6# "mode" => "standalone"
7# "role" => "master"
dragonfly> CLIENT TRACKING ON OPTIN
OK
dragonfly> CLIENT CACHING YES
OK
dragonfly> CLIENT TRACKINGINFO
1# "flags" => 1~ "on"
   2~ "optin"
   3~ "caching-yes"
2# "redirect" => (integer) 0
3# "prefixes" => (empty array)
dragonfly> CLIENT TRACKINGINFO
1# "flags" => 1~ "on"
   2~ "optin"
2# "redirect" => (integer) 0
3# "prefixes" => (empty array)
```
