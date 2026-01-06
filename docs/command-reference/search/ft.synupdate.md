---
description: Creates or updates a synonym group
---

# FT.SYNUPDATE

## Syntax

    FT.SYNUPDATE index synonym_group_id
      [SKIPINITIALSCAN] term [term ...]

**Time complexity:** O(N)

## Description

Creates or updates a synonym group with additional terms. By default, the command triggers a scan of all documents.

## Required arguments

<details open>
<summary><code>index</code></summary>

is index name. You must first create the index using the [`FT.CREATE`](./ft.create.md) command.
</details>

<details open>
<summary><code>synonym_group_id</code></summary>

is the identifier of the synonym group to create or update.
</details>

<details open>
<summary><code>term [term ...]</code></summary>

one or more terms to be added to the synonym group.
</details>

## Optional arguments

<details open>
<summary><code>SKIPINITIALSCAN</code></summary>

This argument is not supported in Dragonfly and is silently ignored.

:::note
SKIPINITIALSCAN is included for compatibility with Redis, but has no effect in Dragonfly.
:::
</details>

## Return

`FT.SYNUPDATE` returns a simple string reply `OK` if executed correctly, or an error reply otherwise.

## Examples

<details open>
<summary><b>Update a synonym group</b></summary>

```bash
dragonfly> FT.SYNUPDATE idx synonym hello hi shalom
OK
```

```bash
dragonfly> FT.SYNUPDATE idx synonym SKIPINITIALSCAN hello hi shalom
OK
```
</details>

## See also

[`FT.SYNDUMP`](./ft.syndump.md)

## Related topics

- [RediSearch](https://redis.io/docs/latest/operate/oss_and_stack/stack-with-enterprise/search/)
