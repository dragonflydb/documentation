---
description: Learn how to use Redis CLIENT INFO command to get information and statistics about the current client connection.
---

import PageTitle from '@site/src/components/PageTitle';

# CLIENT INFO

<PageTitle title="Redis CLIENT INFO Command (Documentation) | Dragonfly" />

## Syntax

    CLIENT INFO

**Time complexity:** O(1)

**ACL categories:** @connection, @slow

The `CLIENT INFO` command returns information and statistics about the current client connection.
The reply uses the [`CLIENT LIST`](./client-list.md) line format and describes only the calling connection.

Compared with the `CLIENT LIST` line of the same connection, `CLIENT INFO` always reports `tid=0`,
appends a set of placeholder fields, and has no trailing newline.

## Return

[Bulk string reply](https://valkey.io/topics/protocol/#bulk-strings): a single line of `property=value` fields separated by spaces.
Dragonfly returns a bulk string on RESP3 connections too, where Valkey returns a verbatim string.

Passing any argument returns `ERR syntax error`.

## Fields

The fields appear in the following order. Fields marked as optional are printed only when they apply.

- `id`: the client ID, as returned by [`CLIENT ID`](./client-id.md).
- `addr`: the address and port of the client.
- `laddr`: the local address and port that the client connected to.
- `fd`: the file descriptor of the socket.
- `name`: the connection name. A new connection reports its client ID here until a name is set with
  [`CLIENT SETNAME`](./client-setname.md) or the `SETNAME` option of [`HELLO`](./hello.md).
  After `CLIENT SETNAME ""`, the value is empty.
- `tls` (optional): the TLS version and cipher of a TLS connection, as `version|cipher`.
- `send-wait-time` (optional): how long, in seconds, the connection has been waiting for a socket write to complete.
  Printed only while a write is in progress.
- `tid`: always `0` in `CLIENT INFO`. Use `CLIENT LIST` to see the index of the thread that serves the connection.
- `irqmatch`: `1` if the CPU that receives the socket's network traffic is the CPU running the connection's thread, otherwise `0`.
- `pipeline` and `pbuf` (optional): the number of parsed commands queued on the connection, including the command being executed,
  and the memory they use in bytes. Printed only while the queue is not empty.
- `age`: the connection age in seconds.
- `idle`: the number of seconds since the connection's last activity.
- `tot-cmds`: the number of commands the connection has run, including ones that returned an error, such as unknown commands.
- `tot-net-in`: the number of bytes read from the socket.
- `tot-read-calls`: the number of socket read calls.
- `tot-dispatches`: the number of commands and messages queued on the connection for dispatch.
- `db`: the index of the selected database.
- `flags` (optional): Dragonfly-specific letters, printed only when at least one applies:
  `a` (the command runs on the asynchronous dispatch path, as pipelined commands do),
  `t` (the connection is closing), `P` (the connection has Pub/Sub subscriptions),
  and `b` (the connection is blocked by a blocking command).
  A blocked connection runs `CLIENT INFO` only after the blocking command returns,
  so `b` shows up only in the `CLIENT LIST` lines of other connections.
- `phase`: the connection phase (`setup`, `readsock`, `process`, `send`, `scheduled`, `shutting_down` or `preclose`).
  A connection running `CLIENT INFO` normally reports `process`.
- `lib-name` and `lib-ver`: the client library name and version set with [`CLIENT SETINFO`](./client-setinfo.md), empty if not set.
- `qbuf=0 qbuf-free=0 obl=0 argv-mem=0 oll=0 omem=0 tot-mem=0 multi=0 psub=0 sub=0`: placeholders with fixed values.
  Dragonfly does not track these counters and prints them for client libraries that expect them, such as the `ACL LOG` parser in redis-py.
  `multi` and `sub` stay `0` even inside a transaction or on a subscribed connection.

Fields that Valkey reports, such as `user`, `cmd`, `resp`, `redir`, `watch` and `events`, are not part of the Dragonfly reply.

## Examples

The ID (also the default `name`), addresses, file descriptor, `irqmatch`, `age`, `idle` and the counters
vary between connections and runs.

```shell
dragonfly> CLIENT INFO
"id=60 addr=127.0.0.1:48370 laddr=127.0.0.1:6379 fd=40 name=60 tid=0 irqmatch=1 pipeline=1 pbuf=320 age=0 idle=0 tot-cmds=2 tot-net-in=61 tot-read-calls=3 tot-dispatches=3 db=0 phase=process lib-name= lib-ver= qbuf=0 qbuf-free=0 obl=0 argv-mem=0 oll=0 omem=0 tot-mem=0 multi=0 psub=0 sub=0"
dragonfly> CLIENT SETNAME worker-1
OK
dragonfly> CLIENT INFO
"id=60 addr=127.0.0.1:48370 laddr=127.0.0.1:6379 fd=40 name=worker-1 tid=0 irqmatch=1 pipeline=1 pbuf=320 age=0 idle=0 tot-cmds=4 tot-net-in=130 tot-read-calls=5 tot-dispatches=5 db=0 phase=process lib-name= lib-ver= qbuf=0 qbuf-free=0 obl=0 argv-mem=0 oll=0 omem=0 tot-mem=0 multi=0 psub=0 sub=0"
```
