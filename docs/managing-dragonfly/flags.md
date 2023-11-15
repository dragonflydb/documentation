# Command line arguments (flags)

Dragonfly can be tuned and configured by a set of config flags. These flags can be:

1. Passed to a Dragonfly as command line arguments. E.g, `dragonfly --port=6379`.
2. Loaded from a file. E.g. `dragonfly --flagfile=path_to_flags/flags.txt`
3. Can be set via env variables by adding the prefix `DFLY_` followed by the flag name. E.g. `export DFLY_port=6379` (note it's case sensitive)
4. At runtime via `CONFIG SET` command. Not all flags can be configured at runtime.

You can try `dragonfly --helpfull` to get a list of all flags or `--help=substring` shows help for
flags which include specified substring in either in the name, description or path.

## Available flags

### `--port`
  Redis port. 0 disables the port, -1 will bind on a random available port.

   `default: 6379`

### `--cache_mode`
  If true, the backend behaves like a cache, by evicting entries when getting close to maxmemory limit

  `default: false`

### `--cluster_mode`
  Set cluster mode. Available options are: `yes`, `emulated` and empty `""`.

  `default: ""`

### `--maxmemory`
  Limit on maximum-memory that is used by the database. 0 - means the program will automatically determine its maximum memory usage.

  `default: 0`

### `--dbnum`
  Number of databases.

   `default: 16`

### `--bind`
  Bind address. If empty - binds on all interfaces. It's not advised due to security implications.

  `default: ""`

### `--requirepass`
  Password for AUTH authentication.

   `default: ""`

### `--dbfilename`
  The filename to save/load the DB.

  `default: "dump-{timestamp}"`

### `--snapshot_cron`
  Cron expression for the time to save a snapshot, crontab style.

  `default:`

### `--use_set2`
  If true use DenseSet for an optimized set data structure. 

  `default: true`

### `--use_zset_tree`
  If true use b+tree for zset implementation.

  `default: true`

### ``--admin_bind`
  If set, the admin console TCP connection would be bind to the given address. 
  This supports both HTTP and RESP protocols. 

  `default: ""`

### `--admin_port`
  If set, would enable admin access to console on the assigned port. 
  This supports both HTTP and RESP protocols. 

  `default: 0`

### `--max_client_iobuf_len`
  Maximum io buffer length that is used to read client requests.

  `default: 65536`

### `--max_multi_bulk_len`
  Maximum multi-bulk (array) length that is allowed to be accepted when parsing RESP protocol

   `default: 65536`

### `--migrate_connections`
  When enabled, Dragonfly will try to migrate connections to the target thread on which they operate. Currently this is
  only supported for Lua script invocations, and can happen at most once per connection.

  `default: true`

### `--no_tls_on_admin_port`
  Allow non-tls connections on admin port.

  `default: false`

### `--pipeline_queue_limit`
  Amount of memory to use for storing pipelined commands in bytes - per IO thread.

  `default: 134217728`

### `--pipeline_squash`
  Number of queued pipelined commands above which squashing is enabled, 0 means disabled. 

  `default: 10`

### `--primary_port_http_enabled`
  If true allows accessing http console on main TCP port.

  `default: true`

### `--request_cache_limit`
  Amount of memory to use for request cache in bytes per IO thread. 

  `default: 67108864`

### `--tcp_nodelay`
  Configures dragonfly connections with socket option TCP_NODELAY. 

  `default: true`

### `--conn_io_thread_start`
  Starting thread id for handling server connections.
  
  `default: 0`

### `--conn_io_threads`
  Number of threads used for handing server connections.

  `default: 0`

### `--conn_use_incoming_cpu`
  If true uses incoming cpu of a socket in order to distribute incoming connections.

  `default: false`

### `--tcp_keepalive`
  The period in seconds of inactivity after which keep-alives are triggerred, the duration 
  until an inactive connection is terminated is twice the specified time. 

  `default: 300`

### `--tls`
  Enable tls.

  `default: false`

### `--tls_ca_cert_dir`
  Certified authority signed certificates directory.

  `default: ""`

### `--tls_ca_cert_file`
  Certified authority signed certificate to validate tls connections.

  `default: ""`

### `--tls_cert_file`
  Cert file(public key) for tls connections. 

  `default: ""`

### `--tls_key_file`
  Private Key file for tls connections.

  `default: ""`

### `--rename_command`
  Change the name of commands, format is: <cmd1_name>=<cmd1_new_name>, <cmd2_name>=<cmd2_new_name>)

  `default:`

