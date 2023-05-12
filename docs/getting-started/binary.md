---
sidebar_position: 2
---

# Install from Binary

Below are step by step instructions for running Dragonfly from binary.

## Prerequisites

- You must be running a Linux based OS (if using mac run using [Docker](getting-started/docker)). Windows WSL will work as well.
- Network access

## Download preferred file

You can download the latest Dragonfly release from one of the links below. You can also checkout [all releases here](https://github.com/dragonflydb/dragonfly/releases).

- [Download Latest (Aarch64)](https://dragonflydb.gateway.scarf.sh/{{DRAGONFLY_VERSION}}/dragonfly-aarch64.tar.gz)
- [Download Latest (X86-64)](https://dragonflydb.gateway.scarf.sh/{{DRAGONFLY_VERSION}}/dragonfly-x86_64.tar.gz)
- [Download Latest (ARM64 Debian)](https://dragonflydb.gateway.scarf.sh/{{DRAGONFLY_VERSION}}/dragonfly_arm64.deb)
- [Download Latest (AMD64 Debian)](https://dragonflydb.gateway.scarf.sh/{{DRAGONFLY_VERSION}}/dragonfly_amd64.deb)

## Uncompress and rename

Next we need to uncompress the file and rename it to 'dragonfly'

```
tar zxf {file_name}
mv {file_name} dragonfly
```

## Run Dragonfly

Run the following command to run Dragonfly.

```
./dragonfly --logtostderr
```

## Run Dragonfly with parameters

The list of supported flags for Dragonfly can be seen by running “--help” option.

The full list of options can be seen by running “--helpfull” option.

The most useful options can be found [here](https://github.com/dragonflydb/dragonfly#configuration).

For example to run dragonfly with:

- Log message at standard error
- Password (set to youshallnotpass)
- Cache mode enabled
- Number of db set to 1
- Listen on port 6379 and local host traffic only
- Persist data at 30 minutes intervals
- Max memory set to 12GB
- The number of keys that the “KEY” commands return (set to 12288)
- Set the dump file name (to dump.db)

You would run:

```
dragonfly --logtostderr --requirepass=youshallnotpass --cache_mode=true -dbnum 1 --bind localhost --port 6379  --save_schedule "*:30" --maxmemory=12gb --keys_output_limit=12288 --dbfilename dump.rdb
```

#### Flag files

Flags can be also provided from a configuration file with the `--flagfile <filename>` flag. The file should list one flag per line, with equal signs instead of spaces for key-value flags.
