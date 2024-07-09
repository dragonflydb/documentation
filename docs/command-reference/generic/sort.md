---
description: "Discover how to use Redis SORT command for sorting elements in list, set or sorted sets."
---

import PageTitle from '@site/src/components/PageTitle';

# SORT

<PageTitle title="Redis SORT Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `SORT` command in Redis is used for sorting the elements in a list, set, or sorted set. This command is particularly useful for organizing and retrieving data in a specific order. Typical scenarios include sorting user scores, timestamps, or any dataset that requires ordered results.

## Syntax

```
SORT key [BY pattern] [LIMIT offset count] [GET pattern [GET pattern ...]] [ASC|DESC] [ALPHA] [STORE destination]
```

## Parameter Explanations

- `key`: The key of the list, set, or sorted set to be sorted.
- `BY pattern`: An optional parameter specifying an external key pattern to sort by.
- `LIMIT offset count`: Optional parameters to limit the number of results returned.
- `GET pattern`: Optional parameter(s) to return additional properties specified by key patterns.
- `ASC|DESC`: Optional parameters to sort in ascending (default) or descending order.
- `ALPHA`: Optional flag to indicate sorting lexicographically rather than numerically.
- `STORE destination`: Optional parameter to store the result in another key instead of returning it.

## Return Values

The return value of the `SORT` command depends on whether the `STORE` option is provided:

- Without `STORE`: Returns a list of sorted elements.
- With `STORE`: Returns the number of elements stored in the destination key.

Example outputs:

- Without `STORE`: `1) "one" 2) "two" 3) "three"`
- With `STORE`: `(integer) 3`

## Code Examples

```cli
dragonfly> RPUSH mylist 3 1 2
(integer) 3
dragonfly> SORT mylist
1) "1"
2) "2"
3) "3"
dragonfly> SORT mylist DESC
1) "3"
2) "2"
3) "1"
dragonfly> SET user:1:name "Alice"
OK
dragonfly> SET user:2:name "Bob"
OK
dragonfly> SET user:3:name "Carol"
OK
dragonfly> SORT mylist BY user:*:name GET user:*:name
1) "Alice"
2) "Bob"
3) "Carol"
dragonfly> SORT mylist LIMIT 0 2
1) "1"
2) "2"
dragonfly> SORT mylist STORE sorted_list
(integer) 3
dragonfly> LRANGE sorted_list 0 -1
1) "1"
2) "2"
3) "3"
```

## Best Practices

- Use the `LIMIT` option to paginate large datasets efficiently.
- When sorting strings, use the `ALPHA` option to ensure correct lexical ordering.

## Common Mistakes

- Sorting a set or sorted set without providing the correct pattern for external keys can lead to unexpected results.
- Omitting the `ALPHA` option when sorting non-numeric strings can cause incorrect ordering.

## FAQs

### How does `BY` work with hash fields?

The `BY` option allows you to sort based on values retrieved from hash fields. For example, if you have hashes representing users, you can sort by a user's age stored in a hash field.

### Can I sort multiple fields at once?

Yes, by using multiple `GET` options, you can retrieve multiple fields, but the sorting itself is based on the primary pattern provided in the `BY` option.

### Is the `SORT` command efficient for large datasets?

The `SORT` command can be computationally expensive for large datasets. It's important to use options like `LIMIT` and consider storing pre-sorted data if performance becomes an issue.
