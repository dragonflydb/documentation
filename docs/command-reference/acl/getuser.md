# ACL GETUSER

## Syntax

    ACL GETUSER username

**ACL categories:** @admin, @slow, @dangerous

The command returns all the rules defined for an existing ACL user.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec/#arrays): a list of ACL rule definitions for the user. Empty array, if the user doesn't exist.

## Examples

```shell
dragonfly> ACL GETUSER default 
1) flags
2) 1) on
   2) nopass
3) passwords
4) (empty array)
5) commands
6) +@ALL +ALL
```
