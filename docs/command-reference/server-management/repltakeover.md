---
description: Learn how to use the Dragonfly REPLTAKEOVER command to promote a replica to master in a planned failover.
---

import PageTitle from '@site/src/components/PageTitle';

# REPLTAKEOVER

<PageTitle title="Dragonfly REPLTAKEOVER Command (Documentation) | Dragonfly" />

## Syntax

    REPLTAKEOVER timeout_sec [SAVE]

**Time complexity:** O(1)

**ACL categories:** @admin, @dangerous, @slow

`REPLTAKEOVER` promotes a replica to master in a planned failover. Run it on a replica that is in
stable sync with its master: `ROLE` reports `online`, or `stable_sync` if the replica runs with
`--info_replication_valkey_compatible=false`. The master first stops serving regular clients and
waits until the replica has applied all of the master's writes. Only then does the replica become
master. This command is Dragonfly-specific.

Valkey's [`FAILOVER`](https://valkey.io/commands/failover/) command, which runs on the master, is
not implemented in Dragonfly. Use `REPLTAKEOVER` on the replica instead.

`REPLTAKEOVER` needs a running master. If the master has failed, promote the replica with
[`REPLICAOF NO ONE`](./replicaof.md).

:::caution
Run `REPLTAKEOVER` only on a replica of a Dragonfly master. In Dragonfly v2.1.0, running it on a
replica of a Redis or Valkey master crashes the replica process.
:::

## Arguments

- `timeout_sec`: how many seconds the master may take to finish running commands and let the
  replica catch up. It must be a non-negative integer. The call returns when the takeover
  succeeds or fails. `0` is accepted, but it leaves the master no time, so in practice the
  takeover fails.
- `SAVE`: the old master saves a snapshot to its `--dir` once the replica has taken over.

## How the takeover works

1. The master stops serving regular clients. Only `PING` and the commands that
   [`COMMAND INFO`](./command-info.md) flags as `admin`, such as `CONFIG`, `SLOWLOG` and
   `REPLICAOF`, still run. Every other command, including reads, `INFO`, `ROLE` and `CLIENT`, fails
   with `LOADING Dragonfly is loading the dataset in memory`. Blocking commands waiting on the
   master are cancelled: `BLPOP` returns a null reply, as if its timeout had expired. Connections
   on the admin port (`--admin_port`) are not restricted.
2. The master waits up to `timeout_sec` seconds for commands that are already running to finish
   and for the replica to apply all the writes the master has executed.
