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

## Available Parameters

DragonflyDB supports the following search configuration parameters:

- **MAXSEARCHRESULTS** - Maximum number of results from ft.search command. Default: `1000000`
- **search.query-string-bytes** - Maximum number of bytes in search query string. Default: `10240`

## Return

- `FT.CONFIG GET` returns an array with parameter names and their values in MAP format.
- `FT.CONFIG SET` returns a simple string reply `OK` if executed correctly, or an error reply otherwise.
- `FT.CONFIG HELP` returns an array of arrays, where each inner array contains 5 elements: parameter name, the string "Description", parameter description, the string "Value", and current value.

## Examples

<details open>
<summary><b>Get all search configuration parameters</b></summary>

```bash
dragonfly> FT.CONFIG GET *
1) "MAXSEARCHRESULTS"
2) "1000000"
3) "search.query-string-bytes"
4) "10240"
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

<details open>
<summary><b>Get a specific configuration parameter</b></summary>

```bash
dragonfly> FT.CONFIG GET search.query-string-bytes
1) "search.query-string-bytes"
2) "10240"
```
</details>

<details open>
<summary><b>Set query string size limit</b></summary>

```bash
dragonfly> FT.CONFIG SET search.query-string-bytes 20480
OK
```
</details>

<details open>
<summary><b>Get help for all parameters</b></summary>

```bash
dragonfly> FT.CONFIG HELP *
1) 1) "MAXSEARCHRESULTS"
   2) "Description"
   3) "Maximum number of results from ft.search command"
   4) "Value"
   5) "1000000"
2) 1) "search_query_string_bytes"
   2) "Description"
   3) "Maximum number of bytes in search query string"
   4) "Value"
   5) "10240"
```
</details>

## See also

[`FT.CREATE`](./ft.create.md) | [`FT.SEARCH`](./ft.search.md)

## Related topics

- [RediSearch](https://redis.io/docs/latest/operate/oss_and_stack/stack-with-enterprise/search/)
