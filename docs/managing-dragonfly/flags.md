# Server Configuration Flags

Dragonfly can be tuned and configured by a set of config flags. These flags can be:

1. Passed to a Dragonfly as command line arguments. E.g, `dragonfly --port=6379`.
2. Loaded from a file. E.g. `dragonfly --flagfile=path_to_flags/flags.txt`
3. Can be set via env variables by adding the prefix `DFLY_` followed by the flag name. E.g. `export DFLY_port=6379` (note it's case sensitive)
4. At runtime via `CONFIG SET` command. Not all flags can be configured at runtime.

You can try `dragonfly --helpfull` to get a list of all flags or `--help=substring` shows help for
flags which include specified substring in either in the name, description or path.

## Available Flags

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

### `--dir`
  Working directory

  `default: ""`

### `--snapshot_cron`
  Cron expression for the time to save a snapshot, crontab style.

  `default:`

### `--admin_bind`
  If set, the admin console TCP connection would be bind to the given address. 
  This supports both HTTP and RESP protocols. 

  `default: ""`

### `--admin_port`
  If set, would enable admin access to console on the assigned port. 
  This supports both HTTP and RESP protocols. 

  `default: 0`

### `--max_client_iobuf_len`
  Maximum io buffer length that is used to read client requests.

  `default: 64.0KiB`

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

### `--publish_buffer_limit`
  Amount of memory to use for storing pub commands in bytes - per IO thread.

  `default: 128.00MiB`

### `--pipeline_squash`
  Number of queued pipelined commands above which squashing is enabled, 0 means disabled. 

  `default: 1`

### `--primary_port_http_enabled`
  If true allows accessing http console on main TCP port.

  `default: true`

### `--request_cache_limit`
  Amount of memory to use for request cache in bytes per IO thread. 

  `default: 64.00MiB`

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
  The period in seconds of inactivity after which keep-alives are triggerred,
  the duration until an inactive connection is terminated is twice the specified time.

  `default: 300`

### `--timeout`
  Close the connection after it is idle for N seconds (`0` to disable).

  `default: 0`

### `--tls`
  Enable tls.

  `default: false`

### `--tls_ca_cert_dir`
  Certified authority signed certificates directory. Use [`c_rehash`](https://www.openssl.org/docs/man3.0/man1/c_rehash.html) on the directory before specifying this flag.

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
  Change the name of commands, format is: `<cmd1_name>=<cmd1_new_name>, <cmd2_name>=<cmd2_new_name>`

  `default:`

### `--restricted_commands`
  Commands restricted to connections on the admin port.

  `default:`

### `--lock_on_hashtags`
  When true, locks are done in the \{hashtag\} level instead of key level. Only use this with `--cluster_mode=emulated|yes`.
  
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

### `--masterauth`
  Password for authentication with master. 

  `default: ""`

### `--replicaof`
  Specifies a host and port which point to a target master to replicate.
  Format should be `<IPv4>:<PORT>` or `host:<PORT>` or `[<IPv6>]:<PORT>`.

  `default:`

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
  When non-empty, keys which start with this prefix are not distributed across shards based on their value but instead
  via round-robin. Use cautiously! This can efficiently support up to a few hundreds of prefixes. Note: prefix is 
  looked inside hashtags when cluster mode is enabled.

  `default: ""`

### `--tiered_prefix`
  Enables tiered storage if set. The string denotes the path and prefix of the files associated
  with tiered storage. For example, `tiered_prefix=/path/to/file-prefix`.

  `default: ""`

### `--tiered_offload_threshold`
  Ratio of free memory (free/max memory) below which offloading starts

  `default: 0.5`

### `--tiered_upload_threshold`
  Ratio of free memory (free/max memory) below which uploading stops. 

  `default: 0.1`

### `--tiered_min_value_size`
  Minimum size of values eligible for offloading. Must be at least 64

  `default: 64`

### `--keys_output_limit`
  Maximum number of keys output by keys command.
  
  `default: 8192`

### `--backing_file_direct`
  If true uses `O_DIRECT` to open backing files.

  `default: true`

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

### `--multi_exec_squash`
  Whether multi exec will squash single shard commands to optimize performance. 

  `default: true`

### `--num_shards`
  Number of database shards, 0 - to choose automatically.
  
  `default: 0`

### `--tls_replication`
  Enable TLS on replication. 

  `default: false`

### `--compression_level`
  The compression level to use on zstd/lz4 compression.

  `default: 2`

### `--compression_mode`
  Set 0 for no compression, set 1 for single entry lzf compression, set 2 for multi entry zstd compression on
  df snapshot and single entry on rdb snapshot, set 3 for multi entry lz4 compression on df snapshot and
  single entry on rdb snapshot.

  `default: 3`

  Where:
  - `0` — `NONE` — single-entry, no compression.
  - `1` — `SINGLE_ENTRY` — single entry lzf compression.
  - `2` — `MULTI_ENTRY_ZSTD` — multi entry zstd compression on df snapshot and single entry on rdb snapshot.
  - `3` — `MULTI_ENTRY_LZ4` — multi entry lz4 compression on df snapshot and single entry on rdb snapshot.

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

  `default: 1000`

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

### `--serialization_max_chunk_size`
  Maximum size of a value that may be serialized at once during snapshotting or full sync.
  Values bigger than this threshold will be serialized using streaming serialization. 
  0 - to disable streaming mode.
  
  `default: 65536`

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

  `default: 8192`

### `--proactor_affinity_mode`
  Can be on, off or auto. 

  `default: "on"`

### `--proactor_threads`
  Number of io threads in the pool. If zero is specified, it will use as many as there are CPU cores.

  `default: 0`

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

### `--logbuflevel`
  Buffer log messages logged at this level or below. (-1 means don't buffer; 0 means buffer INFO only).

  `default: 0`

### `--logbufsecs`
  Buffer log messages for at most this many seconds.

  `default: 30`

### `--max_log_size`
  Approx. maximum log file size (in MB). A value of 0 will be silently overridden to 1. 

  `default: 200`

### `--minloglevel`
  Messages logged at a lower level than this don't actually get logged anywhere. 

  `default: 0`

### `--stderrthreshold`
  Log messages at or above this level are copied to stderr in addition to logfiles. This flag obsoletes --alsologtostderr
  
  `default: 2`

### `--command_alias`
  Add an alias for given commands, format is: `<alias>=<original>, <alias>=<original>`

  `default:`

### `--allocation_tracker`
  Logs stack trace of memory allocation within these ranges. Format is `min:max,min:max,...`.

  `default: ""`

### `--always_flush_pipeline`
  If true, will flush pipeline response after each pipeline squashing.

  `default: false`

### `--announce_port`
  Port that Dragonfly announces to cluster clients and replication master.

  `default: 0`

### `--async_dispatch_quota`
  Maximum number of consecutive async dispatch messages to process before either yielding to I/O when the pipeline appears empty or forcibly processing a queued pipelined command to prevent starvation. Set to 0 to disable this mechanism.

  `default: 100`

### `--availability_zone`
  Server availability zone, used by clients to read from local-zone replicas.

  `default: ""`

### `--background_debug_jobs`
  Use background fibers for debug jobs.

  `default: false`

### `--background_heartbeat`
  Whether to run heartbeat as a background fiber.

  `default: false`

### `--background_snapshotting`
  Whether to run snapshot as a background fiber.

  `default: false`

### `--break_replication_on_master_restart`
  When in replica mode, and master restarts, break replication from master to avoid flushing the replica's data.

  `default: false`

### `--cluster_coordinator_connect_timeout_ms`
  Timeout in milliseconds for coordinator to connect to remote shards.

  `default: 3000`

### `--cluster_coordinator_response_timeout_ms`
  Timeout in milliseconds for coordinator to read responses from remote shards.

  `default: 3000`

### `--cluster_flush_decommit_memory`
  Decommit memory after flushing slots.

  `default: false`

### `--cluster_node_id`
  ID within a cluster, used for slot assignment. MUST be unique. If empty, uses master replication ID (random string).

  `default: ""`

### `--cluster_search`
  Enable search commands for cross-shard search. Turned off by default for safety.

  `default: false`

### `--container_iteration_yield_interval_usec`
  Yield the fiber every N microseconds during container iteration. 0 disables yielding.

  `default: 0`

### `--deserialize_hnsw_index`
  Deserialize HNSW vector index graph structure.

  `default: false`

### `--disable_json_defragmentation`
  If true, disable json object defragmentation.

  `default: false`

### `--enable_heartbeat_rss_eviction`
  Enable eviction during heartbeat when rss memory is under pressure. Eviction based on used_memory will still be enabled.

  `default: true`

### `--enable_memcache_io_loop_v2`
  Enable the event-driven IoLoopV2 for non-TLS Memcache connections.

  `default: true`

### `--enable_resp_io_loop_v2`
  Enable the event-driven IoLoopV2 for non-TLS RESP connections.

  `default: false`

### `--enable_tcp_defer_accept`
  Enable TCP_DEFER_ACCEPT option on server sockets.

  `default: true`

### `--eviction_memory_budget_threshold`
  Eviction starts when the free memory (including RSS memory) drops below `eviction_memory_budget_threshold * max_memory_limit`.

  `default: 0.1`

### `--experimental_cluster_shard_by_slot`
  If true, cluster mode is enabled and sharding is done by slot. Otherwise, sharding is done by hash tag.

  `default: false`

### `--experimental_flat_json`
  If true, uses flat json implementation.

  `default: false`

### `--experimental_replicaof_v2`
  Use ReplicaOfV2 algorithm for initiating replication.

  `default: true`

### `--expose_http_api`
  If set, will expose a POST `/api` handler for sending redis commands as json array.

  `default: false`

### `--fiber_run_warning_threshold_ms`
  If greater than 0, will warn if a fiber runs longer than this threshold (in milliseconds).

  `default: 0`

### `--fiber_safety_margin`
  If > 0, ensures the stack each fiber has at least this margin. The check is done at fiber destruction time.

  `default: 1024`

### `--gcs_auth_token`
  Authentication token for Google Cloud Storage access.

  `default: ""`

### `--gcs_dry_upload`
  If true, performs a dry run upload to Google Cloud Storage without actually writing data.

  `default: false`

### `--huffman_table`
  A comma separated map: `domain1:code1,domain2:code2,...` where domain can currently be only `KEYS` or `STRINGS`, code is a base64-encoded huffman table exported via `DEBUG COMPRESSION EXPORT`. If the flag is empty no huffman compression is applied.

  `default: ""`

### `--info_replication_valkey_compatible`
  When true, output valkey compatible values for info-replication.

  `default: true`

### `--journal_omit_redundant_writes`
  If true, omit journal writes for keys during full sync that are yet to be reached by the serialization loop. Reduces full sync overhead.

  `default: true`

### `--jsonpathv2`
  If true, uses Dragonfly jsonpath implementation, otherwise uses legacy jsoncons implementation.

  `default: true`

### `--keep_legacy_memory_metrics`
  When true, keeps the legacy metrics format for memory-related info fields.

  `default: true`

### `--latency_tracking`
  If true, track latency for commands.

  `default: false`

### `--list_experimental_zstd_dict_threshold`
  Minimum list malloc usage in bytes before attempting ZSTD dictionary compression. 0 disables. Experimental: compression is synchronous and may block the thread.

  `default: 0`

### `--list_tiering_threshold`
  Tiering threshold for lists. Default - no tiering.

  `default: 0`

### `--listpack_max_bytes`
  Maximum total bytes of a hash in listpack encoding before converting to a hash table.

  `default: 1024`

### `--listpack_max_field_len`
  Maximum length of a hash field or value to be stored in listpack encoding.

  `default: 64`

### `--locktag_delimiter`
  If set, this char is used to extract a lock tag by looking at delimiters, like hash tags. If unset, regular hashtag extraction is done (with `{}`). Must be used with `--lock_on_hashtags`.

  `default: ""`

### `--locktag_prefix`
  Only keys with this prefix participate in tag extraction.

  `default: ""`

### `--locktag_skip_n_end_delimiters`
  How many closing tag delimiters should we skip when extracting lock tags. 0 for no skipping. For example, when delimiter is `:` and this flag is 2, the locktag for `:a:b:c:d:e` will be `a:b:c`.

  `default: 0`

### `--log_squash_info_threshold_usec`
  Threshold in microseconds above which to log squashing timings.

  `default: 2147483648`

### `--lua_allow_undeclared_auto_correct`
  If enabled, when a script that is not allowed to run with undeclared keys is trying to access undeclared keys, automatically set the script flag to be able to run with undeclared key.

  `default: false`

### `--lua_enable_redis_log`
  Enable `redis.log` to write logs from lua script.

  `default: false`

### `--lua_float_as_int_shas`
  Comma-separated list of Lua script SHAs which should return floats as integers. SHAs are only looked at when loading the script.

  `default:`

### `--lua_mem_gc_threshold`
  Specifies Lua interpreter's per thread memory limit in bytes after which the GC will be called forcefully. 0 value removes forced GC calls.

  `default: 10000000`

### `--lua_resp2_legacy_float`
  Return rounded down integers instead of floats for lua scripts with RESP2.

  `default: false`

### `--lua_undeclared_keys_shas`
  Comma-separated list of Lua script SHAs which are allowed to access undeclared keys. SHAs are only looked at when loading the script, and new values do not affect already-loaded scripts.

  `default:`

### `--luagc`
  Specifies Lua garbage collector preferences. By default uses default lua GC parameters. Format should be `inc/200/100/13` or `gen/20/100` where `inc` and `gen` are types of GC, numbers are parameters. For more information check https://www.lua.org/manual/5.4/manual.html#2.5

  `default:`

### `--managed_service_info`
  Hides some implementation details from users when true (i.e. in managed service env).

  `default: false`

### `--masteruser`
  Username for authentication with master.

  `default: ""`

### `--max_bulk_len`
  Maximum bulk length that is allowed to be accepted when parsing RESP protocol.

  `default: 2147483648`

### `--max_busy_read_usec`
  Maximum time we read and parse from a socket without yielding, in microseconds.

  `default: 200`

### `--max_busy_squash_usec`
  Maximum time in microseconds to execute squashed commands before yielding.

  `default: 1000`

### `--max_squashed_cmd_num`
  Max number of commands squashed in a single shard during squash optimization.

  `default: 100`

### `--mem_defrag_check_sec_interval`
  Number of seconds between every defragmentation necessity check.

  `default: 60`

### `--mget_dedup_keys`
  If true, MGET will deduplicate keys.

  `default: false`

### `--migration_buckets_cpu_budget`
  How much CPU budget to use for migration buckets serialization.

  `default: 0.2`

### `--migration_buckets_serialization_threshold`
  The number of buckets to serialize on each iteration before yielding.

  `default: 10`

### `--migration_buckets_sleep_usec`
  Sleep time in microseconds after each time we reach `migration_buckets_serialization_threshold`.

  `default: 500`

### `--migration_finalization_timeout_ms`
  Timeout for migration finalization operation.

  `default: 30000`

### `--notify_keyspace_events`
  notify-keyspace-events. Only `Ex` is supported for now.

  `default: ""`

### `--omit_basic_usage`
  Omit printing basic usage info.

  `default: false`

### `--oom_deny_commands`
  Additional commands that will be marked as denyoom.

  `default:`

### `--pause_wait_timeout`
  Timeout in seconds, to set up the pause for all connections for CLIENT PAUSE command and cluster slot migration finalization procedure.

  `default: 1`

### `--pipeline_buffer_limit`
  Amount of memory to use for storing pipeline requests per IO thread. Please note that clients that send excessively huge pipelines may deadlock themselves. See https://github.com/dragonflydb/dragonfly/discussions/3997 for details.

  `default: 128.00MiB`

### `--pipeline_queue_limit`
  Pipeline queue max length. The server will stop reading from the client socket once its pipeline queue crosses this limit, and will resume once it processes excessive requests. This is to prevent OOM states. Users of huge pipeline sizes may require increasing this limit to prevent the risk of deadlocking. See https://github.com/dragonflydb/dragonfly/discussions/3997 for details.

  `default: 10000`

### `--pipeline_squash_limit`
  Limit on the size of a squashed pipeline.

  `default: 1073741824`

### `--pipeline_wait_batch_usec`
  If non-zero, waits for this time for more I/O events to come for the connection in case there is only one command in the pipeline.

  `default: 0`

### `--rdb_ignore_expiry`
  Ignore Key Expiry when loading from RDB snapshot.

  `default: false`

### `--rdb_load_dry_run`
  Dry run RDB load without applying changes.

  `default: false`

### `--rdb_sbf_chunked`
  Enable new save format for saving SBFs in chunks.

  `default: true`

### `--registered_buffer_size`
  Size of registered buffer for IoUring fixed read/writes.

  `default: 524288`

### `--replica_announce_ip`
  IP address that Dragonfly announces to replication master.

  `default: ""`

### `--replica_delete_expired`
  If true, replicas proactively delete expired keys on the read path.

  `default: true`

### `--replica_priority`
  Published by info command for sentinel to pick replica based on score during a failover.

  `default: 100`

### `--replicaof_no_one_start_journal`
  When set, preserves journal offsets after REPLICAOF NO ONE.

  `default: true`

### `--replication_dispatch_threshold`
  Number of bytes to aggregate before replication.

  `default: 1500`

### `--replication_stream_output_limit`
  Limit on the replication output buffer size (in bytes). The streamer throttles when this limit is reached.

  `default: 1048576`

### `--replication_timeout`
  Time in milliseconds to wait for the replication writes being stuck.

  `default: 30000`

### `--rss_oom_deny_ratio`
  When the ratio between maxmemory and RSS memory exceeds this value, commands marked as DENYOOM will fail with OOM error and new connections to non-admin port will be rejected. Negative value disables this feature.

  `default: 1.25`

### `--s3_use_helio_client`
  If true, use helio's native S3 client; if false, use aws-sdk-cpp. Only meaningful when compiled with AWS support; otherwise the helio client is always used.

  `default: true`

### `--save_schedule`
  Deprecated. Please use `--snapshot_cron` instead.

  `default: ""`

### `--scheduler_background_budget`
  Background fiber budget in nanoseconds.

  `default: 50000`

### `--scheduler_background_sleep_prob`
  Sleep probability of background fibers on reaching budget.

  `default: 50`

### `--scheduler_background_warrant`
  Percentage of guaranteed cpu time for background fibers.

  `default: 5`

### `--search_query_string_bytes`
  Maximum number of bytes in search query string.

  `default: 10240`

### `--search_reject_legacy_field`
  FT.AGGREGATE: Reject legacy field names.

  `default: true`

### `--send_timeout`
  Close the connection after it is stuck on send for N seconds (0 to disable).

  `default: 0`

### `--serialize_hnsw_index`
  Serialize HNSW vector index graph structure.

  `default: false`

### `--serialization_tagged_chunks`
  Allow serializer output to be split into tagged chunks and reassembled by receiver.

  `default: false`

### `--shard_thread_busy_polling_usec`
  If non-zero, overrides the busy polling parameter for shard threads.

  `default: 0`

### `--slot_migration_connection_timeout_ms`
  Connection creating timeout for migration operations.

  `default: 2000`

### `--slot_migration_throttle_us`
  Incoming migration throttle time in microseconds, throttled every 100us of migration commands processing. 0 to disable. Recommended value is 20. Values more than 50 can significantly reduce migration speed.

  `default: 0`

### `--squash_stats_latency_lower_limit`
  If set, will not track latency stats below this threshold (usec).

  `default: 0`

### `--squashed_reply_size_limit`
  Max bytes allowed for squashing_current_reply_size. If this limit is reached, connections dispatching pipelines won't squash them.

  `default: 0`

### `--subset_knn_search_threshold`
  If prefilter results are below this threshold, exact subset search will be used instead of HNSW graph search.

  `default: 8192`

### `--table_growth_margin`
  Prevents table from growing if number of free slots x average object size x this ratio is larger than memory budget.

  `default: 0.4`

### `--tcp_backlog`
  TCP listen(2) backlog parameter.

  `default: 256`

### `--tcp_user_timeout`
  The maximum period in milliseconds that transmitted data may stay unacknowledged before TCP aborts the connection. 0 means OS default timeout.

  `default: 0`

### `--tiered_experimental_cooling`
  If true, uses intermediate cooling layer when offloading values to storage.

  `default: true`

### `--tiered_experimental_hash_support`
  Experimental hash datatype offloading.

  `default: false`

### `--tiered_experimental_list_support`
  Experimental list node offloading.

  `default: false`

### `--tiered_max_file_size`
  Limit on maximum file size that is used by the database for tiered storage. 0 means the program will automatically determine its maximum file size.

  `default: 0B`

### `--tiered_max_pending_stash_bytes`
  Maximum bytes in-flight to disk before rejecting new stashes or applying client backpressure. Allows batching writes to saturate disk I/O even with few clients.

  `default: 256.0KiB`

### `--tls_cipher_suites`
  TLS ciphers configuration for TLS 1.3.

  `default: ""`

### `--tls_ciphers`
  TLS ciphers configuration for TLS 1.2.

  `default: "DEFAULT:!MEDIUM"`

### `--tls_prefer_server_ciphers`
  If true, prefer server ciphers over client ciphers.

  `default: false`

### `--tls_session_cache_size`
  Size of the cache for tls sessions.

  `default: 20480`

### `--tls_session_cache_timeout`
  Timeout for each session/ticket.

  `default: 300`

### `--tls_session_caching`
  If true, enables session caching and tickets.

  `default: false`

### `--tx_queue_warning_len`
  Length threshold for warning about long transaction queue.

  `default: 96`

### `--unlink_experimental_async`
  If true, runs unlink command asynchronously.

  `default: true`

### `--uring_direct_table_len`
  If positive, create direct fd table of this length.

  `default: 0`

### `--uring_disable_iowait`
  If true, disables iowait cpu accounting.

  `default: false`

### `--uring_recv_buffer_cnt`
  How many buffer ring entries to allocate per thread for io_uring receive operations. Relevant only for modern kernels with io_uring enabled.

  `default: 0`

### `--use_numeric_range_tree`
  Use range tree for numeric index. If false, use a simple implementation with btree_set. Range tree is more memory efficient and faster for range queries, but slower for single value queries.

  `default: true`

### `--use_oah_set`
  If true, store SET values in OAHSet instead of StringSet.

  `default: false`

### `--user`
  If not empty - drop privileges to this user (and their primary group) after binding ports. Accepts username or numeric uid. If `--dir` is set, chowns the data directory to this user.

  `default: ""`
