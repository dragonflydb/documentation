---
description: Return the role of the instance in the context of replication
---

# ROLE

## Syntax

    ROLE 

**Time complexity:** O(1)

**ACL categories:** @admin, @fast, @dangerous

Provide information on the role of a Dragonfly instance in the context of replication, by returning if the instance is currently a `master` or `slave`. The command also returns additional information about the state of the replication.

## Output format

The command returns an array of elements. The first element is the role of
the instance, as one of the following three strings:

* "master"
* "slave"

The additional elements of the array depends on the role.

## Master output

An example of output when `dragonfly> ROLE` is called in a master instance:

```
1) "master"
2) 1) 1) "127.0.0.1"
      2) "6380"
      3) "stable_sync"

```

The master output is composed of the following parts:

1. The string `master`.
2. An array composed of a three elements array for each connected replica. Every sub-array contains the replica's IP, port, and replication state. For the state meanings see the replica output description below.

## Output of the command on replicas

An example of output when `ROLE` is called in a replica instance:

```
1) "replica"
2) "127.0.0.1"
3) "6379"
4) "stable_sync"
```

The replica output is composed of the following parts:

1. The string `replica`, because of backward compatibility (see note at the end of this page).
2. The IP of the master.
3. The port number of the master.
4. The current replication state, that can be `connecting` (trying to form a network link), `preparation` (initial connection has been made), `full_sync` (the master and replica are performing a full synchronization) and `stable_sync` (the replica is online)

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays): where the first element is one of `master`, `slave`, `sentinel` and the additional elements are role-specific as illustrated above.
