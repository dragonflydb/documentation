---
description:  Discover how to use Redis GET for fetching the value of a defined key.
---

import PageTitle from '@site/src/components/PageTitle';

# GET

<PageTitle title="Redis GET Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `GET` command is used to retrieve the value of a key.
This is one of the fundamental commands for interacting with string data types and serves as the counterpart to the `SET` command.
It is widely used in caching layers, configuration storage, and other situations where key-value data access is needed.

## Syntax

```shell
GET key
```

## Parameter Explanations

- `key`: The key whose associated value will be retrieved. If the key holds a value other than a string, an error is returned.

## Return Values

- If the key exists, `GET` returns the value associated with it as a string.
- If the key does not exist, `nil` is returned.

## Code Examples

### Basic Example

Retrieve the value of a key:

```shell
dragonfly> SET mykey "Hello, Dragonfly!"
OK
dragonfly> GET mykey
"Hello, Dragonfly!"
```

### Non-Existent Key

If the key does not exist, `GET` will return `nil`:

```shell
dragonfly> GET non_existent_key
(nil)
```

### Overwriting a Key

Setting and then retrieving the updated value of a key:

```shell
dragonfly> SET counter "5"
OK
dragonfly> GET counter
"5"
dragonfly> SET counter "10"
OK
dragonfly> GET counter
"10"
```

### Storing JSON-like Data

In Dragonfly, Redis, or Valkey, the string data type is binary-safe.
This means that you can store ASCII strings, unicode strings, or even binary data like an image using the string data type.
For instance, you can store JSON-encoded values to model more complex and structured data:

```shell
dragonfly> SET user:1001 '{"name": "Alice", "age": 30, "country": "Wonderland"}'
OK
dragonfly> GET user:1001
"{\"name\": \"Alice\", \"age\": 30, \"country\": \"Wonderland\"}"
```

You can decode this string in your application using your favorite JSON library.

### Binary Data Retrieval

`GET` also works for values that contain binary data:

```shell
dragonfly> SET binary_data "\x00\x01\x02\x03"
OK
dragonfly> GET binary_data
"\x00\x01\x02\x03"
```

## Best Practices

- Use the `GET` command in combination with `SET` to implement caching mechanisms and session storage efficiently.
- Ensure keys are named using a consistent, readable convention to avoid key collisions and enhance code readability. For example, `user:1001:first_name` rather than `user1001`.

## Common Mistakes

- Providing a key name that has not been set. This will result in a return of `nil`, which some developers may not expect.
- Using `GET` on a key that holds a non-string data type like lists, sets, or hashes—which will result in an error (`WRONGTYPE Operation against a key holding the wrong kind of value`).

## FAQs

### What happens if the key does not exist?

If the key does not exist, `GET` returns `nil`. It does not return an empty string or an error.

### Can I use the `GET` command to retrieve values from non-string data types?

No, the `GET` command is specifically for strings. If used on a key that holds a different data type (e.g., a list or a hash), a `WRONGTYPE` error will be raised.