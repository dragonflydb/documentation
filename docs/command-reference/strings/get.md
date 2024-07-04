---
description: Discover how to use Redis GET for fetching the value of a defined key.
---

import PageTitle from '@site/src/components/PageTitle';

# GET

<PageTitle title="Redis GET Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `GET` command in Redis is used to retrieve the value of a specified key. This command is essential for reading string data stored in Redis. Typical scenarios include fetching user session data, retrieving cached content, or reading configuration settings.

## Syntax

```plaintext
GET key
```

## Parameter Explanations

- **key**: The name of the key whose value you want to retrieve. It must be a string and should exist in the Redis database; otherwise, a nil reply is returned.

## Return Values

The `GET` command returns the value associated with the given key. If the key does not exist, it returns `(nil)`.

Examples:

- If the key exists: `"value"`
- If the key does not exist: `(nil)`

## Code Examples

```cli
dragonfly> SET mykey "Hello"
OK
dragonfly> GET mykey
"Hello"
dragonfly> GET nonexistingkey
(nil)
```

## Best Practices

- Ensure that the keys you are trying to get actually exist to avoid unnecessary nil responses.
- Use appropriate serialization techniques when storing complex data structures as strings.

## Common Mistakes

- Using `GET` on a key that stores non-string data types can lead to errors.
- Not handling the nil response properly, which can cause issues in your application logic.

## FAQs

### What happens if the key does not exist?

If the specified key does not exist, the `GET` command returns `(nil)`.

### Can I use `GET` with non-string data types?

No, `GET` is designed to work with string values. Using it with other data types like lists or hashes will result in an error.
