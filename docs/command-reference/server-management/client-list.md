---
description:  Learn how to use Redis CLIENT LIST command to fetch details about all client connections.
---

import PageTitle from '@site/src/components/PageTitle';

# CLIENT LIST

<PageTitle title="Redis CLIENT LIST Command (Documentation) | Dragonfly" />

## Syntax

    CLIENT LIST

**Time complexity:** O(N) where N is the number of client connections

**ACL categories:** @admin, @slow, @dangerous, @connection

The `CLIENT LIST` command returns information and statistics about the client
connections server in a mostly human readable format.


## Return

[Bulk string reply](https://redis.io/docs/reference/protocol-spec/#bulk-strings): a unique string, formatted as follows:

* One client connection per line (separated by LF)
* Each line is composed of a succession of `property=value` fields separated
  by a space character.

Here is the meaning of the fields:

* `id`: a unique 64-bit client ID
* `addr`: address/port of the client
* `laddr`: address/port of local address client connected to (bind address)
* `fd`: file descriptor corresponding to the socket
* `name`: the name set by the client with `CLIENT SETNAME`
* `age`: total duration of the connection in seconds
* `idle`: idle time of the connection in seconds
* `phase`: connection state as captured by the "client list" command


## Notes

New fields are regularly added for debugging purpose. Some could be removed
in the future. A version safe client using this command should parse
the output accordingly (i.e. handling gracefully missing fields, skipping
unknown fields).
