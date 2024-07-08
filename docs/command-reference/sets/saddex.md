---
description: Learn how to use Redis SADDEX command adding in a value only if it does not exist.
---

import PageTitle from '@site/src/components/PageTitle';

# SADDEX

<PageTitle title="Redis SADDEX Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `SADDEX` command is used to add a member to a set stored at the specified key if and only if the member does not already exist in any given sets. This command can be particularly useful in scenarios where you need to ensure uniqueness of an element across multiple sets before adding it to the target set.

## Syntax

```cli
SADDEX targetset sourcekey1 [sourcekey2 ...] member
```

## Parameter Explanations

- **targetset**: The key of the set where the member will be added.
- **sourcekey1, sourcekey2, ...**: One or more keys of the sets that are checked for the existence of the member.
- **member**: The member to be added to the `targetset`.

## Return Values

This command returns an integer:

- `1` if the member was successfully added to the `targetset`.
- `0` if the member already exists in any of the source sets or in the `targetset`.

## Code Examples

```cli
dragonfly> SADD myset1 "one"
(integer) 1
dragonfly> SADD myset2 "two"
(integer) 1
dragonfly> SADD myset3 "three"
(integer) 1
dragonfly> SADDEX mytargetset myset1 myset2 "one"
(integer) 0
dragonfly> SADDEX mytargetset myset1 myset2 "four"
(integer) 1
dragonfly> SMEMBERS mytargetset
1) "four"
```

## Best Practices

To use `SADDEX` efficiently:

- Organize your sets so that checks against redundant or unnecessary sets are minimized.
- Use it when unique constraints across multiple sets are necessary.

## Common Mistakes

- Not specifying multiple source sets correctly can lead to unexpected results. Ensure all source sets are listed after the `targetset` and before the `member`.
- Using `SADDEX` without understanding its atomicity can lead to partially applied states if not used with caution in concurrent environments.

---

## FAQs

### What happens if the target set does not exist?

If the `targetset` does not exist, it will be created automatically, and the member will be added.

### Can `SADDEX` be used with non-set data types?

No, `SADDEX` is specifically designed for set data types. Attempting to use it with non-set data types will result in an error.
