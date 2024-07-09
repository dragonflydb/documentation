---
description: "Get insights on using Redis RESTORE command to create key using serialized value."
---

import PageTitle from '@site/src/components/PageTitle';

# RESTORE

<PageTitle title="Redis RESTORE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `RESTORE` command in Redis is used to deserialize a binary-serialized value (obtained from the `DUMP` command) back into a key. This command is useful for restoring backups, migrating data between different Redis instances, or transferring data across environments.

## Syntax

```cli
RESTORE key ttl serialized-value [REPLACE] [ABSTTL] [IDLETIME seconds] [FREQ frequency]
```

## Parameter Explanations

- **key**: The name of the key where the deserialized value will be stored.
- **ttl**: Time-to-live for the key in milliseconds. Use 0 if the key should not expire.
- **serialized-value**: The binary data representing the serialized value.
- **REPLACE** (optional): If specified, it will replace any existing value with the same key.
- **ABSTTL** (optional): Uses absolute Unix timestamp for TTL instead of relative TTL.
- **IDLETIME seconds** (optional): Sets the idle time for the key.
- **FREQ frequency** (optional): Sets the access frequency for the key.

## Return Values

- **OK**: Indicates successful restoration.
- **Errors**: Could return errors such as `(error) ERR DUMP payload version or checksum are wrong`, indicating issues with the serialized data.

## Code Examples

```cli
dragonfly> DUMP mykey
"\x00\xc0\n\x06myvalue\x06\x00\xff"
dragonfly> DEL mykey
(integer) 1
dragonfly> RESTORE mykey 0 "\x00\xc0\n\x06myvalue\x06\x00\xff"
OK
dragonfly> GET mykey
"myvalue"
dragonfly> RESTORE newkey 1000 "\x00\xc0\n\x06newvalue\x06\x00\xff" REPLACE
OK
dragonfly> TTL newkey
(integer) -2
```

## Best Practices

- Use the `REPLACE` option cautiously to avoid unintentional data overwrites.
- Ensure that the `serialized-value` is correctly obtained from a reliable source to prevent data corruption.

## Common Mistakes

- Using an incorrect `serialized-value` format resulting in checksum errors.
- Not specifying `REPLACE` when intending to overwrite an existing key, leading to operation failure.

## FAQs

### What does the `ttl` parameter do?

The `ttl` parameter sets the expiration time for the restored key in milliseconds. A `ttl` value of 0 means the key will not expire.

### Can I use `RESTORE` to migrate data between different Redis versions?

Yes, but ensure compatibility between versions, as some changes or deprecations might affect the serialization format.
