---
description: Deletes the index
---

import PageTitle from '@site/src/components/PageTitle';

# FT.DROPINDEX

<PageTitle title="Redis FT.DROPINDEX Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`FT.DROPINDEX` is a command in Redis used to delete an index created by the RedisSearch module. This command is essential when you need to remove an outdated or unnecessary index to free up resources or to reconfigure your indexing strategy. Typical scenarios include database maintenance, schema migrations, and clean-up operations.

## Syntax

```plaintext
FT.DROPINDEX index_name [DD]
```

## Parameter Explanations

- `index_name`: The name of the index to drop. This parameter is required.
- `DD`: Optional flag that indicates the associated document hashes should also be deleted if they are not referenced by other indexes.

## Return Values

The command returns a simple string reply:

- `"OK"` if the index was successfully dropped.
- An error message if the operation fails, such as when the specified index does not exist.

## Code Examples

```cli
dragonfly> FT.CREATE myIdx SCHEMA title TEXT WEIGHT 5.0 body TEXT
OK
dragonfly> FT.SEARCH myIdx "hello"
1) (integer) 0
dragonfly> FT.DROPINDEX myIdx
OK
dragonfly> FT.SEARCH myIdx "hello"
(error) Unknown Index name
dragonfly> FT.CREATE anotherIdx SCHEMA title TEXT WEIGHT 5.0 body TEXT
OK
dragonfly> FT.DROPINDEX anotherIdx DD
OK
```

## Best Practices

- Always ensure that dropping an index will not disrupt your application's functionality.
- Use the `DD` flag cautiously, as it will delete documents that might be referenced by other indexes.

## Common Mistakes

- Forgetting to specify the correct index name can lead to errors, make sure you spell the index name correctly.
- Using the `DD` flag without understanding its impact could result in unintended data loss.

## FAQs

### What happens if I drop an index without using the `DD` flag?

If you drop an index without the `DD` flag, the index is removed, but the documents remain in the database.

### Can I recover an index after dropping it?

No, once an index is dropped, it cannot be recovered. You would need to recreate the index and reindex the documents.
