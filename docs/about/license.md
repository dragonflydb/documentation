---
description: "The Dragonfly Source-Available License (DSAL) for v2.1 and later, BSL 1.1 for older releases, and the Creative Commons license for these docs."
sidebar_position: 3
---

# License

## Software Licensing

Starting with v2.1, Dragonfly is released under the
[Dragonfly Source-Available License (DSAL)](https://github.com/dragonflydb/dragonfly/blob/main/LICENSE.md).
DSAL is a "source available" license and it's not strictly an open-source license.
In general terms, it means that Dragonfly's code is free to use, modify and incorporate into your own
applications or products, as long as you do not distribute or offer it as a standalone database,
data store, caching product or a substantially similar product or service.
Production use is free up to an aggregate of 100 vCPUs across all your concurrently running instances
(including replicas), while non-production use is unlimited. Usage beyond that requires a commercial license.

The license defines the limit and what counts toward it:

- **Usage Limit:** a maximum of 100 vCPUs in Production Use, calculated in the aggregate across all
  instances running concurrently by or on behalf of you and your Affiliates (Section 1).
- **Production Use:** any running instance of Dragonfly or a Modified Version that stores, serves or
  processes data for live end users, customers or your business operations, including any replica,
  standby or failover instance of such an instance, regardless of how it is labeled (Section 17).

See [LICENSE.md](https://github.com/dragonflydb/dragonfly/blob/main/LICENSE.md) for the exact terms.

Releases before v2.1 remain under BSL 1.1 (Business Source License), with the terms in the `LICENSE.md`
file of each release, for example [v2.0.0](https://github.com/dragonflydb/dragonfly/blob/v2.0.0/LICENSE.md).

## Documentation Licensing

DragonflyDB docs are licensed under the
[Creative Commons Attribution-ShareAlike 4.0 International Public License](https://creativecommons.org/licenses/by-sa/4.0/)

## Attribution

Dragonfly implements a lot of Redis server functionality, and DragonflyDB
has modified & adapted documents from [redis-doc](https://github.com/redis/redis-doc/)
for its use here as applicable to DragonflyDB.

We maintain the same Creative Commons Attribution-ShareAlike 4.0 license for the adapted material,
as per the requirements of [LICENSE](https://github.com/redis/redis-doc/blob/master/LICENSE) file
from the original repository.

> Copyright &copy; 2009-2014, Salvatore Sanfilippo<br/>
Copyright &copy; 2023, DragonflyDB Ltd.
