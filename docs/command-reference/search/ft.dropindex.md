---
description: Deletes the index
---

# FT.DROPINDEX

## Syntax

    FT.DROPINDEX index

**Time complexity:** O(1)

**Important**: New in Dragonfly v1.13. Currently, Dragonfly Search is in **Beta**.

## Description

Delete an index.

## Required arguments

<details open>
<summary><code>index</code></summary>

is index name. You must first create the index using [`FT.CREATE`](./ft.create.md).
</details>

## Return

`FT.DROPINDEX` returns a simple string reply `OK` if executed correctly, or an error reply otherwise.

## Examples

<details open>
<summary><b>Delete an index</b></summary>

```bash
dragonfly> FT.DROPINDEX idx
OK
```
</details>

## See also

[`FT.CREATE`](./ft.create.md) | [`FT.INFO`](./ft.info.md)

## Related topics

- [RediSearch](https://redis.io/docs/stack/search)
