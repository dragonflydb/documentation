---
description: Create or update ACL users
---

# ACL SETUSER

## Syntax

    ACL SETUSER username [rule [rule ...]]

**ACL categories:** @admin, @slow, @dangerous

## Rules/Options

The following are the currently allowed rules

`Status` -- `ON/OFF` if the user is allowed to authenticate with `auth` command.

`Password` -- `>password`. Set or update the password of the user.

`ACL Categories` -- To add a category user `+@category_name` and to remove a category `-@category_name`.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec#resp-simple-strings): `OK` if there was no error. Otherwise, the error message of the error.


## Examples

```shell
dragonfly> ACL SETUSER myuser ON >mypass +@string +@fast -@slow
"ok"
```
