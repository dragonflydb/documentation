---
description: "Use Redis SCRIPT HELP command to understand script debugging capabilities."
---

import PageTitle from '@site/src/components/PageTitle';

# SCRIPT HELP

<PageTitle title="Redis SCRIPT HELP Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `SCRIPT HELP` command in Redis provides helpful information about the available scripting commands. It is used mainly for obtaining a brief description of other script-related commands, which can be particularly useful when working with Lua scripts in Redis.

## Syntax

```plaintext
SCRIPT HELP
```

## Parameter Explanations

The `SCRIPT HELP` command does not take any parameters. It is straightforward and serves a single purpose: to display help information.

## Return Values

The command returns an array of strings, where each string is a line of the help documentation. Here is an example of possible output:

```plaintext
1) "SCRIPT LOAD script"
2) "Load the specified Lua script into the script cache."
3) ""
4) "SCRIPT EXISTS sha1 [sha1 ...]"
5) "Check existence of scripts in the script cache."
6) ...
```

## Code Examples

```cli
dragonfly> SCRIPT HELP
1) "SCRIPT LOAD script"
2) "Load the specified Lua script into the script cache."
3) ""
4) "SCRIPT EXISTS sha1 [sha1 ...]"
5) "Check existence of scripts in the script cache."
6) "..."
```

## Best Practices

When using Redis scripting, familiarize yourself with the different scripting commands by periodically checking `SCRIPT HELP`. This ensures you are aware of all available functionalities and can use them efficiently.

## Common Mistakes

### Misunderstanding Command Purpose

Users might expect `SCRIPT HELP` to provide detailed usage instructions for writing Lua scripts. Instead, it only lists available script-related commands and their brief descriptions.

### Parameter Expectation

Attempting to pass parameters to `SCRIPT HELP` will result in an error. The command should be used without any arguments.

## FAQs

### What is the primary use of `SCRIPT HELP`?

`SCRIPT HELP` is used to display a list of available scripting commands and their brief descriptions in Redis.

### Can `SCRIPT HELP` be used with arguments?

No, `SCRIPT HELP` does not accept any arguments. It simply displays help information for scripting commands.
