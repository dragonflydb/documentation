---
description: "Learn how to use GEORADIUSBYMEMBER_RO to find geographical data in your Dragonfly database by defining radius."
---

import PageTitle from '@site/src/components/PageTitle';

# GEORADIUSBYMEMBER_RO
 
<PageTitle title="GEORADIUSBYMEMBER_RO Command (Documentation) | Dragonfly" />

## Syntax

    GEORADIUSBYMEMBER_RO key member radius <M | KM | FT | MI> [WITHCOORD] [WITHDIST] [WITHHASH] [COUNT count [ANY]] [ASC | DESC]

**Time complexity:** O(N+log(M)) where N is the number of elements inside the bounding box of the circular area delimited by center and radius and M is the number of items inside the index.

**ACL categories:** @read, @geo, @slow

Read-only variant of the GEORADIUSBYMEMBER command.

This command is identical to the GEORADIUSBYMEMBER command, except that it doesn't support the optional STORE and STOREDIST parameters.