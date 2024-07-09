---
description: Learn how to use Redis `JSON.DEBUG FIELDS` to get the field names in a JSON object for efficient debugging.
---

import PageTitle from '@site/src/components/PageTitle';

# JSON.DEBUG FIELDS

<PageTitle title="Redis `JSON.DEBUG FIELDS` Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`JSON.DEBUG FIELDS` is a command in Redis designed to provide debugging information about the structure of JSON documents stored in Redis. It gives insights into the fields present within a JSON document, which can be particularly useful during development or troubleshooting.

Typical scenarios include:

- Understanding the structure of complex JSON documents.
- Debugging issues related to missing or unexpected fields in JSON objects.
- Verifying the integrity and completeness of JSON data stored in Redis.

## Syntax

```cli
JSON.DEBUG FIELDS key
```

## Parameter Explanations

- `key`: The key associated with the JSON document for which you want to retrieve field information. It must be a valid string corresponding to an existing key in the database.

## Return Values

The command returns an array of strings, each representing a field name within the specified JSON document.

### Example outputs:

- If the JSON document has fields "name", "age", and "address", the output might be:

  ```cli
  1) "name"
  2) "age"
  3) "address"
  ```

- For an empty or non-existent JSON document, it will return an empty array.

## Code Examples

```cli
dragonfly> JSON.SET myjson . '{"name":"John", "age":30, "city":"New York"}'
OK
dragonfly> JSON.DEBUG FIELDS myjson
1) "name"
2) "age"
3) "city"

dragonfly> JSON.SET anotherjson . '{"product":"Book", "price":15}'
OK
dragonfly> JSON.DEBUG FIELDS anotherjson
1) "product"
2) "price"

dragonfly> JSON.SET emptyjson . '{}'
OK
dragonfly> JSON.DEBUG FIELDS emptyjson
(empty array)
```

## Best Practices

- Use `JSON.DEBUG FIELDS` during development to verify that your JSON documents contain all expected fields before proceeding with application logic.
- Combine `JSON.DEBUG FIELDS` with other JSON commands like `JSON.GET` to dynamically adjust your application behavior based on the existence of certain fields.

## Common Mistakes

- Attempting to use `JSON.DEBUG FIELDS` on keys that do not store JSON documents will result in an error. Ensure that the key indeed contains a JSON value before using this command.

## FAQs

### What happens if I use `JSON.DEBUG FIELDS` on a non-JSON key?

Using `JSON.DEBUG FIELDS` on a key that does not store a JSON document will result in a type error. Always ensure the key refers to a JSON structure.

### Can `JSON.DEBUG FIELDS` handle deeply nested JSON structures?

`JSON.DEBUG FIELDS` only provides the top-level fields of the JSON document. For deeper insights, you will need to access nested objects individually.
