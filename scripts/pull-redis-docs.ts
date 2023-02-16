#!/usr/bin/env ts-node

import path from "path";
import AdmZip from "adm-zip";
import fetch from "cross-fetch";
import fs from "fs";
import yaml from "yaml";

const DRAGONFLY_SUPPORTED_COMMANDS =
  "HMGET,EXISTS,SCARD,LINSERT,HDEL,KEYS,SETBIT,INFO,LPUSH,HSETNX,XSETID,RPOP,SET,ZUNIONSTORE,PUNSUBSCRIBE,JSON.ARRINDEX,SETNX,GETEX,BITOP,LATENCY,EXEC,HMSET,SADD,JSON.OBJLEN,JSON.CLEAR,PUBLISH,HSET,XDEL,XGROUP,PERSIST,TYPE,MULTI,LLEN,SMEMBERS,ZADD,DECR,JSON.STRAPPEND,UNWATCH,FLUSHDB,ECHO,SCRIPT,SPOP,GETRANGE,JSON.DEL,SSCAN,JSON.ARRPOP,SINTER,JSON.DEBUG,DEBUG,HINCRBY,EVAL,XLEN,RPOPLPUSH,ZCARD,SDIFFSTORE,ZREMRANGEBYRANK,JSON.TYPE,JSON.TOGGLE,SORT,MSETNX,XINFO,ZINCRBY,INCRBYFLOAT,JSON.NUMMULTBY,JSON.OBJKEYS,XRANGE,REPLICAOF,DFLY,DECRBY,TTL,SUNIONSTORE,LREM,HVALS,REPLCONF,UNSUBSCRIBE,WATCH,MONITOR,STICK,RENAMENX,JSON.ARRINSERT,EVALSHA,TIME,LPOP,DEL,HLEN,HGET,MGET,LINDEX,BRPOPLPUSH,CLIENT,CONFIG,LASTSAVE,DISCARD,ZCOUNT,RPUSHX,SMISMEMBER,FLUSHALL,INCRBY,SINTERSTORE,FUNCTION,CL.THROTTLE,PUBSUB,HKEYS,HRANDFIELD,SREM,GETDEL,MOVE,ZRANGE,BRPOP,LTRIM,SETRANGE,LPUSHX,ZRANGEBYSCORE,RESTORE,HEXISTS,SUBSCRIBE,ZREMRANGEBYLEX,ZRANK,XREVRANGE,AUTH,MSET,HGETALL,PEXPIRE,ZRANGEBYLEX,EXPIRE,UNLINK,ZINTERSTORE,TOUCH,SMOVE,HSCAN,ZREVRANGEBYLEX,BITFIELD_RO,EXPIREAT,ZPOPMIN,SAVE,ZREVRANGE,QUIT,JSON.ARRTRIM,JSON.ARRAPPEND,SDIFF,GETBIT,SHUTDOWN,BITPOS,PSETEX,PSUBSCRIBE,ZREVRANK,ZSCORE,DBSIZE,SLAVEOF,ZREMRANGEBYSCORE,ZREM,MEMORY,JSON.ARRLEN,PTTL,HSTRLEN,SELECT,ZPOPMAX,ZREVRANGEBYSCORE,INCR,PEXPIREAT,JSON.GET,SUBSTR,SADDEX,JSON.RESP,JSON.MGET,RENAME,PING,SETEX,GET,LPOS,ZLEXCOUNT,COMMAND,ZSCAN,LMOVE,GETSET,BLPOP,DUMP,RPUSH,HINCRBYFLOAT,ZMSCORE,ZUNION,JSON.STRLEN,STRLEN,LSET,JSON.NUMINCRBY,JSON.FORGET,JSON.SET,ROLE,SCAN,SISMEMBER,BGSAVE,LRANGE,BITFIELD,HELLO,BITCOUNT,SUNION,APPEND,XADD,PREPEND".split(
    ","
  );

