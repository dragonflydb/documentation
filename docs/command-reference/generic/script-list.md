---
description: "Learn how to use Redis SCRIPT LIST to return a list of issued script commands."
---

import PageTitle from '@site/src/components/PageTitle';

# SCRIPT LIST

<PageTitle title="Redis SCRIPT LIST Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `SCRIPT LIST` command in Redis is used to list all scripts that are currently cached in the Redis instance. This is particularly useful for managing and debugging Lua scripts in environments where scripting is extensively used.

## Syntax

```cli
SCRIPT LIST
```

## Parameter Explanations

This command does not take any parameters. It simply lists all the SHA1 digests of the scripts that are currently loaded into the script cache.

## Return Values

The `SCRIPT LIST` command returns an array of SHA1 digests of all the cached scripts.

Example output:

```cli
1) "c0e620fa29ac6ca15670913eb8b3d7e4d78068b6"
2) "d5939dcf3cf7e013a5a341b314c8a3e2c7ba0627"
```

## Code Examples

```cli
dragonfly> SCRIPT LOAD "return 'Hello World'"
"c0e620fa29ac6ca15670913eb8b3d7e4d78068b6"
dragonfly> SCRIPT LIST
1) "c0e620fa29ac6ca15670913eb8b3d7e4d78068b6"
dragonfly> SCRIPT LOAD "return 42"
"d5939dcf3cf7e013a5a341b314c8a3e2c7ba0627"
dragonfly> SCRIPT LIST
1) "c0e620fa29ac6ca15670913eb8b3d7e4d78068b6"
2) "d5939dcf3cf7e013a5a341b314c8a3e2c7ba0627"
```

## Best Practices

- Regularly list and manage your cached scripts to avoid clutter and ensure you are not accidentally running outdated or unnecessary scripts.
- Use descriptive comments within your scripts to help identify which script corresponds to each SHA1 digest.

## Common Mistakes

- Not tracking the corresponding Lua code for each SHA1 digest can lead to confusion when trying to debug or update scripts.

## FAQs

### How can I remove a script from the cache?

Use the `SCRIPT FLUSH` command to remove all scripts from the cache or `SCRIPT KILL` to kill the currently executing script, if necessary.

### What happens if I load the same script multiple times?

Loading the same script multiple times will result in the same SHA1 digest being returned, indicating that the script is already cached.
