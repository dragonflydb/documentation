---
description: Learn how to use Redis BF.SCANDUMP to export a Bloom filter in chunks from Dragonfly.
---

import PageTitle from '@site/src/components/PageTitle';

# BF.SCANDUMP

<PageTitle title="Redis BF.SCANDUMP Command (Documentation) | Dragonfly" />

## Syntax

    BF.SCANDUMP key iterator

**Time complexity:** O(F + C) per call, where F is the number of sub-filters and C is the number of bytes returned.

**ACL categories:** @bloom

Exports the Bloom filter stored at `key` as a sequence of binary chunks. Use
[`BF.LOADCHUNK`](./bf.loadchunk.md) to restore those chunks into a Bloom filter.

## Iteration

Start with `iterator` set to `0`. Each call returns an iterator and a data chunk.
Pass the returned iterator to the next `BF.SCANDUMP` call. Continue until the
returned iterator is `0`, which indicates completion and is accompanied by an
empty string.

Treat iterators as opaque values: use the values returned by the command rather
than calculating them yourself. Preserve each nonzero returned iterator together
with its chunk. To restore the filter, pass these pairs to
`BF.LOADCHUNK destination iterator data` in the order they were returned. Do not
pass the final zero iterator and empty string to `BF.LOADCHUNK`.

The chunks contain binary data, so use a client that preserves bytes without
decoding them as text. Keep the source filter unchanged throughout the dump;
the sequence of calls does not provide a snapshot across concurrent updates.

## Return

[Array reply](https://valkey.io/topics/protocol/#arrays) with two elements:

1. [Integer reply](https://valkey.io/topics/protocol/#integers): the iterator for
   the next call, or `0` when the dump is complete.
2. [Bulk string reply](https://valkey.io/topics/protocol/#bulk-strings): the binary
   data chunk, or an empty string when the dump is complete.

[Error reply](https://valkey.io/topics/protocol/#simple-errors): if `key` does not
exist, holds a different data type, is a Bloom filter still being loaded, or
`iterator` is not a nonnegative signed 64-bit integer.

## Examples

Create a filter and start its dump:

```shell
dragonfly> BF.RESERVE visitors 0.01 1000
OK

dragonfly> BF.MADD visitors alice bob carol
1) (integer) 1
2) (integer) 1
3) (integer) 1

dragonfly> BF.SCANDUMP visitors 0
1) (integer) 1
2) "\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00@"
```

The first reply contains metadata. Continue with the returned iterator to obtain
the filter data. The following Python example uses the `redis` package to copy
the filter created above into a new key, `visitors-copy`. Use a destination key
that does not already exist.

```python
import redis

client = redis.Redis(host="localhost", port=6379, decode_responses=False)

iterator = 0
while True:
    iterator, data = client.execute_command("BF.SCANDUMP", "visitors", iterator)
    if iterator == 0:
        break
    client.execute_command("BF.LOADCHUNK", "visitors-copy", iterator, data)

print(client.execute_command("BF.MEXISTS", "visitors-copy", "alice", "bob", "carol"))
# [1, 1, 1]
```

## See also

[`BF.LOADCHUNK`](./bf.loadchunk.md) | [`BF.RESERVE`](./bf.reserve.md) | [`BF.INFO`](./bf.info.md) | [`BF.MEXISTS`](./bf.mexists.md)
