---
description: "Understand Redis SCRIPT EXISTS command for checking scripts' existence in the cache."
---

import PageTitle from '@site/src/components/PageTitle';

# SCRIPT EXISTS

<PageTitle title="Redis SCRIPT EXISTS Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `SCRIPT EXISTS` command in Redis is used to check if specific Lua scripts are present in the script cache. This command is useful in scenarios where you want to ensure that certain scripts are loaded before attempting to execute them, improving efficiency by avoiding redundant script loading.

## Syntax

```plaintext
SCRIPT EXISTS sha1 [sha1 ...]
```

## Parameter Explanations

- **sha1**: The SHA1 hash of the script to check. Multiple SHA1 values can be specified to check the existence of multiple scripts in one command.

## Return Values

The command returns an array of integers. Each integer corresponds to the SHA1 hashes provided and indicates whether the respective script exists in the cache:

- `1` means the script exists.
- `0` means the script does not exist.

### Example Outputs

```cli
dragonfly> SCRIPT EXISTS e0e1f9fabfc9d4800c877a703b823ac0578ff8db
1) 0
dragonfly> SCRIPT EXISTS e0e1f9fabfc9d4800c877a703b823ac0578ff8db d2ab5dc7ad3dee0a4b1fa243b3d3b8c6b6bc4f73
1) 0
2) 1
```

## Code Examples

```cli
dragonfly> SCRIPT LOAD "return 'Hello, Redis!'"
"e0e1f9fabfc9d4800c877a703b823ac0578ff8db"
dragonfly> SCRIPT EXISTS e0e1f9fabfc9d4800c877a703b823ac0578ff8db
1) 1
dragonfly> SCRIPT EXISTS e0e1f9fabfc9d4800c877a703b823ac0578ff8db d2ab5dc7ad3dee0a4b1fa243b3d3b8c6b6bc4f73
1) 1
2) 0
```

## Best Practices

- Cache frequently-used scripts to reduce redundancy and improve performance.
- Use descriptive comments within your scripts to make debugging easier when checking their presence.

## Common Mistakes

- Providing incorrect or malformed SHA1 hashes will result in erroneous checks. Ensure that the SHA1 hashes are accurate.
- Not loading the script before checking its existence. Always load your scripts first using `SCRIPT LOAD`.

## FAQs

### How do I obtain the SHA1 hash for a Lua script?

When you load a script using the `SCRIPT LOAD` command, Redis returns the SHA1 hash of the script. Use this hash for subsequent checks with `SCRIPT EXISTS`.

### What happens if I try to check a script that has never been loaded?

Redis will simply return `0` for that SHA1 hash in the response array, indicating the script does not exist in the cache.
