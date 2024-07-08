---
description: Learn how to use Redis DBSIZE command to fetch the number of keys in the current database.
---

import PageTitle from '@site/src/components/PageTitle';

# DBSIZE

<PageTitle title="Redis DBSIZE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `DBSIZE` command in Redis is used to return the number of keys in the currently selected database. This command is particularly useful for monitoring purposes, allowing administrators to understand the size of a database at any given time. It can be used in scenarios where you need to keep an eye on the key count to manage memory usage or plan database scaling.

## Syntax

```
DBSIZE
```

## Parameter Explanations

The `DBSIZE` command does not take any parameters. It simply counts the keys in the currently selected database.

## Return Values

The return value for the `DBSIZE` command is an integer that represents the number of keys in the current database.

Example:

- If the database contains 5 keys, the command will return `(integer) 5`.

## Code Examples

```cli
dragonfly> SET key1 "value1"
OK
dragonfly> SET key2 "value2"
OK
dragonfly> DBSIZE
(integer) 2
dragonfly> DEL key1
(integer) 1
dragonfly> DBSIZE
(integer) 1
```

## Best Practices

- Use `DBSIZE` sparingly in production environments with very large databases, as counting keys can be an expensive operation.
- Consider using `INFO` command for more extensive monitoring and insights into your Redis instance.

## Common Mistakes

- Forgetting that `DBSIZE` only counts keys in the currently selected database, which could lead to misunderstandings if multiple databases are in use.
- Using `DBSIZE` frequently in scripts could impact performance due to its O(N) complexity, where N is the number of keys.

## FAQs

### What is the time complexity of the DBSIZE command?

The `DBSIZE` command has a time complexity of O(N), where N is the number of keys in the database.

### Does DBSIZE reflect expired keys?

No, `DBSIZE` does not include expired keys that have been lazily removed. It only counts the keys that are currently active in the database.
