---
sidebar_position: 0
---

import CompatibilityTable from '@site/src/components/CompatibilityTable'

# Dragonfly API Compatibility

| Command Family   | Command                       | Dragonfly Support   |
| ---------------- | ----------------------------- | ------------------- |
| Bitmap           | BITCOUNT                      | Fully supported     |
|                  | BITFIELD                      | Unsupported         |
|                  | BITFIELD_RO                   | Unsupported         |
|                  | BITOP                         | Fully supported     |
|                  | BITPOS                        | Fully supported     |
|                  | GETBIT                        | Fully supported     |
|                  | SETBIT                        | Fully supported     |
| Cluster          | ASKING                        | Unsupported         |
|                  | CLUSTER ADDSLOTS              | Unsupported         |
|                  | CLUSTER ADDSLOTSRANGE         | Unsupported         |
|                  | CLUSTER BUMPEPOCH             | Unsupported         |
|                  | CLUSTER COUNT-FAILURE-REPORTS | Unsupported         |
|                  | CLUSTER COUNTKEYSINSLOT       | Unsupported         |
|                  | CLUSTER DELSLOTS              | Unsupported         |
|                  | CLUSTER DELSLOTRANGE          | Unsupported         |
|                  | CLUSTER FAILOVER              | Unsupported         |
|                  | CLUSTER FLUSHSLOTS            | Unsupported         |
|                  | CLUSTER FORGET                | Unsupported         |
|                  | CLUSTER GETKEYSINSLOT         | Unsupported         |
|                  | CLUSTER INFO                  | Fully supported     |
|                  | CLUSTER KEYSLOT               | Unsupported         |
|                  | CLUSTER LINKS                 | Unsupported         |
|                  | CLUSTER MEET                  | Unsupported         |
|                  | CLUSTER MYID                  | Unsupported         |
|                  | CLUSTER MYSHARDID             | Unsupported         |
|                  | CLUSTER NODES                 | Fully supported     |
|                  | CLUSTER REPLICAS              | Unsupported         |
|                  | CLUSTER REPLICATE             | Unsupported         |
|                  | CLUSTER RESET                 | Unsupported         |
|                  | CLUSTER SAVECONFIG            | Unsupported         |
|                  | CLUSTER SET-CONFIG-EPOCH      | Unsupported         |
|                  | CLUSTER SETSLOT               | Unsupported         |
|                  | CLUSTER SHARDS                | Fully supported     |
|                  | CLUSTER SLAVES                | Unsupported         |
|                  | CLUSTER SLOTS                 | Fully supported     |
|                  | READONLY                      | Unsupported         |
|                  | READWRITE                     | Unsupported         |
| Connection       | AUTH                          | Partially supported |
|                  | CLIENT CACHING                | Unsupported         |
|                  | CLIENT GETNAME                | Fully supported     |
|                  | CLIENT GETREDIR               | Unsupported         |
|                  | CLIENT ID                     | Unsupported         |
|                  | CLIENT INFO                   | Unsupported         |
|                  | CLIENT KILL                   | Unsupported         |
|                  | CLIENT LIST                   | Fully supported     |
|                  | CLIENT NO-EVICT               | Unsupported         |
|                  | CLIENT NO-TOUCH               | Unsupported         |
|                  | CLIENT PAUSE                  | Unsupported         |
|                  | CLIENT REPLY                  | Unsupported         |
|                  | CLIENT SETINFO                | Unsupported         |
|                  | CLIENT SETNAME                | Fully supported     |
|                  | CLIENT TRACKING               | Unsupported         |
|                  | CLIENT TRACKINGINFO           | Unsupported         |
|                  | CLIENT UNBLOCK                | Unsupported         |
|                  | CLIENT UNPAUSE                | Unsupported         |
|                  | ECHO                          | Fully supported     |
|                  | HELLO                         | Partially supported |
|                  | PING                          | Fully supported     |
|                  | QUIT                          | Fully supported     |
|                  | RESET                         | Unsupported         |
|                  | SELECT                        | Fully supported     |
| Generic          | COPY                          | Unsupported         |
|                  | DEL                           | Fully supported     |
|                  | DUMP                          | Fully supported     |
|                  | EXISTS                        | Fully supported     |
|                  | EXPIRE                        | Fully supported     |
|                  | EXPIREAT                      | Fully supported     |
|                  | EXPIRETIME                    | Unsupported         |
|                  | KEYS                          | Fully supported     |
|                  | MIGRATE                       | Unsupported         |
|                  | MOVE                          | Fully supported     |
|                  | OBJECT ENCODING               | Unsupported         |
|                  | OBJECT FREQ                   | Unsupported         |
|                  | OBJECT IDLETIME               | Unsupported         |
|                  | OBJECT REFCOUNT               | Unsupported         |
|                  | PRESIST                       | Fully supported     |
|                  | PEXPIRE                       | Fully supported     |
|                  | PEXPIREAT                     | Fully supported     |
|                  | PEXPIRETIME                   | Unsupported         |
|                  | PTTL                          | Fully supported     |
|                  | RANDOMKEY                     | Unsupported         |
|                  | RENAME                        | Fully supported     |
|                  | RENAMENX                      | Fully supported     |
|                  | RESTORE                       | Partially supported |
|                  | SCAN                          | Fully supported     |
|                  | SORT                          | Partially supported |
|                  | SORT_RO                       | Unsupported         |
|                  | TOUCH                         | Fully supported     |
|                  | TTL                           | Fully supported     |
|                  | TYPE                          | Fully supported     |
|                  | UNLINK                        | Fully supported     |
|                  | WAIT                          | Unsupported         |
|                  | WAITAOF                       | Unsupported         |
| Geo              | GEOADD                        | Unsupported         |
|                  | GEODIST                       | Unsupported         |
|                  | GEOHASH                       | Unsupported         |
|                  | GEOPOS                        | Unsupported         |
|                  | GEORADIUS                     | Unsupported         |
|                  | GEORADIUS_RO                  | Unsupported         |
|                  | GEORADIUSBYMEMBER             | Unsupported         |
|                  | GEORADIUSBYMEMBER_RO          | Unsupported         |
|                  | GEOSEARCH                     | Unsupported         |
|                  | GEOSEARCHSTORE                | Unsupported         |
| Hash             | HDEL                          | Fully supported     |
|                  | HEXISTS                       | Fully supported     |
|                  | HGET                          | Fully supported     |
|                  | HGETALL                       | Fully supported     |
|                  | HINCRBY                       | Fully supported     |
|                  | HINCRBYFLOAT                  | Fully supported     |
|                  | HKEYS                         | Fully supported     |
|                  | HLEN                          | Fully supported     |
|                  | HMGET                         | Fully supported     |
|                  | HMSET                         | Unsupported         |
|                  | HRANDFIELD                    | Partially supported |
|                  | HSCAN                         | Fully supported     |
|                  | HSET                          | Fully supported     |
|                  | HSETNX                        | Fully supported     |
|                  | HSTRLEN                       | Fully supported     |
|                  | HVALS                         | Fully supported     |
| HyperLogLog      | PFADD                         | Fully supported     |
|                  | PFMERGE                       | Fully supported     |
|                  | PFCOUNT                       | Fully supported     |
|                  | PFDEBUG                       | Unsupported         |
|                  | PFSELFTEST                    | Unsupported         |
|                  |                               |                     |
| List             | BRPOPLPUSH                    | Fully supported     |
|                  | BRPOP                         | Fully supported     |
|                  | BLMPOP                        | Unsupported         |
|                  | LINDEX                        | Fully supported     |
|                  | LINSERT                       | Fully supported     |
|                  | LLEN                          | Fully supported     |
|                  | LMOVE                         | Fully supported     |
|                  | LPUSH                         | Fully supported     |
|                  | LRANGE                        | Fully supported     |
|                  | LSET                          | Fully supported     |
|                  | LTRIM                         | Fully supported     |
|                  | RPOPLPUSH                     | Fully supported     |
|                  | RPUSH                         | Fully supported     |
|                  | RPUSHX                        | Fully supported     |
|                  | RPOP                          | Fully supported     |
|                  | LREM                          | Fully supported     |
|                  | LPUSHX                        | Fully supported     |
|                  | LMPOP                         | Unsupported         |
|                  | LPOS                          | Fully supported     |
|                  | LPOP                          | Fully supported     |
|                  | BLPOP                         | Fully supported     |
|                  | BLMOVE                        | Fully supported     |
| PubSub           | PSUBSCRIBE                    | Fully supported     |
|                  | PUBLISH                       | Fully supported     |
|                  | PUBSUB CHANNELS               | Fully supported     |
|                  | PUBSUB NUMPAT                 | Fully supported     |
|                  | PUBSUB NUMSUB                 | Fully supported     |
|                  | PUBSUB SHARDCHANNELS          | Fully supported     |
|                  | PUBSUB SHARDNUMSUB            | Fully supported     |
|                  | PUNSUBSCRIBE                  | Fully supported     |
|                  | SPUBLISH                      | Unsupported         |
|                  | SSUBSCRIBE                    | Unsupported         |
|                  | SUNSUBSCRIBE                  | Unsupported         |
|                  | SUBSCRIBE                     | Fully supported     |
|                  | UNSUBSCRIBE                   | Fully supported     |
| Scripting        | EVAL                          | Fully supported     |
|                  | EVAL_RO                       | Unsupported         |
|                  | EVALSHA                       | Fully supported     |
|                  | EVALSHA_RO                    | Unsupported         |
|                  | FCALL                         | Unsupported         |
|                  | FUNCTION FLUSH                | Unsupported         |
|                  | FUNCTION \*                   | Unsupported         |
|                  | SCRIPT LOAD                   | Fully supported     |
|                  | SCRIPT EXISTS                 | Fully supported     |
|                  | SCRIPT FLUSH                  | Unsupported         |
|                  | SCRIPT DEBUG                  | Unsupported         |
|                  | SCRIPT KILL                   | Unsupported         |
| Server           | ACL CAT                       | Unsupported         |
|                  | ACL DELUSER                   | Unsupported         |
|                  | ACL DRYRUN                    | Unsupported         |
|                  | ACL GENPASS                   | Unsupported         |
|                  | ACL GETUSER                   | Unsupported         |
|                  | ACL LIST                      | Unsupported         |
|                  | ACL LOAD                      | Unsupported         |
|                  | ACL LOG                       | Unsupported         |
|                  | ACL SAVE                      | Unsupported         |
|                  | ACL SETUSER                   | Unsupported         |
|                  | ACL USERS                     | Unsupported         |
|                  | ACL WHOAMI                    | Unsupported         |
|                  | BGREWRITEAOF                  | Unsupported         |
|                  | BGSAVE                        | Fully supported     |
|                  | COMMAND                       | Fully supported     |
|                  | COMMAND COUNT                 | Fully supported     |
|                  | COMMAND DOCS                  | Unsupported         |
|                  | COMMAND GETKEYS               | Unsupported         |
|                  | COMMAND GETKEYSANDFLAGS       | Unsupported         |
|                  | COMMAND INFO                  | Unsupported         |
|                  | COMMAND LIST                  | Unsupported         |
|                  | CONFIG GET                    | Unsupported         |
|                  | CONFIG RESETSTAT              | FULLY SUPPORTED     |
|                  | CONFIG REWRITE                | Unsupported         |
|                  | CONFIG SET                    | Unsupported         |
|                  | DBSIZE                        | Fully supported     |
|                  | FAILOVER                      | Unsupported         |
|                  | FLUSHALL                      | Fully supported     |
|                  | FLUSHDB                       | Fully supported     |
|                  | INFO                          | Fully supported     |
|                  | LASTSAVE                      | Fully supported     |
|                  | LATENCY DOCTOR                | Unsupported         |
|                  | LATENCY GRAPH                 | Unsupported         |
|                  | LATENCY HISTOGRAM             | Unsupported         |
|                  | LATENCY HISTORY               | Unsupported         |
|                  | LATENCY LATEST                | Unsupported         |
|                  | LATENCY RESET                 | Unsupported         |
|                  | LOLWUT                        | Unsupported         |
|                  | MEMORY DOCTOR                 | Unsupported         |
|                  | MEMORY MALLOC-STATS           | Fully supported     |
|                  | MEMORY PURGE                  | Unsupported         |
|                  | MEMORY STATS                  | Unsupported         |
|                  | MEMORY USAGE                  | Unsupported         |
|                  | MODULE LIST                   | Unsupported         |
|                  | MODULE LOAD                   | Unsupported         |
|                  | MODULE LOADEX                 | Unsupported         |
|                  | MODULE UNLOAD                 | Unsupported         |
|                  | MONITOR                       | Fully supported     |
|                  | REPLICAOF                     | Fully supported     |
|                  | ROLE                          | Fully supported     |
|                  | SAVE                          | Fully supported     |
|                  | SHUTDOWN                      | Fully supported     |
|                  | SLAVEOF                       | Fully supported     |
|                  | SLOWLOG GET                   | Unsupported         |
|                  | SLOWLOG LEN                   | Unsupported         |
|                  | SLOWLOG RESET                 | Unsupported         |
|                  | SWAPDB                        | Unsupported         |
|                  | TIME                          | Fully supported     |
| Set              | SADD                          | Fully supported     |
|                  | SCARD                         | Fully supported     |
|                  | SDIFF                         | Fully supported     |
|                  | SDIFFSTORE                    | Fully supported     |
|                  | SINTER                        | Fully supported     |
|                  | SINTERCARD                    | Unsupported         |
|                  | SINTERSTORE                   | Fully supported     |
|                  | SISMEMBER                     | Fully supported     |
|                  | SMEMBERS                      | Fully supported     |
|                  | SMISMEMBER                    | Fully supported     |
|                  | SMOVE                         | Fully supported     |
|                  | SPOP                          | Fully supported     |
|                  | SRANDMEMBER                   | Unsupported         |
|                  | SREM                          | Fully supported     |
|                  | SSCAN                         | Fully supported     |
|                  | SUNION                        | Fully supported     |
|                  | SUNIONSTORE                   | Fully supported     |
| Sorted Set       | BZMPOP                        | Unsupported         |
|                  | BZPOPMZX                      | Fully supported     |
|                  | BZPOPMIN                      | Fully supported     |
|                  | ZADD                          | Fully supported     |
|                  | ZCARD                         | Fully supported     |
|                  | ZCOUNT                        | Fully supported     |
|                  | ZDIFF                         | Unsupported         |
|                  | ZDIFFSTORE                    | Unsupported         |
|                  | ZINCRBY                       | Fully supported     |
|                  | ZINTER                        | Unsupported         |
|                  | ZINTERCARD                    | Fully supported     |
|                  | ZINTERSTORE                   | Fully supported     |
|                  | ZLEXCOUNT                     | Fully supported     |
|                  | ZMPOP                         | Unsupported         |
|                  | ZMSCORE                       | Fully supported     |
|                  | ZPOPMAX                       | Fully supported     |
|                  | ZPOPMIN                       | Fully supported     |
|                  | ZRANDMEMBER                   | Unsupported         |
|                  | ZRANGE                        | Fully supported     |
|                  | ZRANGEBYLEX                   | Fully supported     |
|                  | ZRANGEBYSCORE                 | Fully supported     |
|                  | ZRANK                         | Fully supported     |
|                  | ZREM                          | Fully supported     |
|                  | ZREMRANGEBYLEX                | Fully supported     |
|                  | ZREMRANGEBYRANK               | Fully supported     |
|                  | ZREMRANGEBYSCORE              | Fully supported     |
|                  | ZREVRANGE                     | Fully supported     |
|                  | ZREVRANGEBYLEX                | Fully supported     |
|                  | ZREVRANGEBYSCORE              | Fully supported     |
|                  | ZREVRANK                      | Fully supported     |
|                  | ZSCAN                         | Fully supported     |
|                  | ZSCORE                        | Fully supported     |
|                  | ZUNION                        | Fully supported     |
|                  | ZUNIONSTORE                   | Fully supported     |
| Stream           | XAUTOCLAIM                    | Unsupported         |
|                  | XCLAIM                        | TBD                 |
|                  | XREAD                         | Fully supported     |
|                  | XADD                          | Fully supported     |
|                  | XPENDING                      | TBD                 |
|                  | XGROUP                        | Partially supported |
|                  | XRANGE                        | Fully supported     |
|                  | XSETID                        | Fully supported     |
|                  | XREVRANGE                     | Fully supported     |
|                  | XREADGROUP                    | Unsupported         |
|                  | XDEL                          | Fully supported     |
|                  | XINFO                         | Partially supported |
|                  | XACK                          | Unsupported         |
|                  | XTRIM                         | Partially supported |
| String           | APPEND                        | Fully supported     |
|                  | DECR                          | Fully supported     |
|                  | DECRBY                        | Fully supported     |
|                  | GET                           | Fully supported     |
|                  | GETDEL                        | Fully supported     |
|                  | GETEX                         | Fully supported     |
|                  | GETRANGE                      | Fully supported     |
|                  | GETSET                        | Fully supported     |
|                  | INCR                          | Fully supported     |
|                  | INCRBY                        | Fully supported     |
|                  | INCRBYFLOAT                   | Fully supported     |
|                  | LCS                           | Unsupported         |
|                  | MGET                          | Fully supported     |
|                  | MSET                          | Fully supported     |
|                  | MSETNX                        | Fully supported     |
|                  | PSETEX                        | Fully supported     |
|                  | SET                           | Fully supported     |
|                  | SETEX                         | Fully supported     |
|                  | SETNX                         | Fully supported     |
|                  | SETRANGE                      | Fully supported     |
|                  | STRLEN                        | Fully supported     |
|                  | SUBSTR                        | Fully supported     |
| Transactions     | DISCARD                       | Fully supported     |
|                  | EXEC                          | Fully supported     |
|                  | MULTI                         | Fully supported     |
|                  | UNWATCH                       | Fully supported     |
|                  | WATCH                         | Fully supported     |
| Bloom Filter     | TBD                           | Unsupported         |
| Cuckoo Filter    | TBD                           | Unsupported         |
| Count-min Sketch | TBD                           | Unsupported         |
| Graph            | TBD                           | Unsupported         |
| JSON             | ARRAPPEND                     | Fully supported     |
|                  | ARRINDEX                      | Fully supported     |
|                  | ARRINSERT                     | Fully supported     |
|                  | ARRLEN                        | Fully supported     |
|                  | ARRPOP                        | Fully supported     |
|                  | ARRTRIM                       | Fully supported     |
|                  | CLEAR                         | Fully supported     |
|                  | DEBUG                         | Fully supported     |
|                  | DEBUG MEMORY                  | Unsupported         |
|                  | DEL                           | Fully supported     |
|                  | FORGET                        | Fully supported     |
|                  | GET                           | Fully supported     |
|                  | MERGE                         | Unsupported         |
|                  | MGET                          | Fully supported     |
|                  | MSET                          | Unsupported         |
|                  | NUMINCRBY                     | Fully supported     |
|                  | NUMMULTBY                     | Fully supported     |
|                  | OBJKEYS                       | Fully supported     |
|                  | OBJLEN                        | Fully supported     |
|                  | RESP                          | Fully supported     |
|                  | SET                           | Fully supported     |
|                  | STRAPPEND                     | Fully supported     |
|                  | STRLEN                        | Fully supported     |
|                  | TOGGLE                        | Fully supported     |
|                  | TYPE                          | Fully supported     |
| Search           | FT.CREATE                     | Unsupported         |
|                  | FT.SEARCH                     | Unsupported         |
| Auto Suggest     | TBD                           | Unsupported         |
| T-Digest         | TBD                           | Unsupported         |
| Time Series      | TBD                           | Unsupported         |
| Top-K            | TBD                           | Unsupported         |
