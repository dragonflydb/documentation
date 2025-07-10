---
description: Learn how to use Redis XSETID to set the last delivered ID for streams.
---

import PageTitle from '@site/src/components/PageTitle';

# XSETID

<PageTitle title="Redis XSETID Command (Documentation) | Dragonfly" />

## Introduction

The `XSETID` command is an internal command. It is used by a Dragonfly primary instance to replicate the last delivered ID of streams.

## Syntax

```shell
XSETID key last-id
```

## Parameter Explanations

- `key`: The stream for which you want to set the last delivered ID.
- `last-id`: The last delivered ID of a stream to set.

## Return Values

- The command returns `OK` if the ID for the consumer group is successfully set.
