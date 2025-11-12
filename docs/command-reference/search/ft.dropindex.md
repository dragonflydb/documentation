---
description: Deletes the index
---

# FT.DROPINDEX

## Syntax

    FT.DROPINDEX index [DD]

**Time complexity:** O(1) or O(N) if `DD` is used, where N is the number of documents in the index.

## Description

Delete an index.

By default, `FT.DROPINDEX` only removes the index definition and associated metadata while keeping the actual documents (HASH or JSON keys) intact.

## Required arguments

<details open>
<summary><code>index</code></summary>

is index name. You must first create the index using [`FT.CREATE`](./ft.create.md).
</details>

## Optional arguments

<a name="DD"></a>
<details open>
<summary><code>DD</code></summary>

If set, the operation will delete the actual documents (HASH or JSON keys) that were indexed, in addition to dropping the index itself.

Without this option, only the index structure is removed while all the indexed documents remain in the database.

:::warning
Using `DD` will permanently delete all documents that were indexed. This operation cannot be undone.
:::

</details>

## Return

`FT.DROPINDEX` returns a simple string reply `OK` if executed correctly, or an error reply otherwise.

## Examples

<details open>
<summary><b>Delete an index (keep documents)</b></summary>

Delete the index but keep all the indexed documents in the database.

```bash
dragonfly> FT.DROPINDEX idx
OK
```
</details>

<details open>
<summary><b>Delete an index and all its documents</b></summary>

Delete the index and all documents that were indexed by it.

```bash
dragonfly> FT.DROPINDEX idx DD
OK
```

:::warning
This will permanently delete all HASH or JSON keys that were indexed by `idx`.
:::

</details>

## See also

[`FT.CREATE`](./ft.create.md) | [`FT.INFO`](./ft.info.md)

## Related topics

- [RediSearch](https://redis.io/docs/latest/operate/oss_and_stack/stack-with-enterprise/search/)
