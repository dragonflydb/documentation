---
description: "Learn how to use Redis CLUSTER KEYSLOT command to compute the hash slot of a key in Dragonfly, including hash tags."
---

import PageTitle from '@site/src/components/PageTitle';

# CLUSTER KEYSLOT

<PageTitle title="Redis CLUSTER KEYSLOT Command (Documentation) | Dragonfly" />

## Syntax

    CLUSTER KEYSLOT key

**Time complexity:** O(N) where N is the number of bytes in the key

**ACL categories:** @slow

The `CLUSTER KEYSLOT` command returns the hash slot of `key`: the CRC16 of the key modulo 16384.
If the key contains a [hash tag](https://valkey.io/topics/cluster-spec/#hash-tags), only the tag is hashed,
so keys with the same tag map to the same slot.
With the default flags, the result is the same as in Valkey.

The slot is computed from the key name only.
The command does not check whether the key exists or which node owns the slot.
It requires `--cluster_mode=emulated` or `--cluster_mode=yes`.
Otherwise, it returns `ERR Cluster is disabled. Enabled via passing --cluster_mode=emulated|yes`.

Dragonfly extracts the hash tag with the same rules that it uses for lock tags.
The [`--locktag_delimiter`](../../managing-dragonfly/flags.md#--locktag_delimiter),
[`--locktag_skip_n_end_delimiters`](../../managing-dragonfly/flags.md#--locktag_skip_n_end_delimiters) and
[`--locktag_prefix`](../../managing-dragonfly/flags.md#--locktag_prefix) flags change these rules, even without `--lock_on_hashtags`,
and `CLUSTER KEYSLOT` follows them.
With `--cluster_mode=yes`, the node also uses this slot to decide whether it serves a key or replies with a `MOVED` redirection.
The result can then differ from the slot that a cluster client computes.
For example, with `--locktag_prefix=pre`, `CLUSTER KEYSLOT {user1}.a` returns `5959` instead of `8106`,
because the key does not start with `pre` and is hashed as a whole.

## Return

[Integer reply](https://valkey.io/topics/protocol/#integers): the hash slot of the key, from `0` to `16383`.

## Examples

```shell
dragonfly> CLUSTER KEYSLOT somekey
(integer) 11058
dragonfly> CLUSTER KEYSLOT {user1}.following
(integer) 8106
dragonfly> CLUSTER KEYSLOT {user1}.followers
(integer) 8106
```

## See also

[`CLUSTER SLOTS`](./cluster-slots.md) | [`CLUSTER SHARDS`](./cluster-shards.md) | [`CLUSTER`](./cluster.md) | [Cluster Mode](../../managing-dragonfly/cluster-mode.md)
