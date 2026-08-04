---
description: Learn how to use the CF.INSERT command to add multiple items to a Cuckoo filter in Dragonfly.
---
import PageTitle from '@site/src/components/PageTitle';

# CF.INSERT

<PageTitle title="CF.INSERT Command (Documentation) | Dragonfly" />

## Syntax

    CF.INSERT key [CAPACITY capacity] [NOCREATE] ITEMS item [item ...]

**Time complexity:** O(k * n), where k is the number of sub-filters and n is the number of items

**ACL categories:** @cuckoo_filter, @slow, @write

Adds one or more items to the Cuckoo filter at `key`, creating it first if it doesn't exist.

Like [`CF.ADD`](./cf.add.md), duplicate insertions are allowed.

## Parameters

| Parameter    | Default | Description                                                                                   |
|--------------|---------|-------------------------------------------------------------------------------------------------|
| `key`        |         | The name of the filter.                                                                        |
| `CAPACITY`   | `1024`  | Initial capacity to use if the filter is created by this command. Ignored if `key` already exists. |
| `NOCREATE`   |         | If set, the filter must already exist; otherwise an error is returned instead of creating it.  |
| `ITEMS`      |         | One or more items to add. Required.                                                            |

## Return

[Array reply](https://valkey.io/topics/protocol/#arrays) of [Integer replies](https://valkey.io/topics/protocol/#integers), one per item, in the same order as the input:

- `1` if the item was successfully added.
- `-1` if the filter is full and the item could not be added.

[Error reply](https://valkey.io/topics/protocol/#simple-errors): if `NOCREATE` is set and `key` does not exist, or `CAPACITY` is `0`.

## Examples

```shell
dragonfly> CF.INSERT cf ITEMS Hello World
1) (integer) 1
2) (integer) 1

dragonfly> CF.INSERT cf CAPACITY 500 ITEMS foo
1) (integer) 1

dragonfly> CF.INSERT cf NOCREATE ITEMS bar
1) (integer) 1

dragonfly> CF.INSERT no_such_key NOCREATE ITEMS bar
(error) ERR no such key
```

## See also

[`CF.INSERTNX`](./cf.insertnx.md) | [`CF.ADD`](./cf.add.md) | [`CF.RESERVE`](./cf.reserve.md)