const DOCS_COMMANDS_PATH = path.join(__dirname, "../docs/command-reference");

const commandConfigGroupToCommandDir = {
  json: "json",
  string: "strings",
  connection: "server-management",
  server: "server-management",
  bitmap: "strings",
  list: "lists",
  generic: "generic",
  transactions: "generic",
  scripting: "generic",
  hash: "hashes",
  pubsub: "pubsub",
  set: "sets",
  stream: "pubsub",
  "sorted-set": "sorted-sets",
} as const;

const fetchRepoZip = async (repoZipUrl: string) => {
  const zipResponse = await fetch(repoZipUrl);
  const zipArrayBuffer = await zipResponse.arrayBuffer();

  return Buffer.from(zipArrayBuffer);
};

const getZipEntryContent = (entry: AdmZip.IZipEntry) =>
  entry.getData().toString();

const isCommandEntry = (entry: AdmZip.IZipEntry) =>
  !entry.isDirectory &&
  entry.entryName.includes("commands/") &&
  !path.basename(entry.entryName).startsWith("_");

const getCommandsFromZip = (zip: AdmZip) =>
  Object.fromEntries(
    zip
      .getEntries()
      .filter(isCommandEntry)
      .map((entry) => [
        path.basename(entry.entryName),
        getZipEntryContent(entry),
      ])
  );

const getCommandsConfigFromZip = (zip: AdmZip): Record<string, CommandConfig> =>
  JSON.parse(
    getZipEntryContent(
      zip
        .getEntries()
        .find((entry) => entry.entryName.endsWith("commands.json"))
    )
  );

const specialSyntaxes = {
  return: "## Return",
  examples: "## Examples",
  "nil-reply": "[Null reply](/docs/reference/protocol-spec#resp-bulk-strings)",
  "simple-string-reply":
    "[Simple string reply](/docs/reference/protocol-spec#resp-simple-strings)",
  "integer-reply":
    "[Integer reply](/docs/reference/protocol-spec#resp-integers)",
  "bulk-string-reply":
    "[Bulk string reply](/docs/reference/protocol-spec#resp-bulk-strings)",
  "array-reply": "[Array reply](/docs/reference/protocol-spec#resp-arrays)",
  "error-reply": "[Error reply](/docs/reference/protocol-spec#resp-errors)",
};

const processMdSpecialSyntax = (mdContent: string) =>
  mdContent
    .replace(
      new RegExp(`@(${Object.keys(specialSyntaxes).join("|")})`, "g"),
      (match, key) => specialSyntaxes[key] || match
    )
    .replace(/{{< highlight (.+?) >}}/g, "``` $1")
    .replace(/{{< \/ highlight >}}/g, "```")
    .replace(/{{% alert title="(.+?)" color="warning" %}}/g, ":::note $1\n")
    .replace(/{{% \/alert %}}/g, "\n:::");

