---
description: Deletes the index
---

# FT.DROPINDEX

## Syntax

    FT.DROPINDEX index [DD]

**Time complexity:** O(1) or O(N) if documents are deleted, where N is the number of keys in the keyspace.

## Description

Delete an index. For usage, see [examples](#examples) below.

## Required arguments

<details open>
<summary><code>index</code></summary>

is full-text index name. You must first create the index using [`FT.CREATE`](./ft.create.md).
</details>

## Optional arguments

<details open>
<summary><code>DD</code></summary>

drop operation that, if set, deletes the actual document hashes.

By default, `FT.DROPINDEX` does not delete the documents associated with the index. Adding the `DD` option deletes the documents as well. 
If an index creation is still running ([`FT.CREATE`](./ft.create.md) is running asynchronously), only the document hashes that have already been indexed are deleted. 
The document hashes left to be indexed remain in the database.
To check the completion of the indexing, use [`FT.INFO`](./ft.info.md).

</details>

## Return

`FT.DROPINDEX` returns a simple string reply `OK` if executed correctly, or an error reply otherwise.

## Examples

<details open>
<summary><b>Delete an index</b></summary>

```bash
dragonfly> FT.DROPINDEX idx DD
OK
```
</details>

## See also

[`FT.CREATE`](./ft.create.md) | [`FT.INFO`](./ft.info.md)
