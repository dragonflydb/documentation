---
sidebar_position: 5
---

# SSD Data Tiering in Dragonfly

Dragonfly v1.21.0 introduces a powerful feature: SSD data tiering. This innovative approach optimizes
storage utilization by leveraging SSD/NVMe disks as a secondary storage tier that complements
your existing RAM. By intelligently offloading specific data to faster disk storage,
Dragonfly can significantly reduce physical memory usage, potentially achieving a 2-5x improvement.

## How It Works

Dragonfly's data tiering focuses on string values exceeding 64 characters in length.
When enabled, these longer strings are intelligently offloaded to the SSD tier,
while shorter strings and other data types remain in memory. The main hashtable index is also kept
in memory, which ensures high performant lookup operations.
The offloaded data is still accessible and seamlessly loaded back into RAM when needed for reads.


## Enabling Data tiering
The feature can be enable by passing `--tiered_prefix <nvme_path>/<basename>` flag.
Dragonfly will automatically check the free disk space on the partition hosting `<nvme_path>` and
will deduce the maximum disk space it can use. In order to manually set the maximum
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


## System requirements
Dragonfly Data Tiering requires linux kernel version 5.19 or higher with io_uring API enabled.
**io_uring API is a critical requirement** for SSD Data tiering. Additionally, it demands
that `<nvme_path>` points to a relatively fast SDD disk. For cloud workloads, using instances
with locally attached SSDs is recommended. See below for specific cloud provider suggestions.

### GCP
GCP has excellent local ssd hardware that has great performance characteristics.
Any instance with local ssd storage will suffice.

### AWS
AWS provides a variety of instance families with local SSD disks attached.
You can refer to the [following table](https://docs.aws.amazon.com/ec2/latest/instancetypes/mo.html#mo_instance-store)
for detailed performance characteristics of local SSDs for each instance type.
We recommend choosing an instance type from the r6gd or m6gd families.


## Notes
Data tiering is currently in alpha, which means it's under development and may have
limited functionality or stability. If you encounter any issues while using data tiering,
please report them by [filing an issue](https://github.com/dragonflydb/dragonfly/issues/)
**Limitation:** Data tiering is not currently supported by BITOP operations.