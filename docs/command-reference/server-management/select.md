---
description: Change the selected database for the current connection
---

# SELECT

## Syntax

    SELECT index

**Time complexity:** O(1)

**ACL categories:** @fast, @connection

Select the Dragonfly logical database having the specified zero-based numeric index.
New connections always use the database 0.

Selectable databases are a form of namespacing: all databases are still persisted in the same snapshot files. However different databases can have keys with the same name, and commands like `FLUSHDB`, `SWAPDB` or `RANDOMKEY` work on specific databases.

In practical terms, Dragonfly databases should be used to separate different keys belonging to the same application (if needed), and not to use a single instance for multiple unrelated applications.

Since the currently selected database is a property of the connection, clients should track the currently selected database and re-select it on reconnection.
## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec/#simple-strings)
