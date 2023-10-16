# ACL DRYRUN

## Syntax

    ACL DRYRUN username command

**ACL categories:** @admin, @slow, @dangerous

This command simulates the execution of a given command by a user. It can be used to test the permissions without having to enable the user or cause the side effects of running the actual commands.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec/#simple-strings): `OK` on successor the reason the user can't execute the command.

## Examples

```shell
dragonfly> ACL SETUSER mike >mypass +GET -SET
ACL DRYRUN mike GET
"OK"

dragonfly> ACL DRYRUN mike SET
(error) ERR User: mike is not allowed to execute command: SET
```
