---
description: Learn how to use Redis REPLCONF command for assisting in the replication process.
---

import PageTitle from '@site/src/components/PageTitle';

# REPLCONF

<PageTitle title="Redis REPLCONF Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`REPLCONF` is a command used in Redis replication to configure settings for the replication link between a master and its replicas. It is typically employed during the initial synchronization process or when changing runtime parameters of the replication link. Scenarios include adjusting buffer sizes, setting offsets, and managing acknowledgments.

## Syntax

```cli
REPLCONF <option> [value]
```

## Parameter Explanations

- `option`: The configuration option to set. Common options include:

  - `listening-port`: Sets the port on which the replica listens.
  - `ack`: Acknowledges the receipt of replication data up to a specified offset.
  - `getack`: Requests an acknowledgment from the replica.

- `value`: The value to be assigned to the given option. This varies based on the chosen option.

## Return Values

The return value of `REPLCONF` depends on the specific option used:

- For `ack` and `getack` options, it typically returns an `OK` if successful.
- Invalid options or values generate error messages.

Example:

```cli
dragonfly> REPLCONF listening-port 6380
OK
dragonfly> REPLCONF ack 12345
OK
```

## Code Examples

```cli
dragonfly> REPLCONF listening-port 6380
OK
dragonfly> REPLCONF ack 12345
OK
dragonfly> REPLCONF getack
(null)
```

## Best Practices

- Ensure you understand the exact role each replication configuration parameter plays in your high availability setup.
- Use `REPLCONF` to fine-tune replication performance and reliability based on your network characteristics.

## Common Mistakes

### Using Incorrect Option Names

Using an unsupported or misspelled option name will result in an error. Always refer to official documentation for supported options.

```cli
dragonfly> REPLCONF unkown-option 1234
(error) ERR unknown option 'unkown-option'
```

### Incorrect Value Types

Providing values that do not match the expected type or format for a given option can also lead to errors. Make sure the values align with what the option expects.

## FAQs

### What happens if I use an unknown option?

Redis will return an error indicating that the option is unknown.

### Can `REPLCONF` be used by normal clients?

No, it is intended for internal replication management and should be used within the context of Redis' built-in replication mechanisms.
