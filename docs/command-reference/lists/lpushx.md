---
description: Learn to use Redis LPUSHX for prepending a value to a list when list exists.
---

import PageTitle from '@site/src/components/PageTitle';

# LPUSHX

<PageTitle title="Redis LPUSHX Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `LPUSHX` command is used in Redis to insert a value at the head of an existing list. Unlike `LPUSH`, which creates a new list if the specified key does not exist, `LPUSHX` only performs the operation if the list already exists. This command is typically used in scenarios where you want to ensure that you're only adding elements to lists that have already been initialized, avoiding accidental creation of new lists.

## Syntax

```plaintext
LPUSHX key element [element ...]
```

## Parameter Explanations

- **key**: The name of the existing list to which you want to add the element(s).
- **element [element ...]**: One or more values to be added to the head (left side) of the list.

## Return Values

The command returns an integer representing the length of the list after the push operation. If the key does not exist, it returns 0, as no operation is performed.

## Code Examples

```cli
dragonfly> LPUSH mylist "world"
(integer) 1
dragonfly> LPUSHX mylist "hello"
(integer) 2
dragonfly> LPUSHX nonexistinglist "hello"
(integer) 0
dragonfly> LRANGE mylist 0 -1
1) "hello"
2) "world"
```

## Best Practices

When using `LPUSHX`, ensure that the target list has been initialized beforehand. This prevents confusion over whether a list was intended to be created or not.

## Common Mistakes

A common mistake is assuming `LPUSHX` will create a new list if the key does not exist. It strictly operates only on pre-existing lists.

## FAQs

### What happens if I use LPUSHX on an empty key?

The command will return 0, indicating no operation was performed since the key does not exist.

### Can I push multiple elements using LPUSHX?

Yes, you can push multiple elements at once by specifying them in the command. However, they will all be added to the head of the list only if the list exists.
