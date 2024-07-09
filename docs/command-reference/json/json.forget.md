---
description: Know how to use Redis JSON.FORGET command for deleting a key-value pair from a JSON object.
---

import PageTitle from '@site/src/components/PageTitle';

# JSON.FORGET

<PageTitle title="Redis JSON.FORGET Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `JSON.FORGET` command in Redis is used to delete a specified path from a JSON document stored in the database. This command is part of the RedisJSON module, which allows for efficient storage and manipulation of JSON data. Typical scenarios for using `JSON.FORGET` include removing specific fields from JSON objects or deleting entire nested structures within a JSON document.

## Syntax

```plaintext
JSON.FORGET key path
```

## Parameter Explanations

- `key`: The key associated with the JSON document.
- `path`: The JSONPath expression that specifies the location within the JSON document to delete. The root path (`$`) can be used to delete the entire JSON document.

## Return Values

`JSON.FORGET` returns:

- `(integer) 1` if the path was successfully deleted.
- `(integer) 0` if the path did not exist.

## Code Examples

```cli
dragonfly> JSON.SET mydoc $ '{"name":"John", "age":30, "city":"New York"}'
OK
dragonfly> JSON.FORGET mydoc $.age
(integer) 1
dragonfly> JSON.GET mydoc $
"{\"name\":\"John\",\"city\":\"New York\"}"

dragonfly> JSON.FORGET mydoc $.nonexistent
(integer) 0
```

## Best Practices

- Ensure paths are correctly specified to avoid accidentally deleting unintended parts of the JSON document.
- Regularly back up your Redis data to prevent accidental loss of important JSON structures.

## Common Mistakes

- Using an incorrect path that does not match any part of the JSON document, leading to no deletions being performed.
- Forgetting that deleting the root path (`$`) removes the entire JSON document.

## FAQs

### What happens if I use `JSON.FORGET` on a non-existing path?

If you use `JSON.FORGET` on a non-existing path, the command will return `(integer) 0`, indicating that no deletion occurred.

### Can I use `JSON.FORGET` to delete multiple paths at once?

No, `JSON.FORGET` operates on a single path at a time. You need to issue multiple commands to delete multiple paths.
