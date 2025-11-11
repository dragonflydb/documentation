---
description: Configure search engine at runtime
---

# FT.CONFIG

## Syntax

    FT.CONFIG GET pattern
    FT.CONFIG SET option value
    FT.CONFIG HELP [option]

**Time complexity:** O(1)

## Description

Configure search engine at runtime.

## Required arguments

<details open>
<summary><code>GET pattern</code></summary>

returns the current values of configuration parameters matching the given pattern.

`pattern` is a glob-style pattern for the configuration parameter names.
</details>

<details open>
<summary><code>SET option value</code></summary>

sets a configuration parameter to the given value.

`option` is the configuration parameter name.
`value` is the new value for the configuration parameter.
</details>

<details open>
<summary><code>HELP [option]</code></summary>

returns help information about configuration parameters.

If `option` is specified, returns help for that specific parameter.
If no option is given, returns help for all available parameters.
</details>

## Return

- `FT.CONFIG GET` returns an array with parameter names and their values.
- `FT.CONFIG SET` returns a simple string reply `OK` if executed correctly, or an error reply otherwise.
- `FT.CONFIG HELP` returns an array with parameter information including descriptions and current values.

## Examples

<details open>
<summary><b>Get all search configuration parameters</b></summary>

```bash
dragonfly> FT.CONFIG GET *
1) "MAXSEARCHRESULTS"
2) "1000000"
```
</details>

<details open>
<summary><b>Set maximum search results</b></summary>

```bash
dragonfly> FT.CONFIG SET MAXSEARCHRESULTS 500000
OK
```
</details>

<details open>
<summary><b>Get help for a specific parameter</b></summary>

```bash
dragonfly> FT.CONFIG HELP MAXSEARCHRESULTS
1) "MAXSEARCHRESULTS"
2) "Description"
3) "Maximum number of results from ft.search command"
4) "Value"
5) "500000"
```
</details>

## See also

[`FT.CREATE`](./ft.create.md) | [`FT.SEARCH`](./ft.search.md)

## Related topics

- [RediSearch](https://redis.io/docs/latest/operate/oss_and_stack/stack-with-enterprise/search/)
