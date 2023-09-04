---
description: Add new entries to streams
---

# XADD

## Syntax

    XADD key [NOMKSTREAM] [<MAXLEN | MINID> [= | ~] threshold [LIMIT count]] <* | id> field value [field value ...]

**Time complexity:** O(1) when adding a new entry, O(N) when trimming where N being the number of entries evicted

**ACL categories:** @write, @stream, @fast

**XADD** command appends new entry to the specified key i.e. stream.
The command returns the *ID* of the new entry. User can either explicitly
specify the ID of the newly created entry or the command automatically
generates an ID.

Each entry can store multiple field-value pairs. The field-value pairs
are stored in the same order as the client specified. Commands that read
the stream, such as **XRANGE** or **XREAD**, are guaranteed to return the
fields and values exactly in the same order they were added by **XADD**.

Note that **XADD** is the only command that appends entries into a
stream. No other command has the ability to add new entries.

### Key

Key is the stream name to which the entry needs to be appended. If the
stream is not found, the command creates a new stream with the key and
appends the entry to it.

### Specifying ID

It is required to specify ID or a special character "**\***" before starting
the field-value pair list. An ID has two parts. These are - 
* **Unix time in milliseconds** - It is a 64 bit number that stores
	unix time in milliseconds. When the entry is auto-generated (i.e. client
	didn't specify an ID explicitly), the command uses the time of generation
	to built the unique ID.
* **Sequence** - 64 bit number. The sequence part of the ID helps distinguishing
	two entries that were created at the same time. 

These two part are joined by the "**-**" character. So a complete ID has the following
pattern - *<time-in-ms\>-<sequence\>*. Below is an example -
```shell
1623910120014-1
```

Clients can also specify incomplete IDs where the sequence part is
replaced with the **\*** character. In that case, the command generates
the id with greater sequence number than the previous entry having
the same unix time. For example, if the previously generated entry has
the id `1623910120014-1` and if the client specified `1623910120014-*`,
the new entry will have the id `1623910120014-2`.

```shell
dragonfly> XADD mystream 1623910120014-1 name bob
"1623910120014-1"
dragonfly> XADD mystream 1623910120014-* name alice
"1623910120014-2"
```

If client specify **\*** instead of an ID, dragonfly will auto-generate
an ID for the created entry.
```shell
dragonfly> XADD mystream * name john
"1623910151125-0"
```


### NOMKSTREAM

By default dragonfly creates a new stream if the given key doesn't
exist. If **NOMKSTREAM** is specified, dragonfly will not create
any new stream.

### MAXLEN and MINID

Sometimes there is a need to control the maximum number of entries
in a stream. **MAXLEN** and **MINID** options can be used in these
cases. Basically XADD trims entries from the specified stream
according to the client's need.

**MAXLEN** ensures that the number of entries in a stream
doesn't exceed a certain limit. **MINID**, on the other hand,
ensures that entries with IDs less than the specified **MINID**
get deleted. These two options take a *threshold* denoting the
length (in case of **MAXLEN**) or ID (in case of **MINID**).

Dragonfly gives two options to control the trimming nature.
"**=**" argument tells the command to do exact trimming of
entries. Whereas **~** argument tells the command to do
approximate trimming. That is, it is upto the command to
decide how many entries need to be deleted. So a stream may
have **few more** entries than the given *threshold*.

```shell
dragonfly> XADD mystream MAXLEN = 2 * name Alice
"1687928705042-0"
dragonfly> XLEN mystream
(integer) 2
```

**LIMIT** is useful when you want to limit the number of delete
operations used for **MAXLEN** or **MINID**.

## Return

[Bulk String Reply](https://redis.io/docs/reference/protocol-spec#resp-bulk-strings).
The command returns the ID of the added entry. The ID is the
one auto-generated if * is passed as ID argument, otherwise
the command just returns the same ID specified by the user
during insertion.