### `--restricted_commands`
  Commands restricted to connections on the admin port.

  `default:`


### --`lock_on_hashtags`
  When true, locks are done in the {hashtag} level instead of key level. Only use this with `--cluster_mode=emulated|yes`.
  
  `default: false`

### `--enable_heartbeat_eviction`
  Enable eviction during heartbeat when memory is under pressure. 

  `default: true`

### `--max_eviction_per_heartbeat`

 The maximum number of key-value pairs that will be deleted in each eviction when heartbeat based eviction is
 triggered under memory pressure.

 `default: 100`

### `--max_segment_to_consider`

  The maximum number of dashtable segments to scan in each eviction when heartbeat based eviction is triggered under memory
  pressure.

  `default: 4`

### `--force_epoll`
  If true - uses linux epoll engine underneath. Can fit for kernels older than 5.10. 

  `default: false`

### `--pidfile`
  If not empty - server writes its pid into the file).

  `default: ""`

### `--unixsocket`

  If not empty - specifies path for the Unix socket that will be used for listening for incoming connections.

  `default: ""`

### `--unixsocketperm`
  Set permissions for unixsocket, in octal value.
   
  `default: ""`

### `--version_check`
  If true, Will monitor for new releases on Dragonfly servers once a day. 

  `default: true`

### `--hz`
  Base frequency at which the server performs other background tasks. Warning: not advised to decrease in production.

  `default: 100`

### `--mem_defrag_page_utilization_threshold`
  Memory page under utilization threshold. Ratio between used and committed size, below this, memory in
  this page will defragmented. 

  `default: 0.8`

### `--mem_defrag_threshold`
  Minimum percentage of used memory relative to maxmemory cap before running defragmentation. 

  `default: 0.7`

### `--mem_defrag_waste_threshold`
  The ratio of wasted/committed memory above which we run defragmentation. 

  `default: 0.2`

### `--shard_round_robin_prefix`
  When non-empty, keys with hash-tags, whose hash-tag starts with this prefix are not distributed 
  across shards based on their value but instead via round-robin. Use cautiously! This can 
  efficiently support up to a few hundreds of hash-tags. 

  `default: ""`

### `--spill_file_prefix`
   Enables tiered storage if set. The string denotes the path and prefix of the files associated
   with tiered storage. For example, `spill_file_prefix=/path/to/file-prefix`.

  `default: ""`

### `--keys_output_limit`
  Maximum number of keys output by keys command.
  
  `default: 8192`

### `--backing_file_direct`
  If true uses `O_DIRECT` to open backing files.

  `default: false`

### `--list_compress_depth`
  Compress depth of the list. Default is no compression. 

  `default: 0`

### `--list_max_listpack_size`
  Maximum listpack size, default is 8kb.
  
  `default: -2`

### `--admin_nopass`
  If set, would enable open admin access to console on the assigned port, without authorization needed.

  `default: false`

### `--memcached_port`
  Memcached port: 

  `default: 0`

### `--multi_eval_squash_buffer`
  Max buffer for squashed commands per script:

  `default: 4096`

### `--multi_exec_mode`
  Set multi exec atomicity mode: 1 for global, 2 for locking ahead, 3 for non atomic. 

  `default: 2`

### `--multi_exec_squash`
  Whether multi exec will squash single shard commands to optimize performance. 

  `default: true`

### `--num_shards`
  Number of database shards, 0 - to choose automatically.
  
  `default: 0`

### `--oom_deny_ratio`
  commands with flag denyoom will return OOM when the ratio between maxmemory and used memory is above this value. 

  `default: 1.1`

### `--masterauth`
  Password for authentication with master. 

  `default: ""`

### `--replicaof`
  Specifies a host and port which point to a target master to replicate.
  Format should be `<IPv4>:<PORT>` or `host:<PORT>` or `[<IPv6>]:<PORT>`.

  `default:`

### `--tls_replication`
  Enable TLS on replication. 

  `default: false`

### `--compression_level`
  The compression level to use on zstd/lz4 compression.

  `default: 2`

