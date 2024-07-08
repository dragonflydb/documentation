---
description: Learn how to use Redis SELECT command to switch the database for the present connection.
---

import PageTitle from '@site/src/components/PageTitle';

# SELECT

<PageTitle title="Redis SELECT Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `SELECT` command in Redis is used to switch the current connection to a different logical database. Redis supports multiple databases, which are identified by their numeric indices. This command is especially useful when you want to logically separate data within a single Redis instance.

## Syntax

```plaintext
SELECT index
```

## Parameter Explanations

- **index**: The zero-based numeric index of the database to be selected. Redis typically has 16 databases by default, indexed from 0 to 15.

## Return Values

- **OK**: Indicates that the database switch was successful.

### Example

```cli
dragonfly> SELECT 1
OK
dragonfly> SET key "value"
OK
dragonfly> SELECT 0
OK
dragonfly> GET key
(nil)
dragonfly> SELECT 1
OK
dragonfly> GET key
"value"
```

## Code Examples

```cli
dragonfly> SELECT 2
OK
dragonfly> SET mykey "hello"
OK
dragonfly> SELECT 3
OK
dragonfly> GET mykey
(nil)
dragonfly> SELECT 2
OK
dragonfly> GET mykey
"hello"
```

## Common Mistakes

- **Invalid Index**: Trying to select a database index that does not exist will result in an error. Ensure the index is within the configured range.

### Example

```cli
dragonfly> SELECT 16
(error) ERR DB index is out of range
```

## FAQs

### How many databases can I have in Redis?

By default, Redis allows 16 databases (indexed 0-15), but this can be changed in the configuration file (`redis.conf`) by setting the `databases` directive.

### Can different connections use different databases simultaneously?

Yes, each connection can select its own database independently of other connections.