const processMdLinks = (mdContent: string) => {
  return mdContent
    .replace(/(\s|\()\/commands\/([a-z-_]+)/g, "$1./$2.md")
    .replace(
      /(\s|\()(\/(?:docs|topics)(?:[a-z-_/]+))/g,
      "$1https://redis.io$2"
    );
};

const buildFrontMatter = (commandConfig: CommandConfig) => {
  return yaml.stringify({ description: commandConfig.summary }).trim();
};

type Argument = (
  | { type: "oneof" | "block"; arguments: Argument[] }
  | {
      type:
        | "integer"
        | "string"
        | "key"
        | "pattern"
        | "double"
        | "unix-time"
        | "pure-token";
    }
) & {
  optional?: boolean;
  multiple?: boolean;
  multiple_token?: boolean;
  token?: string;
  name: string;
  display_text?: string;
};

type CommandConfig = {
  summary: string;
  complexity: string;
  group: keyof typeof commandConfigGroupToCommandDir;
  arguments?: Argument[];
};

const stringifyCommandArgument = (arg: Argument) => {
  const prependToken = (str: string) =>
    `${arg.token == null ? "" : arg.token || '""'}\xa0${str}`.trim();
  const wrapOptional = (str: string) => (arg.optional ? `[${str}]` : str);
  const wrapMultiple = (str: string) =>
    arg.multiple ? `${str} [${str} ...]` : str;
  const wrapOneOf = (str: string) =>
    arg.type === "oneof" && (!arg.optional || arg.token != null)
      ? `<${str}>`
      : str;
  const wrap = (str: string) =>
    wrapOptional(
      arg.multiple_token
        ? wrapOneOf(wrapMultiple(prependToken(str)))
        : prependToken(wrapOneOf(wrapMultiple(str)))
    );

  if (arg.type === "oneof") {
    return wrap(arg.arguments.map(stringifyCommandArgument).join(" | "));
  }

  if (arg.type === "block") {
    return wrap(arg.arguments.map(stringifyCommandArgument).join(" "));
  }

  if (arg.type === "pure-token") {
    return wrap("");
  }

  return wrap(`${arg.display_text || arg.name}`);
};

const generateCommandMdDoc = (
  commandName: string,
  commandConfig: CommandConfig,
  commandMdContents: string
) => {
  const frontMatter = buildFrontMatter(commandConfig);
  const stringifiedArguments =
    commandConfig.arguments?.map(stringifyCommandArgument).join(" ") || "";
  const processedCommandMdContents = processMdLinks(
    processMdSpecialSyntax(commandMdContents)
  );

  return [
    "---",
    frontMatter,
    "---",
    "",
    `# ${commandName}`,
    "",
    "## Syntax",
    "",
    `    ${commandName} ${stringifiedArguments}`,
    "",
    `**Time complexity:** ${commandConfig.complexity}`,
    "",
    processedCommandMdContents,
  ].join("\n");
};

const main = async () => {
  console.log("Fetching Repo ZIPs...");

  const zipBuffers = await Promise.all([
    fetchRepoZip(
      "https://github.com/RedisJSON/RedisJSON/archive/refs/heads/master.zip"
    ),
    fetchRepoZip(
      "https://github.com/redis/redis-doc/archive/refs/heads/master.zip"
    ),
  ]);

  console.log("Loading Repo ZIPs...");

  const zips = zipBuffers.map((buffer) => new AdmZip(buffer));

  console.log("Parsing commands.json files...");

  const commandsConfig = zips.reduce(
    (config, zip) => ({ ...config, ...getCommandsConfigFromZip(zip) }),
    {} as Record<string, CommandConfig>
  );

  console.log("Parsing commands markdown files...");

  const commands = zips.reduce(
    (obj, zip) => ({ ...obj, ...getCommandsFromZip(zip) }),
    {}
  );

  for (let [commandName, commandConfig] of Object.entries(commandsConfig)) {
    console.group("Processing command", commandName, "...");

    if (DRAGONFLY_SUPPORTED_COMMANDS.includes(commandName)) {
      const commandFileName = commandName.toLowerCase().split(" ").join("-");
      const commandFilePath = `${commandFileName}.md`;
      const commandFileAbsolutePath = path.join(
        DOCS_COMMANDS_PATH,
        commandConfigGroupToCommandDir[commandConfig.group],
        commandFilePath
      );
      const commandMdContents = commands[commandFilePath];

      console.log("Generating doc file");

      const commandMdDoc = generateCommandMdDoc(
        commandName,
        commandConfig,
        commandMdContents
      );

      console.log(
        "Writing doc file into",
        path.relative(process.cwd(), commandFileAbsolutePath)
      );

      fs.writeFileSync(commandFileAbsolutePath, commandMdDoc);
    } else {
      console.log("Command not supported by Dragonfly. Skipping.");
    }

    console.groupEnd();
  }
};

main();
