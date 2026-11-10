---
description:  Learn how to use Redis ROLE command to retrieve the role of the server.
---

import PageTitle from '@site/src/components/PageTitle';

# ROLE

<PageTitle title="Redis ROLE Command (Documentation) | Dragonfly" />

## Syntax

    ROLE

**Time complexity:** O(1)

**ACL categories:** @admin, @fast, @dangerous

Provide information on the role of a Dragonfly instance in the context of replication, by returning if the instance is currently a `master` or `slave`. The command also returns additional information about the state of the replication.

## Output format

The command returns an array of elements. The first element is the role of
the instance, as one of the following strings:

* "master"
* "slave"

The additional elements of the array depends on the role.

## Master output

An example of output when `dragonfly> ROLE` is called in a master instance:

```
1) "master"
2) 1) 1) "127.0.0.1"
      2) "6380"
      3) "online"
```

The master output is composed of the following parts:

1. The string `master`.
2. An array composed of a three elements array for each connected replica. Every sub-array contains the replica's IP, port, and replication state. For the state meanings see the replica output description below.

## Output of the command on replicas

An example of output when `ROLE` is called in a replica instance:

```
1) "slave"
2) "127.0.0.1"
3) "6379"
4) "online"
```

The replica output is composed of the following parts:

1. The string `slave`.
2. The IP address or hostname of the master.
3. The port number of the master.
4. The current replication state, that can be `connecting` (trying to form a network link), `preparation` (initial connection has been made), `full_sync` (the master and replica are performing a full synchronization) and `online` (the replica is in stable sync with the master).

`slave` and `online` are the default, Valkey-compatible values. When an instance runs with
[`--info_replication_valkey_compatible=false`](../../managing-dragonfly/flags.md#--info_replication_valkey_compatible),
its `ROLE` reply contains `replica` instead of `slave` and `stable_sync` instead of `online`.

## Return

[Array reply](https://valkey.io/topics/protocol/#arrays): where the first element is `master` or `slave` and the additional elements are role-specific as illustrated above.
