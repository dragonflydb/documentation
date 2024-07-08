---
description: Learn how to use Redis RPUSHX to append value to a list only if the list exists.
---

import PageTitle from '@site/src/components/PageTitle';

# RPUSHX

<PageTitle title="Redis RPUSHX Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `RPUSHX` command in Redis is used to append a value to the end of a list, but only if the list already exists. This command is useful for maintaining data integrity by ensuring that no new lists are created accidentally. Typical use cases include logging systems where entries are appended to existing logs, or queues where tasks are only added to pre-existing task lists.

## Syntax

```
RPUSHX key value [value ...]
```

## Parameter Explanations

- **key**: The name of the list to which you want to append the value(s). This list must exist; otherwise, the command will have no effect.
- **value [value ...]**: One or more values to append to the list. Multiple values can be appended in a single command, separated by spaces.

## Return Values

- **(integer)**: The length of the list after the `RPUSHX` operation, or 0 if the list does not exist.

### Example:

If the list does not exist:

```cli
dragonfly> RPUSHX mylist "world"
(integer) 0
```

If the list exists:

```cli
dragonfly> RPUSH mylist "hello"
(integer) 1
dragonfly> RPUSHX mylist "world"
(integer) 2
```

## Code Examples

Appending to a non-existent list:

```cli
dragonfly> RPUSHX mylist "item1"
(integer) 0
```

Appending to an existing list:

```cli
dragonfly> RPUSH mylist "start"
(integer) 1
dragonfly> RPUSHX mylist "middle"
(integer) 2
dragonfly> RPUSHX mylist "end"
(integer) 3
dragonfly> LRANGE mylist 0 -1
1) "start"
2) "middle"
3) "end"
```

Appending multiple values:

```cli
dragonfly> RPUSH mylist "initial"
(integer) 1
dragonfly> RPUSHX mylist "one" "two" "three"
(integer) 4
dragonfly> LRANGE mylist 0 -1
1) "initial"
2) "one"
3) "two"
4) "three"
```

## Best Practices

- Ensure the list exists before using `RPUSHX` to avoid unnecessary command executions.
- Use `EXISTS` command to check for list existence if unsure.

## Common Mistakes

- Using `RPUSHX` on a non-existent list, resulting in no elements being added and the return value being 0.

## FAQs

### How is `RPUSHX` different from `RPUSH`?

`RPUSHX` only appends elements if the list already exists, whereas `RPUSH` will create the list if it does not exist.

### Can I append multiple values using `RPUSHX`?

Yes, you can append multiple values in one command by specifying them consecutively.
