#!/usr/bin/env ts-node

import path from "path";
import AdmZip from "adm-zip";
import fetch from "cross-fetch";
import fs from "fs";
import yaml from "yaml";

const REPO_ZIP_URL =
  "https://github.com/redis/redis-doc/archive/refs/heads/master.zip";
const ZIP_ROOT_DIR = "redis-doc-master";
const REPO_COMMANDS_DIR_PATH = `${ZIP_ROOT_DIR}/commands/`;
const REPO_COMMANDS_JSON_PATH = `${ZIP_ROOT_DIR}/commands.json`;

const DOCS_COMMANDS_PATH = path.join(__dirname, "../docs/command-reference");

const fetchRepoZip = async () => {
  const zipResponse = await fetch(REPO_ZIP_URL);
  const zipArrayBuffer = await zipResponse.arrayBuffer();

  return Buffer.from(zipArrayBuffer);
};

const getZipEntryContent = (entry: AdmZip.IZipEntry) =>
  entry.getData().toString();

const isCommandEntry = (entry: AdmZip.IZipEntry) =>
  !entry.isDirectory &&
  entry.entryName.startsWith(REPO_COMMANDS_DIR_PATH) &&
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
  JSON.parse(getZipEntryContent(zip.getEntry(REPO_COMMANDS_JSON_PATH)));

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
  mdContent.replace(
    new RegExp(`@(${Object.keys(specialSyntaxes).join("|")})`, "g"),
    (match, key) => specialSyntaxes[key] || match
  );

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
  console.log("Fetching Repo ZIP...");

  const zipBuffer = await fetchRepoZip();

  console.log("Loading Repo ZIP...");

  const zip = new AdmZip(zipBuffer);

  console.log("Parsing commands.json file...");

  const commandsConfig = getCommandsConfigFromZip(zip);

  console.log("Parsing commands markdown files...");

  const commands = getCommandsFromZip(zip);

  for (let [commandName, commandConfig] of Object.entries(commandsConfig)) {
    console.group("Processing command", commandName, "...");

    const commandFileName = commandName.toLowerCase().split(" ").join("-");
    const commandFilePath = `${commandFileName}.md`;
    const commandFileAbsolutePath = path.join(
      DOCS_COMMANDS_PATH,
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

    console.groupEnd();
  }
};

main();
