---
description: Learn how to use Redis BF.LOADCHUNK to restore a Bloom filter from binary chunks in Dragonfly.
---

import PageTitle from '@site/src/components/PageTitle';

# BF.LOADCHUNK

<PageTitle title="Redis BF.LOADCHUNK Command (Documentation) | Dragonfly" />

## Syntax

    BF.LOADCHUNK key iterator data

**Time complexity:** O(F + B) per call, where F is the number of sub-filters and B is the number of bytes copied or initialized. Starting a new sub-filter initializes its entire storage.

**ACL categories:** @bloom

Restores a Bloom filter at `key` from binary chunks produced by
[`BF.SCANDUMP`](./bf.scandump.md).

## Loading chunks

Pass each chunk's **returned iterator** and its corresponding `data` to
`BF.LOADCHUNK`, in the order returned by `BF.SCANDUMP`. Use the returned iterator,
not the iterator supplied to the dump call. Preserve the data as bytes without
decoding it as text or modifying it.

The first chunk has iterator `1` and initializes the destination. It creates a
new key or **replaces an existing key of any type**, clearing any expiration on
that key. There is no need to call `BF.RESERVE` first. Loading this first chunk
again restarts the restore.

Subsequent chunks populate the filter. A successful reply confirms that the
individual chunk was loaded, not that the entire filter has been restored.
Load every chunk before querying or modifying the destination. The restore spans
multiple commands and is not atomic; an interrupted restore can leave an
incomplete filter.

When `BF.SCANDUMP` returns iterator `0` and an empty string, the dump is complete.
Do not pass that final pair to `BF.LOADCHUNK`. There is no separate finalization
command. If the destination needs an expiration, set it after loading all chunks.

## Return

[Simple string reply](https://valkey.io/topics/protocol/#simple-strings): `OK`
when the chunk is loaded successfully.

[Error reply](https://valkey.io/topics/protocol/#simple-errors): if the iterator
is not a positive signed 64-bit integer, the payload is invalid, or a subsequent
chunk targets a missing key or a key holding a different data type.

## Examples

The following Python example uses the `redis` package to create a filter, collect
its dump chunks, and restore them into a new key. Keep the source filter unchanged
while collecting the dump. Use a destination key that does not already exist
unless you intend to replace it.

```python
import redis

client = redis.Redis(host="localhost", port=6379, decode_responses=False)

client.execute_command("BF.RESERVE", "visitors", 0.01, 1000)
client.execute_command("BF.MADD", "visitors", "alice", "bob", "carol")

chunks = []
iterator = 0
while True:
    iterator, data = client.execute_command("BF.SCANDUMP", "visitors", iterator)
    if iterator == 0:
        break
    chunks.append((iterator, data))

for iterator, data in chunks:
    client.execute_command("BF.LOADCHUNK", "visitors-copy", iterator, data)

print(client.execute_command("BF.MEXISTS", "visitors-copy", "alice", "bob", "carol"))
# [1, 1, 1]
```

You can inspect the restored filter from the command line:

```shell
dragonfly> BF.MEXISTS visitors-copy alice bob carol
1) (integer) 1
2) (integer) 1
3) (integer) 1
```

## See also

[`BF.SCANDUMP`](./bf.scandump.md) | [`BF.INFO`](./bf.info.md) | [`BF.MEXISTS`](./bf.mexists.md)