### `--compression_mode`
  Set 0 for no compression, set 1 for single entry lzf compression,set 2 for multi entry zstd compression on 
  df snapshot and single entry on rdb snapshot, set 3 for multi entry lz4 compression on df snapshot and 
  single entry on rdb snapshot.

  `default: 3`

### `--enable_multi_shard_sync`
  Execute multi shards commands on replica synchronized.

  `default: false`

### `--master_connect_timeout_ms`
  Timeout for establishing connection to a replication master. 

  `default: 20000`

### `--master_reconnect_timeout_ms`
  Timeout for re-establishing connection to a replication master. 

  `default: 1000`

### `--replica_partial_sync`
  Use partial sync to reconnect when a replica connection is interrupted.

  `default: true`

### `--replication_acks_interval`
  Interval between acks in milliseconds.

  `default: 3000`

### `--default_lua_flags`

  Configure default flags for running Lua scripts:

   - Use `allow-undeclared-keys` to allow accessing undeclared keys,
   - Use `disable-atomicity` to allow running scripts non-atomically.

  Specify multiple values separated by space, for example `allow-undeclared-keys disable-atomicity` 
  runs scripts non-atomically and allows accessing undeclared keys. 

  `default: ""`

### `--lua_auto_async`

  If enabled, call/pcall with discarded values are automatically replaced with acall/apcall.

  `default: false`

### `--df_snapshot_format`
  If true, save in dragonfly-specific snapshotting format

  `default: true`

### `--dir`
  Working directory

  `default: ""`

### `--epoll_file_threads`
  Thread size for file workers when running in epoll mode, default is hardware concurrent threads. 

  `default: 0`

### `--maxclients`
  Maximum number of concurrent clients allowed.
   
  `default: 64000`

### `--s3_ec2_metadata`
  Whether to load credentials and configuration from EC2 metadata. 

  `default: false`

### `--s3_endpoint`
  Endpoint for s3 snapshots, default uses aws regional endpoint. 

  `default: ""`

### `--s3_sign_payload`
  Whether to sign the s3 request payload when uploading snapshots. 

  `default: true`

### `--s3_use_https`
  Whether to use https for s3 endpoints. 

  `default: true`

### `--slowlog_log_slower_than`
  Add commands slower than this threshold to slow log. The value is expressed in microseconds 
  and if it's negative disables the slowlog.

  `default: 10000`

### `--slowlog_max_len`
  Slow log maximum length.

  `default: 20`

### `--interpreter_per_thread`
  Lua interpreters per thread

  `default: 10`

### `--enable_top_keys_tracking`
  Enables / disables tracking of hot keys debugging feature. 

  `default: false`

### `--tiered_storage_max_pending_writes`
  Maximal number of pending writes per thread. 

  `default: 32`

### `--aclfile`
  Path and name to aclfile.

  `default: ""`

### `--acllog_max_len`
  Specify the number of log entries. Logs are kept locally for each thread and therefore 
  the total number of entries are `acllog_max_len * threads`

  `default: 32`

### `--cluster_announce_ip`
  Ip that cluster commands announce to the client.

  `default: ""`

### `--shard_repl_backlog_len`
  The length of the circular replication log per shard.

  `default: 1024`

### `--proactor_affinity_mode`
  Can be on, off or auto. 

  `default: "on"`

### `--proactor_threads`
  Number of io threads in the pool. 

  `default: 0`

### `--proactor_register_fd`
  If true tries to register file descriptors.
  
  `default: false`

### `--flagfile`
  Comma-separated list of files to load flags from. 

  `default:`

### `--alsologtostderr`
  Log messages go to stderr in addition to logfiles.

  `default: false`

### `--log_dir`
  If specified, logfiles are written into this directory instead of the default logging directory.

  `default: ""`

### `--logtostderr`
  Log messages go to stderr instead of logfiles.

  `default: false`

### `--logtostdout`
  Log messages go to stdout instead of logfiles.

  `default: false`

### `--max_log_size`
  Approx. maximum log file size (in MB). A value of 0 will be silently overridden to 1. 

  `default: 1800`

### `--minloglevel`
  Messages logged at a lower level than this don't actually get logged anywhere. 

  `default: 0`

### `--stderrthreshold`
  Log messages at or above this level are copied to stderr in addition to logfiles. This flag obsoletes --alsologtostderr
  
  `default: 2`
