---
description:  Learn how to use Dragonfly CLIENT SETINFO command.
---

import PageTitle from '@site/src/components/PageTitle';

# CLIENT SETINFO

<PageTitle title="Redis CLIENT SETINFO Command (Documentation) | Dragonfly" />

## Syntax

    CLIENT SETINFO <LIB-NAME libname | LIB-VER libver>

**Time complexity:** O(1)

**ACL categories:** @slow, @connection

The CLIENT SETINFO command assigns various info attributes to the current connection which are displayed in the output of CLIENT LIST and CLIENT INFO.

Currently the supported attributes are:

lib-name - meant to hold the name of the client library that's in use.
lib-ver - meant to hold the client library's version.


## Return

[Simple string reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#simple-strings):  OK if the attribute name was successfully set.
