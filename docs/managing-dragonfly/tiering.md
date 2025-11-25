---
sidebar_position: 5
---

# SSD Data Tiering

Dragonfly v1.35 ([v1.35.0](https://github.com/dragonflydb/dragonfly/releases/tag/v1.35.0) &
[v1.35.1](https://github.com/dragonflydb/dragonfly/releases/tag/v1.35.1)) introduces a powerful new feature: **SSD Data Tiering**.
With it, Dragonfly can leverage SSD/NVMe devices as a secondary storage tier that complements
RAM. By intelligently offloading specific data to fast disk storage,
Dragonfly can significantly reduce physical memory usage, potentially
achieving a 2x-5x improvement while maintaining sub-millisecond average latency.

Dragonfly's data tiering currently focuses on large string values (those exceeding 64 characters by default).
When enabled, these longer strings are offloaded to the SSD tier.
Shorter strings and other data types, along with the primary hashtable index,
remain in high-speed memory for rapid lookup. This tiered approach maintains high performance
while reducing memory consumption. When accessed, offloaded data is seamlessly retrieved from
SSD and integrated back into memory. Write, delete, and expire operations are managed
entirely in-memory, leveraging disk-based keys for efficient operation.

---

## Configuring Data Tiering

The feature can be enabled by passing the `--tiered_prefix <nvme_path>/<basename>` flag.
Dragonfly will automatically check the free disk space on the partition hosting the `<nvme_path>`
to determine the maximum capacity it can use. Finally, it creates one storage file for
each [proactor thread](http://localhost:3000/docs/managing-dragonfly/flags#--proactor_threads),
corresponding to the number of threads Dragonfly is running with.

Here are the main server flags related to SSD data tiering:

- `tiered_prefix`: The path and base file name for SSD data tiering. **This flag also enables the feature overall**.
  Note that when SSD data tiering is enabled, new values are always placed on disk immediately after creation.
  See upload/offload thresholds and examples below for more details.
- `tiered_offload_threshold`: The ratio of free memory, below which values will be actively offloaded to disk by a background process.
- `tiered_upload_threshold`: The ratio of free memory, below which values are no longer returned to memory when read.
- `tiered_storage_write_depth`: The maximum number of concurrent disk writes to avoid overloading the disk.
- `tiered_max_file_size`: The maximum file size in bytes (must be multiples of 256MB), usually determined automatically.
- `tiered_min_value_size`: This option can be used to raise the 64-byte value limit to offload only larger values.
- `registered_buffer_size`: The size of registered buffers to use for zero-copy reads and writes with `io_uring`.
- `tiered_experimental_cooling`: Whether to use experimental cooling. See below for more details.

For example:

```shell
$> ./dragonfly --maxmemory=20G \
               --tiered_prefix=/mnt/fast-ssd/dragonfly-tiered-file \
               --tiered_upload_threshold=0.2 \
               --tiered_offload_threshold=0.4
```

The command above configures Dragonfly to:

- Run with a memory limit of 20GB.
- When the memory usage is above 16GB (less than 20% free), values read from disk will be returned to the client directly without being promoted back to memory.
- New values are offloaded to disk immediately, but active background offloading starts only when 12GB (less than 40% free) or more memory is used.
- In between 12GB and 16GB of memory usage, a continuous uploading/offloading process will keep the most recently used entries in memory and older ones on disk.

---

## Checking Data Tiering Metrics

Dragonfly provides detailed metrics to help you monitor and analyze data tiering performance.
By running the `INFO TIERED` command, you will get the following metrics:

- `tiered_entries`: The number of value entries offloaded to disk.
- `tiered_entries_bytes`: The amount of data (in bytes) offloaded to disk.
- `tiered_total_stashes`: The number of offload requests issued.
- `tiered_total_fetches`: The number of times offloaded entries were read from disk.
- `tiered_total_deletes`: The number of times offloaded entries were deleted from disk.
- `tiered_total_uploads`: The number of times offloaded entries were promoted back to memory.
- `tiered_allocated_bytes`: The amount of disk space used by data tiering.
- `tiered_capacity_bytes`: The maximum size of tiered on-disk capacity.
- `tiered_pending_read_cnt`: The number of currently pending I/O read requests. A high number indicates that the server is bottlenecked on disk read I/O.
- `tiered_pending_stash_cnt`: The number of currently pending I/O write requests. A high number indicates that the server is bottlenecked on disk write I/O.
- `tiered_cold_storage_bytes`: The cooling queue capacity in bytes.
- `tiered_ram_hits`: The number of entry lookups resulted in in-memory hits.
- `tiered_ram_misses`: The number of entry lookups resulted in disk reads.
- `tiered_ram_cool_hits`: The number of entry lookups resulted in cooling buffer hits.

### Experimental Cooling

As mentioned above, when SSD data tiering is enabled, new values are always placed on disk immediately after creation.
However, if `tiered_experimental_cooling` is enabled, a copy is also kept in memory, making the value exist both on disk and in memory.
This allows Dragonfly to quickly change an entry's state to either in-memory only (warm) or on-disk only (cold) without any pending I/O operations.
Those duplicated values are accounted for in both `tiered_entries_bytes` and `used_memory`.
However, offload and upload thresholds are determined without taking them into account.
Thus, to determine the "real" free memory amount (without values that are tiered but in the cooling state),
one has to subtract `tiered_cold_storage_bytes` from `used_memory`.

---

## Performance

Performance benchmarks against ElastiCache instances and Memcached,
conducted on AWS instances, demonstrate Dragonfly's superior performance.
We've conducted load tests using `r6gd.xlarge` instances on AWS and compared Dragonfly against
data stores with similar features, namely [ElastiCache data tiering](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/data-tiering.html)
running on the `cache.r6gd.xlarge` instance and a self-hosted
[Memcached/Extstore](https://docs.memcached.org/features/flashstorage/) server running on `r6gd.xlarge`.
The test consisted of writing a 90GB dataset into all stores and then reading them randomly with uniform distribution.

During the write phase with 200K RPS, Memcached/Extstore dropped ~18% of the workload in order
to cope with memory pressure. ElastiCache, on the other hand, throttled down the traffic to 66.5K RPS.
**Dragonfly handled 200K RPS with 8ms P99 latency and with enough memory capacity to handle even more data.**

During the read phase, Dragonfly was the only data store that could actually saturate local SSD IOPS and reached 60K RPS for reads.
ElastiCache reached 23.5K RPS, and Memcached reached only 16K RPS for reads.
**With 60K RPS throughput, Dragonfly exhibited 5ms P99 latency**,
while both ElastiCache and Memcached reached 190ms P99 latency.

---

## System Requirements

Dragonfly data tiering requires Linux kernel version 5.19 or higher with the `io_uring` API enabled.
The **`io_uring` API is a critical requirement** for this feature. Additionally, it requires
that `<nvme_path>` points to a relatively fast SSD disk. For cloud workloads, using instances
with locally attached SSDs is recommended. See below for specific cloud provider suggestions.

### GCP

- GCP has excellent local SSD hardware that has great performance characteristics.
- Any instance with local SSD storage will suffice.

### AWS

- AWS provides various instance families with local SSD disks attached.
- You can refer to [the following table](https://docs.aws.amazon.com/ec2/latest/instancetypes/mo.html#mo_instance-store)
  for detailed performance characteristics of local SSDs for each instance type.
- We recommend choosing an instance type from the `r6gd/m6gd` or higher performance instance families.

---

## Notes

- Dragonfly v1.35 (release notes for [v1.35.0](https://github.com/dragonflydb/dragonfly/releases/tag/v1.35.0)
  and [v1.35.1](https://github.com/dragonflydb/dragonfly/releases/tag/v1.35.1)) is the first official release of SSD data tiering.
- If you encounter any problems while using this feature, please report them by [filing a GitHub issue](https://github.com/dragonflydb/dragonfly/issues/).
- Data tiering is currently only for string values. But it is not supported for BitMap and HyperLogLog operations.
