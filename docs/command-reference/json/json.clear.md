---
description: Learn how to use Redis JSON.CLEAR command to delete all the keys from a JSON object.
---

import PageTitle from '@site/src/components/PageTitle';

# JSON.CLEAR

<PageTitle title="Redis JSON.CLEAR Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `JSON.CLEAR` command in Redis is used to clear the contents of an existing JSON value. This command is particularly useful when you want to reset a JSON object or array without removing the key itself. Typical scenarios include resetting the state of complex data structures or preparing a JSON object for new data while preserving its schema.

## Syntax

```cli
JSON.CLEAR <key> [path]
```

## Parameter Explanations

- **key**: The key holding the JSON value to be cleared.
- **path**: (Optional) A JSONPath expression specifying the part of the JSON value to clear. If omitted, the entire JSON value is cleared.

## Return Values

- **(Integer)**: Returns the number of paths that were cleared.

Example:

```cli
(integer) 1
```

## Code Examples

```cli
dragonfly> JSON.SET myjson . '{"name":"John", "age":30, "cars":["Ford", "BMW", "Fiat"]}'
OK
dragonfly> JSON.GET myjson
"{\"name\":\"John\",\"age\":30,\"cars\":[\"Ford\",\"BMW\",\"Fiat\"]}"
dragonfly> JSON.CLEAR myjson .cars
(integer) 1
dragonfly> JSON.GET myjson
"{\"name\":\"John\",\"age\":30,\"cars\":[]}"
dragonfly> JSON.CLEAR myjson .
(integer) 1
dragonfly> JSON.GET myjson
"{}"
```

## Best Practices

- Use specific JSONPath expressions to clear only the necessary parts of your JSON data, thus avoiding unintended data loss.
- Ensure you understand the structure of your JSON before using the `JSON.CLEAR` command to prevent clearing crucial data inadvertently.

## Common Mistakes

- Omitting the path when it's needed: Without specifying the correct path, you might unintentionally clear the entire JSON content.
- Using incorrect or unsupported JSONPath expressions can result in errors or no action at all.

## FAQs

### What happens if I clear a non-existent path?

If you attempt to clear a path that does not exist, the command will return `(integer) 0`, indicating no paths were cleared.

### Does clearing a JSON value delete the key?

No, `JSON.CLEAR` only resets the JSON value or specified path within the JSON structure. The key itself remains in the database.

### Can I undo a JSON.CLEAR operation?

No, once the data is cleared, it cannot be retrieved unless you have a prior backup or log of the data.
