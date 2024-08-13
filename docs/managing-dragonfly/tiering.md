---
sidebar_position: 5
---

# SSD Data Tiering

Dragonfly v1.21.0 introduces a powerful new feature: SSD data tiering. With it, Dragonfly
can leverage SSD/NVMe devices as a secondary storage tier that complements
RAM. By intelligently offloading specific data to fast disk storage,
Dragonfly can significantly reduce physical memory usage, potentially
achieving a 2x-5x improvement while maintaining sub-millisecond average latency.

## How It Works

Dragonfly's data tiering focuses on string values exceeding 64 characters in size.
When enabled, these longer strings are offloaded to the SSD tier.
Shorter strings and other data types, along with the primary hashtable index,
remain in high-speed memory for rapid lookup. This tiered approach maintains high performance
while reducing memory consumption. When accessed, offloaded data is seamlessly retrieved from
SSD and integrated back into memory. Write, delete, and expire operations are managed
entirely in-memory, leveraging disk-based keys for efficient operation.


## Enabling Data tiering
The feature can be enable by passing `--tiered_prefix <nvme_path>/<basename>` flag.
Dragonfly will automatically check the free disk space on the partition hosting `<nvme_path>` and
will deduce the maximum capacity it can use. In order to explicitly set the maximum
disk space capacity, for data tiering you can use `--tiered_max_file_size=<size>`. For example,
`--tiered_max_file_size=96G`.

## Checking Data tiering metrics

**Dragonfly provides detailed metrics to help you monitor and analyze data tiering performance.**
When running `redis-cli info tiered` you get the following metrics:

* **tiered_entries:**  - how many values are offloaded.
* **tiered_entries_bytes:** - how much data was offloaded in bytes
* **tiered_total_stashes:** - how many offload requests were issued
* **tiered_total_fetches:** - how many times the offloaded items were read from disk
* **tiered_total_deletes:** - how many times the offloaded items were deleted from disk
* **tiered_total_uploads:** - how many times the offloaded items were promoted back to RAM
* **tiered_allocated_bytes:** - how much disk space was used by data tiering.
* **tiered_capacity_bytes:** - the maximum size of tiered on-disk capacity.
* **tiered_pending_read_cnt:**   - currently pending io read requests. A high number indicates
that the server is bottlenecked on disk read i/o.
* **tiered_pending_stash_cnt:**  - currently pending io write requests. A high number indicates that
the server is bottlenecked on disk write i/o.
* **tiered_cold_storage_bytes:** - cooling queue capacity in bytes
* **tiered_ram_hits:**           - how many times an entry lookup resulted in in-memory hit
* **tiered_ram_misses:**         - how many times an entry lookup resulted in a disk read
* **tiered_ram_cool_hits:**      - how many times an entry lookup resulted in cooling buffer hit.

## Performance
Performance benchmarks against Elasticache instances and Memcached,
conducted on AWS instances, demonstrate Dragonfly's superior performance.
We've conducted loadtests using `r6gd.xlarge` instance on AWS and compared Dragonfly against
datastore with similar features, namely Elasticache Data tiering `cache.r6gd.xlarge` instance and
self-hosted Memcached/ExtStore server also running on `r6gd.xlarge`. The test consisted of
writing a 90GB dataset into all stores and then reading them randomly with uniform distribution.

During the write phase with 200K rps, Memcached had to drop 20% of the workload in order
to cope with memory pressure, while Elasticache throttled down the traffic to 66.5K rps.
Dragonfly handled 200K qps with 7ms P99 latency and with enough RAM reserves to digest even more
data.

During the read phase Dragonfly was the only datastore that could actually
saturate local SSD IOPS and reached 60K rps for reads. Elasticache could reach 23.5K rps
and Memcached reached only 16K rps for reads. With 60K rps throughput,
Dragonfly inhibited 5ms P99 latency, while both Memcached and Elasticache reached 190ms P99 latency.

## System requirements
Dragonfly Data Tiering requires Linux kernel version 5.19 or higher with io_uring API enabled.
**io_uring API is a critical requirement** for SSD Data tiering. Additionally, it requires
that `<nvme_path>` points to a relatively fast SSD disk. For cloud workloads, using instances
with locally attached SSDs is recommended. See below for specific cloud provider suggestions.

### GCP
GCP has excellent local SSD hardware that has great performance characteristics.
Any instance with local SSD storage will suffice.

### AWS
AWS provides a variety of instance families with local SSD disks attached.
You can refer to the [following table](https://docs.aws.amazon.com/ec2/latest/instancetypes/mo.html#mo_instance-store)
for detailed performance characteristics of local SSDs for each instance type.
We recommend choosing an instance type from the r6gd or m6gd families.


## Notes
Data tiering is currently in alpha, which means it's under development and may have
limited functionality or stability. If you encounter any issues while using data tiering,
please report them by [filing an issue](https://github.com/dragonflydb/dragonfly/issues/).

**Limitations:**
* Data tiering is not currently supported by BITOP operations.