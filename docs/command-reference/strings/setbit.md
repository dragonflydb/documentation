---
description: Learn about Redis SETBIT to manipulate specific binary bits of a string value.
---

import PageTitle from '@site/src/components/PageTitle';

# SETBIT

<PageTitle title="Redis SETBIT Explained (Better Than Official Docs)" />

## Introduction

The `SETBIT` command in Redis is utilized for setting or clearing the bit at a specified offset in a string value. This command is essential for tasks that require bit-level operations such as bitmap indexing, feature flags, and tracking user activity.

## Syntax

```plaintext
SETBIT key offset value
```

## Parameter Explanations

- **key**: The name of the key holding the string where the bit operation will be performed.
- **offset**: The zero-based position in the string where the bit is to be set or cleared.
- **value**: The bit value to set (0 or 1).

## Return Values

The `SETBIT` command returns the original bit value located at the specified offset before it was modified.

#### Example Outputs

```cli
(integer) 0  // The previous bit value was 0
(integer) 1  // The previous bit value was 1
```

## Code Examples

### Basic Example

Set a bit in a key and retrieve its previous value:

```cli
dragonfly> SETBIT mykey 7 1
(integer) 0
dragonfly> SETBIT mykey 7 0
(integer) 1
```

### Feature Flags

Use `SETBIT` to toggle a feature flag for a user:

```cli
dragonfly> SETBIT user:1001:flags 3 1    // Enable feature flag at position 3
(integer) 0
dragonfly> SETBIT user:1001:flags 3 0    // Disable feature flag at position 3
(integer) 1
```

### User Activity Tracking

Track daily login activities using a bitmap:

```cli
dragonfly> SETBIT user:1001:logins 192 1  // Mark login on day 193
(integer) 0
dragonfly> GETBIT user:1001:logins 192   // Check if the user logged in on day 193
(integer) 1
```

## Best Practices

- Ensure that offsets are within the range of the string length to avoid unexpected behavior.
- Utilize bitmaps for tasks requiring minimal storage and high efficiency in boolean state tracking.

## Common Mistakes

- Using non-integer values for the offset or bit value.
- Assuming that the `SETBIT` command can create keys with types other than strings.

## FAQs

### What happens if the offset is beyond the current length of the string?

Redis automatically extends the string with zero bits to accommodate the offset.

### Can I use `SETBIT` on non-string data types?

No, `SETBIT` is only applicable to string keys.
