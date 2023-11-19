---
sidebar_position: 5
---

# Scripting with Lua

Dragonfly allows users to execute scripts written in [Lua](https://lua.org). Its interface for managing and writing scripts its compatible with the [interface provided by Redis](https://redis.io/docs/manual/programmability/eval-intro/).

Dragonfly uses Lua version 5.4.

## Script flags

Dragonfly provides additional flexibility with special script flags. By default, none are set. 

Flags can be configured in multiple ways:

#### 1. Inside the script souce code

```lua
#!lua flags=allow-undeclared-keys,disable-atomicity
-- script body below
```

#### 2. As default flags

Default flags are applied to all scripts and can be provided as an argument to Dragonfly.

`./dragonfly --default_lua_flags=allow-undeclared-keys,disable-atomicity`


#### 3. With `SCRIPT FLAGS` command

Flags can be set for a script by its SHA.

`SCRIPT FLAGS sha1 disable-atomicity allow-undeclared-keys`

This command can be called even *before the script is loaded*. This makes it possible to patch scripts used by frameworks or side applications.

First, determine what SHAs are used by the framework/application. This can be done with the `SCRIPT LIST` command. Then, before starting the framework/application, call `SCRIPT FLAGS sha1 [flags ...]` for all required scripts with the desired flags.

### Allowing undeclared keys

Dragonfly forbids accessing undeclared keys from scripts and returns the following error: 

```
script tried accessing undeclared key
```
 
To allow accessing any keys, including undeclared, the flag `allow-undeclared-keys` should be used. 
This option is disabled by default because unpredictability, atomicity and multithreading don't mix well. If enabled, Dragonlfy has to stop all other operations when the script is running.

### Disabling atomicity

Disabling atomicity for a script allows Dragonfly to execute commands that access any of the declared keys while the script is still running. The script's execution can be compared to a series of pipelined commands, only that it's not produced by a remote client, but the script itself.

The `disable-atomicity` flag disables atomicity. 

This behavior can be useful for long running scripts that don't require strict atomicity. Because the keys will always be available to other clients for both reads and writes, latency spikes can be avoided.

Dragonfly's asynchronous model keeps this flag functional even on with low number of cores. Please note that a script can only be interrupted when calling commands. Intensive computations can still cause latency spikes. 
