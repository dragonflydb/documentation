---
description: Simulate execution of a command from a user
---

import PageTitle from '@site/src/components/PageTitle';

# ACL DRYRUN

<PageTitle title="Redis ACL DRYRUN Command (Documentation) | Dragonfly" />

## Syntax

    ACL DRYRUN username command

**ACL categories:** @admin, @slow, @dangerous

This command simulates the execution of a given command by a user.
It can be used to test the permissions without having to enable the user or cause the side effects of running the actual command.

## Return

- [Simple string reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#simple-strings): `OK` on success.
- [Bulk string reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#bulk-strings): an error describing why the user can't execute the command.

## Examples

```shell
dragonfly> ACL SETUSER mike >mypass +GET -SET
OK

dragonfly> ACL DRYRUN mike GET
OK

dragonfly> ACL DRYRUN mike SET
"This user has no permissions to run the 'set' command"
```
