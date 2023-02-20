---
description: Delete a function by name
---

# FUNCTION DELETE

## Syntax

    FUNCTION DELETE library-name

**Time complexity:** O(1)

Delete a library and all its functions.

This command deletes the library called _library-name_ and all functions in it.
If the library doesn't exist, the server returns an error.

For more information please refer to [Introduction to Redis Functions](https://redis.io/topics/functions-intro).

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec#resp-simple-strings)

## Examples

```
redis> FUNCTION LOAD Lua mylib "redis.register_function('myfunc', function(keys, args) return 'hello' end)"
OK
redis> FCALL myfunc 0
"hello"
redis> FUNCTION DELETE mylib
OK
redis> FCALL myfunc 0
(error) ERR Function not found
```
