---
description: Learn how to use Redis JSON.STRLEN to measure the length of a string in a JSON document.
---

import PageTitle from '@site/src/components/PageTitle';

# JSON.STRLEN

<PageTitle title="Redis JSON.STRLEN Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`JSON.STRLEN` is a Redis command used with the RedisJSON module to determine the length of a JSON string at a specified path within a JSON document. This can be particularly useful for validating data sizes, enforcing length constraints, or optimizing storage by understanding the size of JSON values.

## Syntax

```plaintext
JSON.STRLEN <key> <path>
```

## Parameter Explanations

- `<key>`: The key in Redis that holds the JSON document.
- `<path>`: The JSONPath expression indicating the location of the string within the JSON document. This should point directly to a string value.

## Return Values

The command returns an integer representing the length of the JSON string at the specified path.

### Examples:

- If the string's length is 10, it returns `(integer) 10`.
- If the path does not exist or does not point to a string, it returns `nil`.

## Code Examples

```cli
dragonfly> JSON.SET mydoc $ '{"name": "John", "age": 30, "city": "New York"}'
OK
dragonfly> JSON.STRLEN mydoc $.name
(integer) 4
dragonfly> JSON.STRLEN mydoc $.city
(integer) 8
dragonfly> JSON.STRLEN mydoc $.age
(nil)
```

## Best Practices

- Ensure the path points directly to a string; otherwise, the command will return `nil`.
- Use this command to validate input lengths when dealing with user-generated content to enforce maximum allowed sizes.

## Common Mistakes

- Providing a path that leads to a non-string element such as an object, array, or number will result in a `nil` return value.
- Using incorrect JSONPath syntax might lead to unexpected results or errors.

## FAQs

### What happens if the provided path does not exist?

If the path does not exist or does not point to a valid string, `JSON.STRLEN` returns `nil`.

### Can I use JSON.STRLEN on nested JSON strings?

Yes, you can use JSON.STRLEN on nested JSON strings by providing the correct JSONPath to the string.
