---
sidebar_position: 0
---

# Dragonfly API Compatibility

| Command Family                               | Command                                                    | Dragonfly Support                                        |
| :------------------------------------------- | :--------------------------------------------------------- | :------------------------------------------------------- |
| <span class="family">Bitmap</span>           | <span class="command">BITCOUNT</span>                      | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">BITFIELD</span>                      | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">BITFIELD_RO</span>                   | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">BITOP</span>                         | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">BITPOS</span>                        | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">GETBIT</span>                        | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">SETBIT</span>                        | <span class="support supported">Fully supported</span>   |
| <span class="family">Cluster</span>          | <span class="command">ASKING</span>                        | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CLUSTER ADDSLOTS</span>              | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CLUSTER ADDSLOTSRANGE</span>         | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CLUSTER BUMPEPOCH</span>             | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CLUSTER COUNT-FAILURE-REPORTS</span> | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CLUSTER COUNTKEYSINSLOT</span>       | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CLUSTER DELSLOTS</span>              | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CLUSTER DELSLOTRANGE</span>          | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CLUSTER FAILOVER</span>              | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CLUSTER FLUSHSLOTS</span>            | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CLUSTER FORGET</span>                | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CLUSTER GETKEYSINSLOT</span>         | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CLUSTER INFO</span>                  | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">CLUSTER KEYSLOT</span>               | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CLUSTER LINKS</span>                 | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CLUSTER MEET</span>                  | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CLUSTER MYID</span>                  | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CLUSTER MYSHARDID</span>             | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CLUSTER NODES</span>                 | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">BICLUSTER REPLICASTCOUNT</span>      | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CLUSTER REPLICATE</span>             | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CLUSTER RESET</span>                 | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CLUSTER SAVECONFIG</span>            | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CLUSTER SET-CONFIG-EPOCH</span>      | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CLUSTER SETSLOT</span>               | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CLUSTER SHARDS</span>                | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">CLUSTER SLAVES</span>                | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CLUSTER SLOTS</span>                 | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">READONLY</span>                      | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">READWRITE</span>                     | <span class="support unsupported">Unsupported</span>     |
| <span class="family">Connection</span>       | <span class="command">AUTH</span>                          | <span class="support partial">Partially supported</span> |
|                                              | <span class="command">CLIENT CACHING</span>                | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CLIENT GETNAME</span>                | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">BITCCLIENT GETREDIROUNT</span>       | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CLIENT ID</span>                     | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CLIENT INFO</span>                   | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CLIENT KILL</span>                   | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CLIENT LIST</span>                   | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">CLIENT NO-EVICT</span>               | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CLIENT NO-TOUCH</span>               | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CLIENT PAUSE</span>                  | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CLIENT REPLY</span>                  | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CLIENT SETINFO</span>                | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CLIENT SETNAME</span>                | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">CLIENT TRACKING</span>               | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CLIENT TRACKINGINFO</span>           | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CLIENT UNBLOCK</span>                | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CLIENT UNPAUSE</span>                | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">ECHO</span>                          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">HELLO</span>                         | <span class="support partial">Partially supported</span> |
|                                              | <span class="command">PING</span>                          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">QUIT</span>                          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">RESET</span>                         | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">SELECT</span>                        | <span class="support supported">Fully supported</span>   |
| <span class="family">Generic</span>          | <span class="command">COPY</span>                          | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">DEL</span>                           | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">DUMP</span>                          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">EXISTS</span>                        | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">EXPIRE</span>                        | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">EXPIREAT</span>                      | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">DEXPIRETIMEUMP</span>                | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">KEYS</span>                          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">MIGRATE</span>                       | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">MOVE</span>                          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">OBJECT ENCODING</span>               | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">OBJECT FREQ</span>                   | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">OBJECT IDLETIME</span>               | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">OBJECT REFCOUNT</span>               | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">PRESIST</span>                       | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">PEXPIRE</span>                       | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">PEXPIREAT</span>                     | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">PEXPIRETIME</span>                   | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">PTTL</span>                          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">RANDOMKEY</span>                     | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">RENAME</span>                        | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">RENAMENX</span>                      | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">RESTORE</span>                       | <span class="support partial">Partially supported</span> |
|                                              | <span class="command">SCAN</span>                          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">SORT</span>                          | <span class="support partial">Partially supported</span> |
|                                              | <span class="command">SORT_RO</span>                       | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">TOUCH</span>                         | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">TTL</span>                           | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">TYPE</span>                          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">UNLINK</span>                        | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">WAIT</span>                          | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">WAITAOF</span>                       | <span class="support unsupported">Unsupported</span>     |
| <span class="family">Geo</span>              | <span class="command">GEOADD</span>                        | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">GEODIST</span>                       | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">GEOHASH</span>                       | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">GEOPOS</span>                        | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">GEORADIUS</span>                     | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">GEORADIUS_RO</span>                  | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">GEORADIUSBYMEMBER</span>             | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">GEORADIUSBYMEMBER_RO</span>          | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">GEOSEARCH</span>                     | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">GEOSEARCHSTORE</span>                | <span class="support unsupported">Unsupported</span>     |
| <span class="family">Hash</span>             | <span class="command">HDEL</span>                          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">HEXISTS</span>                       | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">HGET</span>                          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">HGETALL</span>                       | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">HINCRBY</span>                       | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">HINCRBYFLOAT</span>                  | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">HKEYS</span>                         | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">HLEN</span>                          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">HMGET</span>                         | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">HMSET</span>                         | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">HRANDFIELD</span>                    | <span class="support partial">Partially supported</span> |
|                                              | <span class="command">HSCAN</span>                         | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">HSET</span>                          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">HSETNX</span>                        | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">HSTRLEN</span>                       | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">HVALS</span>                         | <span class="support supported">Fully supported</span>   |
| <span class="family">HyperLogLog</span>      | <span class="command">PFADD</span>                         | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">PFMERGE</span>                       | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">PFCOUNT</span>                       | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">PFDEBUG</span>                       | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">PFSELFTEST</span>                    | <span class="support unsupported">Unsupported</span>     |
| <span class="family">List</span>             | <span class="command">BRPOPLPUSH</span>                    | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">BRPOP</span>                         | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">BLMPOP</span>                        | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">LINDEX</span>                        | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">LINSERT</span>                       | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">LLEN</span>                          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">LMOVE</span>                         | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">LPUSH</span>                         | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">LRANGE</span>                        | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">LSET</span>                          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">LTRIM</span>                         | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">RPOPLPUSH</span>                     | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">RPUSH</span>                         | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">RPUSHX</span>                        | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">RPOP</span>                          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">LREM</span>                          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">LPUSHX</span>                        | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">LMPOP</span>                         | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">LPOS</span>                          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">LPOP</span>                          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">BLPOP</span>                         | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">BLMOVE</span>                        | <span class="support supported">Fully supported</span>   |
| <span class="family">PubSub</span>           | <span class="command">PSUBSCRIBE</span>                    | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">PUBLISH</span>                       | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">PUBSUB CHANNELS</span>               | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">PUBSUB NUMPAT</span>                 | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">PUBSUB NUMSUB</span>                 | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">PUBSUB SHARDCHANNELS</span>          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">PUBSUB SHARDNUMSUB</span>            | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">PUNSUBSCRIBE</span>                  | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">SPUBLISH</span>                      | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">SSUBSCRIBE</span>                    | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">SUNSUBSCRIBE</span>                  | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">SUBSCRIBE</span>                     | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">UNSUBSCRIBE</span>                   | <span class="support supported">Fully supported</span>   |
| <span class="family">Scripting</span>        | <span class="command">EVAL</span>                          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">EVAL_RO</span>                       | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">EVALSHA</span>                       | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">EVALSHA_RO</span>                    | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">FCALL</span>                         | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">FUNCTION FLUSH</span>                | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">FUNCTION</span> \*                   | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">SCRIPT LOAD</span>                   | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">SCRIPT EXISTS</span>                 | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">SCRIPT FLUSH</span>                  | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">SCRIPT DEBUG</span>                  | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">SCRIPT KILL</span>                   | <span class="support unsupported">Unsupported</span>     |
| <span class="family">Server</span>           | <span class="command">ACL CAT</span>                       | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">ACL DELUSER</span>                   | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">ACL DRYRUN</span>                    | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">ACL GENPASS</span>                   | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">ACL GETUSER</span>                   | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">ACL LIST</span>                      | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">ACL LOAD</span> v                    | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">ACL LOG</span>                       | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">ACL SAVE</span>                      | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">ACL SETUSER</span>                   | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">ACL USERS</span>                     | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">ACL WHOAMI</span>                    | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">BGREWRITEAOF</span>                  | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">BGSAVE</span>                        | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">COMMAND</span>                       | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">COMMAND COUNT</span>                 | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">COMMAND DOCS</span>                  | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">COMMAND GETKEYS</span>               | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">COMMAND GETKEYSANDFLAGS</span>       | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">COMMAND INFO</span>                  | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">COMMAND LIST</span>                  | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CONFIG GET</span>                    | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CONFIG RESETSTAT</span>              | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">CONFIG REWRITE</span>                | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">CONFIG SET</span>                    | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">DBSIZE</span>                        | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">FAILOVER</span>                      | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">FLUSHALL</span>                      | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">FLUSHDB</span>                       | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">INFO</span>                          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">LASTSAVE</span>                      | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">LATENCY DOCTOR</span>                | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">LATENCY GRAPH</span>                 | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">LATENCY HISTOGRAM</span>             | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">LATENCY HISTORY</span>               | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">LATENCY LATEST</span>                | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">LATENCY RESET</span>                 | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">LOLWUT</span>                        | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">MEMORY DOCTOR</span>                 | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">MEMORY MALLOC-STATS</span>           | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">MEMORY PURGE</span>                  | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">MEMORY STATS</span>                  | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">MEMORY USAGE</span>                  | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">MODULE LIST</span>                   | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">MODULE LOAD</span>                   | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">MODULE LOADEX</span>                 | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">MODULE UNLOAD</span>                 | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">MONITOR</span>                       | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">REPLICAOF</span>                     | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">ROLE</span>                          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">SAVE</span>                          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">SHUTDOWN</span>                      | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">SLAVEOF</span>                       | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">SLOWLOG GET</span>                   | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">SLOWLOG LEN</span>                   | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">SLOWLOG RESET</span>                 | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">SWAPDB</span>                        | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">TIME</span>                          | <span class="support supported">Fully supported</span>   |
| <span class="family">Set</span>              | <span class="command">SADD</span>                          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">SCARD</span>                         | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">SDIFF</span>                         | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">SDIFFSTORE</span>                    | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">SINTER</span>                        | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">SINTERCARD</span>                    | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">SINTERSTORE</span>                   | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">SISMEMBER</span>                     | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">SMEMBERS</span>                      | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">SMISMEMBER</span>                    | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">SMOVE</span>                         | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">SPOP</span>                          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">SRANDMEMBER</span>                   | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">SREM</span>                          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">SSCAN</span>                         | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">SUNION</span>                        | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">SUNIONSTORE</span>                   | <span class="support supported">Fully supported</span>   |
| <span class="family">Sorted Set</span>       | <span class="command">BZMPOP</span>                        | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">BZPOPMZX</span>                      | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">BZPOPMIN</span>                      | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">ZADD</span>                          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">ZCARD</span>                         | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">ZCOUNT</span>                        | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">ZDIFF</span>                         | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">ZDIFFSTORE</span>                    | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">ZINCRBY</span>                       | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">ZINTER</span>                        | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">ZINTERCARD</span>                    | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">ZINTERSTORE</span>                   | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">ZLEXCOUNT</span>                     | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">ZMPOP</span>                         | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">ZMSCORE</span>                       | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">ZPOPMAX</span>                       | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">ZPOPMIN</span>                       | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">ZRANDMEMBER</span>                   | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">ZRANGE</span>                        | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">ZRANGEBYLEX</span>                   | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">ZRANGEBYSCORE</span>                 | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">ZRANK</span>                         | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">ZREM</span>                          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">ZREMRANGEBYLEX</span>                | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">ZREMRANGEBYRANK</span>               | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">ZREMRANGEBYSCORE</span>              | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">ZREVRANGE</span>                     | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">ZREVRANGEBYLEX</span>                | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">ZREVRANGEBYSCORE</span>              | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">ZREVRANK</span>                      | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">ZSCAN</span>                         | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">ZSCORE</span>                        | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">ZUNION</span>                        | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">ZUNIONSTORE</span>                   | <span class="support supported">Fully supported</span>   |
| <span class="family">Stream</span>           | <span class="command">XAUTOCLAIM</span>                    | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">XCLAIM</span>                        | TBD                                                      |
|                                              | <span class="command">XREAD</span>                         | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">XADD</span>                          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">XPENDING</span>                      | TBD                                                      |
|                                              | <span class="command">XGROUP</span>                        | <span class="support partial">Partially supported</span> |
|                                              | <span class="command">XRANGE</span>                        | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">XSETID</span>                        | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">XREVRANGE</span>                     | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">XREADGROUP</span>                    | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">XDEL</span>                          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">XINFO</span>                         | <span class="support partial">Partially supported</span> |
|                                              | <span class="command">XACK</span>                          | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">XTRIM</span>                         | <span class="support partial">Partially supported</span> |
| <span class="family">String</span>           | <span class="command">APPEND</span>                        | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">DECR</span>                          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">DECRBY</span>                        | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">GET</span>                           | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">GETDEL</span>                        | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">MSGETEXET</span>                     | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">GETRANGE</span>                      | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">GETSET</span>                        | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">INCR</span>                          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">INCRBY</span>                        | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">INCRBYFLOAT</span>                   | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">LCS</span>                           | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">MGET</span>                          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">MSET</span>                          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">MSETNX</span>                        | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">PSETEX</span>                        | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">SET</span>                           | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">SETEX</span>                         | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">SETNX</span>                         | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">SETRANGE</span>                      | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">STRLEN</span>                        | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">SUBSTR</span>                        | <span class="support supported">Fully supported</span>   |
| <span class="family">Transactions</span>     | <span class="command">DISCARD</span>                       | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">EXEC</span>                          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">MULTI</span>                         | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">UNWATCH</span>                       | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">WATCH</span>                         | <span class="support supported">Fully supported</span>   |
| <span class="family">Bloom Filter</span>     | <span class="command">TBD</span>                           | <span class="support unsupported">Unsupported</span>     |
| <span class="family">Cuckoo Filter</span>    | <span class="command">TBD</span>                           | <span class="support unsupported">Unsupported</span>     |
| <span class="family">Count-min Sketch</span> | <span class="command">TBD</span>                           | <span class="support unsupported">Unsupported</span>     |
| <span class="family">Graph</span>            | <span class="command">TBD</span>                           | <span class="support unsupported">Unsupported</span>     |
| <span class="family">JSON</span>             | <span class="command">ARRAPPEND</span>                     | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">ARRINDEX</span>                      | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">ARRINSERT</span>                     | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">ARRLEN</span>                        | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">ARRPOP</span>                        | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">ARRTRIM</span>                       | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">CLEAR</span>                         | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">DEBUG</span>                         | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">DEBUG MEMORY</span>                  | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">DEL</span>                           | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">FORGET</span>                        | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">GET</span>                           | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">MERGE</span>                         | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">MGET</span>                          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">MSET</span>                          | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">NUMINCRBY</span>                     | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">NUMMULTBY</span>                     | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">OBJKEYS</span>                       | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">OBJLEN</span>                        | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">RESP</span>                          | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">SET</span>                           | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">STRAPPEND</span>                     | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">STRLEN</span>                        | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">TOGGLE</span>                        | <span class="support supported">Fully supported</span>   |
|                                              | <span class="command">TYPE</span>                          | <span class="support supported">Fully supported</span>   |
| <span class="family">Search</span>           | <span class="command">FT.CREATE</span>                     | <span class="support unsupported">Unsupported</span>     |
|                                              | <span class="command">FT.SEARCH</span>                     | <span class="support unsupported">Unsupported</span>     |
| <span class="family">Auto Suggest</span>     | <span class="command">TBD</span>                           | <span class="support unsupported">Unsupported</span>     |
| <span class="family">T-Digest</span>         | <span class="command">TBD</span>                           | <span class="support unsupported">Unsupported</span>     |
| <span class="family">Time Series</span>      | <span class="command">TBD</span>                           | <span class="support unsupported">Unsupported</span>     |
| <span class="family">Top-K</span>            | <span class="command">TBD</span>                           | <span class="support unsupported">Unsupported</span>     |
