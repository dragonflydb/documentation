---
description: "Explore the Redis TYPE command for finding a key's data type."
---

import PageTitle from '@site/src/components/PageTitle';

# TYPE

<PageTitle title="Redis TYPE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `TYPE` command in Redis is used to determine the data type stored at a specific key. This is particularly useful when working with multiple types of data structures (strings, lists, sets, hashes, etc.) in Redis, as it allows you to confirm the type of value before performing type-specific operations.

## Syntax

```plaintext
TYPE key
```

## Parameter Explanations

- **key**: The key whose data type you want to determine. The key must be specified exactly as it's stored in the Redis database.

## Return Values

The command returns a string representing the type of the value stored at the given key. Possible return values include:

- `"string"`: The key stores a string value.
- `"list"`: The key stores a list.
- `"set"`: The key stores a set.
- `"zset"`: The key stores a sorted set.
- `"hash"`: The key stores a hash.
- `"stream"`: The key stores a stream.
- `"none"`: The key does not exist.

## Code Examples

```cli
dragonfly> SET mykey "Hello"
OK
dragonfly> TYPE mykey
string

dragonfly> LPUSH mylist "World"
(integer) 1
dragonfly> TYPE mylist
list

dragonfly> HSET myhash field1 "value1"
(integer) 1
dragonfly> TYPE myhash
hash

dragonfly> TYPE nonexistingkey
none
```

## Best Practices

When dealing with dynamic or unknown keys in your application, always use the `TYPE` command to check the data type before performing any operations. This helps avoid errors caused by attempting incompatible actions on the wrong data type.

## Common Mistakes

- **Assuming types**: Never assume the data type of a key without checking it first. Different parts of an application or different applications might use the same key for different purposes.
- **Nonexistent keys**: Accessing the type of a nonexistent key will return `"none"`. Make sure to handle this case appropriately in your code.

## FAQs

### What happens if I call `TYPE` on a key that doesn't exist?

If you call `TYPE` on a key that doesn't exist, the command will return `"none"`.

### Can `TYPE` help prevent errors in my application?

Yes, using `TYPE` to check the data type before performing operations can help prevent errors such as trying to push elements into a string or incrementing a list.
