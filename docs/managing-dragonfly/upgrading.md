---
description: "Breaking changes and required actions when upgrading Dragonfly to v2.1: removed flags, ACL changes, new defaults and snapshot compatibility."
sidebar_position: 11
---

# Upgrading Dragonfly

This page lists, for each release, the changes that can stop an existing deployment from starting or change how it behaves, and what to do about each one.
If you skip releases, read every section between your current version and the target version.
New features and bug fixes are listed in the [release notes](https://github.com/dragonflydb/dragonfly/releases).

## Upgrading to v2.1

In this section, v2.0 means the v2.0.x releases.

### License

Starting with v2.1, Dragonfly is released as Dragonfly Enterprise under the Dragonfly Source-Available License (DSAL) instead of the Business Source License 1.1 (BSL 1.1).
Releases before v2.1 remain under BSL 1.1.
Production use is free up to an aggregate of 100 vCPUs; beyond that, a commercial license is required, which you can get by signing up at [dragonflydb.cloud](https://dragonflydb.cloud/signup).
Review the new terms before you upgrade. See [License](../about/license.md).

### Removed and retired flags

v2.1 removes two flags and retires six. Check the command line, flagfiles and `DFLY_` environment variables of every instance before you upgrade.

| Flag | Effect on the command line or in a flagfile | What to do |
|---|---|---|
| `--proactor_irq_cpus` | Startup fails | Use `--proactor_tail_cpus` with the same CPU list. It pins the listed CPUs to the highest proactor thread indices, as `--proactor_irq_cpus` did. |
| `--proactor_busy_poll_usec` | Startup fails | Remove the flag. [`--shard_thread_busy_polling_usec`](./flags.md#--shard_thread_busy_polling_usec) still overrides busy polling for shard threads. |
| `--tiered_max_pending_stash_bytes` | Ignored, logs an error | Use `--tiered_max_pending_bytes`, which counts both reads and writes. The old value is not carried over. |
| `--s3_sign_payload` | Ignored, logs an error | Remove the flag. S3 snapshot uploads always use an unsigned payload. |
| `--s3_use_helio_client` | Ignored, logs an error | Remove the flag. Dragonfly always uses its native S3 client. |
| `--mget_dedup_keys` | Ignored, logs an error | Remove the flag. |
| `--experimental_flat_json` | Ignored, logs an error | Remove the flag. |
| `--disable_json_defragmentation` | Ignored, logs an error | Remove the flag. |

On the command line or in a flagfile, the first two flags make Dragonfly exit with code 1 and print errors such as:

```text
ERROR: Unknown command line flag 'proactor_irq_cpus'. Did you mean: proactor_tail_cpus ?
ERROR: Unknown command line flag 'proactor_busy_poll_usec'
```

The six retired flags are still accepted but have no effect. Each one logs an error at startup, for example:

```text
ERROR: Accessing retired flag 'mget_dedup_keys'
```

Set as `DFLY_` environment variables, the two removed flags make Dragonfly abort at startup:

```text
unknown environment variable DFLY_proactor_irq_cpus
```

Remove all eight flags from the command lines, flagfiles and `DFLY_` environment variables of your Docker, Docker Compose and Kubernetes configurations before you upgrade.
The current flags are described in [Server Configuration Flags](./flags.md).

### Changed flag defaults

- [`--enable_resp_io_loop_v2`](./flags.md#--enable_resp_io_loop_v2) is now `true` (was `false`): RESP connections use the event-driven IoLoopV2.
- [`--use_oah_set`](./flags.md#--use_oah_set) is now `true` (was `false`): set values are stored in OAHSet instead of StringSet.
- [`--disable_scope_based_mem_track`](./flags.md#--disable_scope_based_mem_track) is now `false` (was `true`): scope-based memory metrics are collected.

To keep the v2.0 behavior, set the old value explicitly, for example `--enable_resp_io_loop_v2=false`.

[`--list_compress_dict_threshold`](./flags.md#--list_compress_dict_threshold) is deprecated.
It still works when `--list_compress_policy` is not set, but Dragonfly logs a deprecation warning.
Replace `--list_compress_dict_threshold=N` with `--list_compress_policy=min_size=N`.

### ACL categories and rules

v2.1 aligns ACL categories with Valkey, so users defined for v2.0 can lose or gain access to commands.
Before you upgrade, load your users into a v2.1 test instance and check the commands each user needs with [`ACL DRYRUN`](../command-reference/acl/dryrun.md).

The administrative subcommands of `CLIENT` and `MEMORY` now have their own categories:

- `CLIENT KILL`, `CLIENT LIST`, `CLIENT MIGRATE`, `CLIENT PAUSE` and `CLIENT UNPAUSE`: `@admin, @connection, @dangerous, @slow`.
- `MEMORY ARENA`, `MEMORY DECOMMIT`, `MEMORY DEFRAGMENT`, `MEMORY DEFRAGMENT-SEGMENTS` and `MEMORY TRACK`: `@admin, @dangerous, @slow`.

Users whose rules remove `@admin` or `@dangerous`, such as `+@all -@dangerous`, can no longer run these subcommands, and `+@connection -@admin` no longer allows the `CLIENT` ones.
Other subcommands, such as `CLIENT GETNAME` and `MEMORY USAGE`, keep the categories of their parent command, and `+client` and `+memory` still allow every subcommand.

```shell
dragonfly> ACL SETUSER ops ON nopass ~* +@all -@dangerous
OK
dragonfly> ACL DRYRUN ops CLIENT LIST
"This user has no permissions to run the 'CLIENT LIST' command"
dragonfly> ACL DRYRUN ops CLIENT GETNAME
OK
dragonfly> ACL DELUSER ops
(integer) 1
```

Rules can now name these subcommands with `|`, for example `+client|kill` or `-memory|arena`. v2.0 rejected such rules as unrecognized parameters.
Subcommands without their own ACL entry cannot be named this way: `+client|getname` returns `ERR Unrecognized parameter`.
[`ACL CAT`](../command-reference/acl/cat.md) lists the new entries as `CLIENT|KILL`, `MEMORY|ARENA` and so on, and lists `ACL` subcommands as `ACL|SAVE` instead of `ACL SAVE`. Update scripts that parse its output.

The categories of 65 commands changed. The most visible changes:

- `JSON.*`, `BF.*` and `CL.THROTTLE` gained `@read` or `@write`, and `@fast` or `@slow`.
- `FT.*` commands gained `@slow`. `FT.CREATE`, `FT.ALTER`, `FT.DROPINDEX` and `FT.SYNUPDATE` also gained `@write`, and `FT.CONFIG` gained `@admin` and `@dangerous`.
- `XGROUP` gained `@stream` and `@write`, `XINFO` gained `@read` and `@stream`, and `SHRINK` changed from `@read, @slow` to `@fast, @write`.
- `HGETALL` moved from `@fast` to `@slow`. `ZLEXCOUNT`, `BZPOPMIN`, `BZPOPMAX` and `XSETID` moved from `@slow` to `@fast`.
- `REPLTAKEOVER`, `DFLY` and `DFLYCLUSTER` are now `@admin, @dangerous, @slow`.

As a result, a user defined as `+@all -@write` can no longer run `JSON.SET`, `BF.ADD`, `CL.THROTTLE`, `FT.CREATE`, `XGROUP CREATE` or `SHRINK`, and a user defined as `-@all +@read` can now run `JSON.GET`, `BF.EXISTS` and `XINFO`.
`-@admin` now also denies `FT.CONFIG` and `REPLTAKEOVER`, and `-@dangerous` now also denies `FT.CONFIG`, `DFLY` and `DFLYCLUSTER`.

### ACL key permissions

[Key patterns](./acl.md#key-permissions) are checked more strictly:

- A command that both reads and writes a key, such as `INCR`, `GETDEL`, `LPOP` or `SET` with the `GET` option, needs read and write access to that key from one pattern: `~pattern` or `%RW~pattern`.
  A `%W~` pattern alone no longer allows it, and neither do two different patterns such as `%R~a* %W~a:*`.
  The same pattern given as both `%R~` and `%W~` is merged into one `~` pattern.
- `MEMORY USAGE`, `XINFO` and `JSON.DEBUG` now require read access to the key they inspect.
- [`RM`](../command-reference/generic/rm.md) now requires write access to all keys: `~*`, `%W~*` or `%RW~*`.

### ACL file and passwords

- If the file given with [`--aclfile`](./flags.md#--aclfile) is missing or cannot be parsed, Dragonfly logs `Could not load the acl file <path>: <reason>` and exits with code 1.
  v2.0 logged a warning and started with only the `default` user, which had no password unless `--requirepass` was set.
  Fix the file, or create an empty one, before you upgrade.
- A `#<hash>` password must be exactly 64 hexadecimal characters, the SHA-256 digest of the password. `ACL SETUSER` now accepts it too.
  A shorter or invalid hash returns `ERR Error in ACL SETUSER modifier: The password hash must be exactly 64 hexadecimal characters`, and the same hash in the ACL file stops startup.
  v2.0 accepted malformed hashes in ACL files without an error. Files written by `ACL SAVE` on v2.0 load unchanged.
- `CONFIG SET requirepass <password>` now replaces all passwords of the `default` user. v2.0 added the new password and kept the old ones.
  `CONFIG SET requirepass ""` makes `default` a `nopass` user and removes its passwords.
- [`--jwt_validate`](./flags.md#--jwt_validate) can only be set at startup. `CONFIG SET jwt_validate` returns `ERR Unknown option or number of arguments for CONFIG SET - 'jwt_validate'`.

### Network listeners

Without [`--bind`](./flags.md#--bind), v2.1 listens on `::` instead of `0.0.0.0` on hosts that support dual-stack sockets (on Linux, when `net.ipv6.bindv6only` is `0`), so one listener accepts both IPv4 and IPv6 clients.
IPv4 clients still appear with their IPv4 addresses, for example in `CLIENT LIST`.
The startup log shows the new address:

```text
AcceptServer - listening on :::6379
```

If Dragonfly must not accept IPv6 connections, set `--bind` explicitly, for example `--bind=0.0.0.0`.
The admin port does not follow `--bind`: even with `--bind` set, the admin listener uses `::` when `--admin_port` is set and [`--admin_bind`](./flags.md#--admin_bind) is empty. Set `--admin_bind` as well.

### TIME reply

[`TIME`](../command-reference/server-management/time.md) now returns its two elements as bulk strings, as Valkey does. v2.0 returned two integers.
Clients that check the reply type, and Lua scripts that call `redis.call('TIME')`, now get strings. In Lua, convert them with `tonumber()` where a number is needed.

### Snapshots and persistence

v2.1 writes hashes that have field expirations, such as those set with [`HSETEX`](../command-reference/hashes/hsetex.md), in the RDB encoding shared with Valkey (object type 22) instead of the Dragonfly-specific type 31.
This applies to Dragonfly-format snapshots, to `SAVE RDB` files and to `DUMP` payloads.
v2.1 still loads snapshots and `DUMP` payloads from older versions.

Versions older than v2.1 cannot read the new encoding. v2.0 fails to start from a snapshot that contains such a hash and logs:

```text
Unrecognized rdb object type: 22
Rdb load failed: Internal error when loading RDB file 8
```

`RESTORE` on v2.0 rejects such `DUMP` payloads with `ERR Bad data format`.
To roll back after v2.1 has written hashes with field expirations, replicate from the v2.1 instance to an instance that runs the older version, then promote it. Full sync to an older replica still uses the old encoding, and so does `DUMP` while such a replica is connected.

v2.1 also adds experimental append-only file persistence, disabled by default (`--aof`). See [Append Only File (AOF)](./aof.md).

### Search

[`FT.INFO`](../command-reference/search/ft.info.md) output changed. Update clients that parse it by position or compare its values as text:

- `default_language` appears only when the index language is not `english`.
- `attributes` are listed in declaration order.
- Each attribute lists its parameters before its flags, and numbers use the shortest form: `WEIGHT 1 SORTABLE` instead of `SORTABLE WEIGHT 1.000000`.
- Sortable `NUMERIC` fields also show `UNF`.
- The index name and the attribute entries are bulk strings instead of simple strings.

[`FT.CREATE`](../command-reference/search/ft.create.md) now rejects a field declared with both `NOINDEX` and `INDEXMISSING`, which v2.0 accepted:

```shell
dragonfly> FT.CREATE idx ON HASH SCHEMA title TEXT NOINDEX INDEXMISSING
(error) ERR Field cannot be defined with both `NOINDEX` and `INDEXMISSING` `title`
```
