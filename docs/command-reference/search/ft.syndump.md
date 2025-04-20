---
description: Dumps the synonyms from an index
---

# FT.SYNDUMP

## Syntax

    FT.SYNDUMP index

**Time complexity:** O(1)

**Important**: New in Dragonfly v1.13. Currently, Dragonfly Search is in **Beta**.

## Description

Dumps all synonym groups that exist in the given index.

## Required arguments

<details open>
<summary><code>index</code></summary>

is index name. You must first create the index using the [`FT.CREATE`](./ft.create.md) command.
</details>

## Return

`FT.SYNDUMP` returns an array of pairs, where the first element of each pair is the synonym group identifier, and the second element is an array of terms belonging to that group.

## Examples

<details open>
<summary><b>Dump synonym groups</b></summary>

```bash
dragonfly> FT.SYNUPDATE idx synonym hello hi shalom
OK
dragonfly> FT.SYNDUMP idx
1) "synonym"
2) 1) "hello"
   2) "hi"
   3) "shalom"
```
</details>

## See also

[`FT.SYNUPDATE`](./ft.synupdate.md)

## Related topics

- [RediSearch](https://redis.io/docs/stack/search)
