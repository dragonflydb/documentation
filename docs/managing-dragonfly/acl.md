# Access Control Lists (ACL)

Dragonfly has built in support for ACL. DF operators, get fine grained control on how and who accesses the datastore via the ACL family of commands.
Since, DF is designed as a drop in replacement for Redis, you can expect the same API functionality for ACL as in Redis.

All connections in DF default to the user `default` (unless the operator turns them off). `default` can `auth` in DF using any password, is allowed to
execute any command and is part of all the available ACL groups.

Permissions for a given user are controlled via a domain specific language (DSP) and are divided into 4 categories:

1. ACL groups
2. Commands
3. Pub/Sub messages (not implemented yet)
4. Keys (not implemented yet)

Granting or revoking permissions for a user is as easy as calling the `ACL SETUSER` command. For example:

```
ACL SETUSER John ON >mypassword +@ADMIN +SET
```

If the user `John` does not exist, then the user is created with the permissions specified in the argument list of the command.
Otherwise, `SETUSER` acts as an `update` of the entry (and its permissions) for that user.

A user can be `ON` or `OFF`. By default, all users (except `default`) are `OFF` (unless you explicitly grant them `ON`). The
`ON/OFF` mechanism grants or revokes the user the ability to `authenticate` in the sytem via the `AUTH` command.

## Passwords
A password can be set via the `>` character followed by the password. For example: `ACL SETUSER Mike >mypassword`, creates the user `Mike` with
pass `mypassword`. Currently, each user can have only one password.

The `special` word `nopass` allows the user to `auth` via any password.

Note that subsequent uses of `>` on already existing user, act an password update.

## Authentication

Users can use `AUTH USERNAME PASSWORD` to authorize their connection with a given user. After that, all of the commands issued within a connection
will abide by the user's specified permissions. By changing the `default` user's status to `OFF` or password, it will make all incoming connections
to require authentication.

Note that, if the password is changed and a user has already `authenticated` then they don't need to authenticate again for that given connection.
Basically, password change does not act as a connection eviction mechanism. However, if the `ACL DELUSER` is used to remove the user from the system,
then their connection is killed by the system. Furthermore, any change to a user's permission list via `ACL SETUSER` will propagate to the already
active and authenticated connections.

Also note, that the flag `--requirepass` now also changes the `default` user password. So, if during Dragonfly startup the flag `requirepass` is set,
then the `default` user's password will be the one specified in that flag.

## ACL Groups
Each `command` belongs to a set of ACL groups. The syntax for specifying a group is:

```
+@GROUP_NAME
-@GROUP_NAME
```

The sign at the front dictates the operation (`+` for granting and `-` for revoking). The `@` denotes category (ACL group) and
the `GROUP_NAME` is the name of the group. For example:

```
ACL SETUSER John ON +@FAST
```

Updates the permissions of user `John` and grants him the ability to run any command in the group `FAST`. Revoking this,
is straighforward:

```
ACL SETUSER John -@FAST
```

There are also the special keywords `+@ALL, -@ALL` that allow the user to run commands found in `ALL GROUPS`.

With `@ALL` it's possible to do:

```
ACL SETUSER John +@ALL -@ADMIN -@FAST
```

Which basically grants all but the `@ADMIN` and `@FAST` groups to the user. That way, it's easy to express which groups of permissions
the user should not be a part of.

## Commands

Dividing the commands into groups offers a great flexibility of quickly granting/revoking permissions but it's somehow limited because
these groups are not user defined. Therefore, for finer control, the user can specify a list of commands that is explicitly allowed to execute.
For example:

```
ACL SETUSER John +GET +SET +@FAST
```

This allows the user `John` to execute only the `SET` && `GET` commands and all of the commands associated with the group `FAST`.
Any attempt of user `John` to issue a command other than the above, will be rejected by the system.

Note that the syntax is similar to the ACL groups, but without the prefix `@`.

The special `+ALL` (note without the `@`) is used to denote all of the currently implemented commands.

## Persistence

The state of all of the users and their permissions can be captured and placed in a file. As with redis,
the `--aclfile` option is used to specify the file from which Dragonfly will load the ACL state from.

Afterwards, any change done at runtime, can be persisted at anytime via the command `ACL SAVE` which
evicts the currently stored ACL state to the file specified in the `--aclfile` option.

Note, that the `aclfile` file is compatible with Redis (however it must not contain any keys or
pub/sub DSL's because these yet are not supported so if you plan to migrate, just open the file and strip them away).

If you want the `aclfile` to be writable, that is, if you want `ACL SAVE` to work, we would advice against placing the `aclfile`
under `/etc` directory because the folder is only accesible by Dragonfly as `readonly`. You change this behaviour, by editing 
the systemd service file located in `/lib/systemd/system/dragonfly.service`.

For convenience, we suggest to place `acl` files in `/var/lib/dragonfly/`.

## Logs

All connections that fail to authenticate and all of the authenticated users who fail to run a command (because 
of their permissions) are stored in a log. The size of the log can be configured by the option `--acllog_max_len`.
This flag, operates a little bit differently from Redis. Specifically, because Dragonfly uses a shared nothing thread per core architecture,
each thread of execution has its own log. Therefore, the total size of the log entries, is the flag number multiplied
by the available number of cores in the system. So for example, if you are running on a 4 core machine with `--acllog_max_len=8`
then the total number of log entries stored in the system at any time can be `32` and each core can store up to `8` entries.
When the per-thread threshold is reached, each new log entry will cause the oldest one to get evicted.

Log information can be printed via the command `ACL LOG`.