3. The master confirms, and the replica promotes itself to master and returns `OK`.
4. The old master gives its other replicas the rest of `timeout_sec` to catch up. With `SAVE`, it
   then saves a snapshot to its `--dir`. Then it shuts down like `SHUTDOWN NOSAVE`, so without
   `SAVE` no snapshot is written. The process exits with status 0. With `--cluster_mode=yes` it
   stays up instead; see [Cluster mode](#cluster-mode).

If the master cannot finish step 2 within `timeout_sec`, it goes back to serving clients, the
replica stays a replica, and `REPLTAKEOVER` returns `Couldn't execute takeover: Bad message`.
A long-running command, a client that reads a large reply slowly, or a lagging replica can keep
the master from finishing in time.

## After the takeover

Outside cluster mode, clients are not redirected. Point them, or the DNS name or service they
connect through, to the new master.

The old master's other replicas keep trying to reach the old master. Run
[`REPLICAOF`](./replicaof.md) with the new master's address on each of them. They can continue
with a partial sync instead of a full sync if the new master's
[replication backlog](../../managing-dragonfly/replication.md#dragonfly-dragonfly-replication)
still holds the writes made since the takeover.

If the old master is restarted with its original flags, it starts as a separate master and loads
the newest snapshot in its `--dir`, if there is one. To add it back, start it as a replica of the
new master instead, for example with `--replicaof`.

## Cluster mode

With `--cluster_mode=yes`, the old master doesn't shut down. The new master takes over the old
master's slots in its own cluster configuration. The old master stays in the taken-over state:
`PING` returns `PONG`, commands on keys get a `MOVED` redirect to the new master, commands flagged
`admin` still run, and other commands fail with the `LOADING` error.

The slots move only if the cluster configuration lists the replica among the old master's
replicas. Otherwise the takeover still returns `OK`, but both nodes keep redirecting the old
master's slots to the old master, and the old master redirects them to itself.

Other cluster nodes don't learn about the change. Push the updated configuration to all nodes with
`DFLYCLUSTER CONFIG`, as for any other change to the
[cluster](../../managing-dragonfly/cluster-mode.md#multi-shard-cluster). The new configuration
doesn't end the old master's taken-over state, even if it gives the old master its slots back, and
`REPLICAOF NO ONE` returns `OK` without ending it either. Only `REPLICAOF` with a master's address,
or a restart, ends it. For example, run `REPLICAOF` with the new master's address to make the old
master a replica of the new master.

With `--cluster_mode=emulated`, the old master shuts down, as in standalone mode.

## Return

[Simple string reply](https://valkey.io/topics/protocol/#simple-strings): `OK` if the takeover
succeeded. On a master, the command changes nothing and returns `OK`.

[Error reply](https://valkey.io/topics/protocol/#simple-errors):

- `ERR wrong number of arguments for 'repltakeover' command` if `timeout_sec` is missing.
- `ERR value is not an integer or out of range` if `timeout_sec` is not an integer.
- `ERR timeout is negative` if `timeout_sec` is negative.
- `ERR Unsupported option:<argument>` for any argument after `timeout_sec` other than one `SAVE`.
- `LOADING Dragonfly is loading the dataset in memory` while the replica loads the master's data
  in a full sync.
- `ERR Full sync not done` if the replica is not in stable sync for another reason, for example
  right after `REPLICAOF` or while the master is unreachable.
- `ERR Couldn't execute takeover: <reason>` if the takeover failed. If the master could not
  finish within `timeout_sec`, the reason is `Bad message`.

## Examples

These sessions use two Dragonfly containers on one Docker network. The master runs with default
flags and is reachable as `primary`. The replica was started with `--replicaof=primary:6379`, and
the key `greeting` was set to `hello` on the master.

Run `REPLTAKEOVER` on the replica:

```shell
dragonfly> ROLE
1) "slave"
2) "primary"
3) "6379"
4) "online"

dragonfly> REPLTAKEOVER 10
OK

dragonfly> ROLE
1) "master"
2) (empty array)

dragonfly> GET greeting
"hello"

dragonfly> SET greeting bye
OK
```

The `primary` container exited with status 0 right after the takeover.

A timeout of `0` leaves the master no time to finish, so the takeover fails and the replica keeps
its role:

```shell
dragonfly> REPLTAKEOVER 0
(error) ERR Couldn't execute takeover: Bad message

dragonfly> ROLE
1) "slave"
2) "primary"
3) "6379"
4) "online"
```

After the master failed, the replica reports `connecting`. `REPLTAKEOVER` is rejected, so promote
the replica with `REPLICAOF NO ONE`:

```shell
dragonfly> ROLE
1) "slave"
2) "primary"
3) "6379"
4) "connecting"

dragonfly> REPLTAKEOVER 10
(error) ERR Full sync not done

dragonfly> REPLICAOF NO ONE
OK

dragonfly> ROLE
1) "master"
2) (empty array)
```

On a master, the command returns `OK` and changes nothing. Invalid arguments are rejected:

```shell
dragonfly> REPLTAKEOVER 10
OK

dragonfly> REPLTAKEOVER -1
(error) ERR timeout is negative

dragonfly> REPLTAKEOVER ten
(error) ERR value is not an integer or out of range

dragonfly> REPLTAKEOVER 10 NOW
(error) ERR Unsupported option:NOW
```

## See also

[`REPLICAOF`](./replicaof.md) | [`ROLE`](./role.md) | [`SHUTDOWN`](./shutdown.md) | [Replication](../../managing-dragonfly/replication.md) | [Cluster mode](../../managing-dragonfly/cluster-mode.md)
