---
sidebar_position: 2
---

# Install from Binary

Below are step-by-step instructions for running Dragonfly from binary.

## Prerequisites

- You must be running a Linux-based OS (if using a Mac, run using [Docker](/getting-started/docker), Windows WSL will work as well).
- Network access
- Minimum 4GB of RAM to get the benefits of Dragonfly
- Minimum 1 CPU Core
- Linux Kernel 4.19 or higher

## Step 1: Download preferred release

Download the latest Dragonfly release from one of the links below. You can also checkout [all releases here](https://github.com/dragonflydb/dragonfly/releases).

- [Download Latest (Aarch64)](https://dragonflydb.gateway.scarf.sh/latest/dragonfly-aarch64.tar.gz)
- [Download Latest (X86-64)](https://dragonflydb.gateway.scarf.sh/latest/dragonfly-x86_64.tar.gz)
- [Download Latest (ARM64 Debian)](https://dragonflydb.gateway.scarf.sh/latest/dragonfly_arm64.deb)
- [Download Latest (AMD64 Debian)](https://dragonflydb.gateway.scarf.sh/latest/dragonfly_amd64.deb)

## Step 2: Uncompress and rename file

Uncompress the downloaded file and rename it to `dragonfly`:

```
tar zxf {file_name}
mv {file_name} dragonfly
```

## Step 3: Run Dragonfly

Use the following command to run Dragonfly:

```
./dragonfly --logtostderr
```

## Run Dragonfly with flags

The list of supported flags for Dragonfly can be seen by running the `--help` option, and a full list of options can be viewed with the `--helpfull` option.

A list of the most useful flags can be found [here](https://github.com/dragonflydb/dragonfly#configuration).

For example, to run dragonfly with:

- Log message at standard error
- Password (set to `youshallnotpass`)
- Cache mode enabled
- Number of db set to `1`
- Listen on port `6379` and `localhost` traffic only
- Persist data at `30` minute intervals
- Max memory set to 12GB
- The number of keys that `KEY` commands return (set to 12288)
- Set the dump file name (to `dump.db`)

You would run:

```
dragonfly --logtostderr --requirepass=youshallnotpass --cache_mode=true -dbnum 1 --bind localhost --port 6379  --snapshot_cron "*/30 * * * *" --maxmemory=12gb --keys_output_limit=12288 --dbfilename dump.rdb
```

#### Flag files

To add flags from a configuration file, use the `--flagfile <filename>` flag. The file must list one flag per line. For key-value flags, use the `--<flag_name>=<flag_value>` format (note the equals character, you can't use a space character).
