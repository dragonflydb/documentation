#!/usr/bin/env ts-node
//
// Regenerates the `## Benchmark` section on command-reference pages from
// the latest results published in github.com/dragonflydb/benchmarking.
//
// Usage: yarn sync-benchmarks
// Intended to run on a schedule via .github/workflows/sync-benchmarks.yml,
// which opens a PR only when the generated content actually changes.

import AdmZip from "adm-zip";
import fetch from "cross-fetch";
import fs from "fs";
import path from "path";

const BENCHMARKING_ZIP =
  "https://github.com/dragonflydb/benchmarking/archive/refs/heads/main.zip";
const BENCHMARKING_BLOB_ROOT =
  "https://github.com/dragonflydb/benchmarking/blob/main/";
const DOCS_COMMAND_REFERENCE = path.join(
  __dirname,
  "../docs/command-reference"
);
const GITHUB_API = "https://api.github.com";

const START_MARKER = "<!-- benchmark:start -->";
const END_MARKER = "<!-- benchmark:end -->";

const KEY_DIST_LABELS: Record<string, string> = {
  U: "uniform",
  N: "normal",
  Z: "zipfian",
  S: "sequential",
};

type ResultRow = {
  engine: string;
  throughput: string;
  p50: string;
  p99: string;
  p999: string;
  avgLatency: string;
};

type BenchmarkData = {
  command: string;
  dragonflyOps: number;
  valkeyOps: number;
  redisOps: number;
  hardware: string;
  tool: string;
  client: string;
  dataset: string;
  duration: string;
  measuredOn: string;
  harnessPath: string;
  results: ResultRow[];
};

function githubHeaders(): Record<string, string> {
  const token = process.env.GITHUB_TOKEN;
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function fetchRepoZip(url: string): Promise<AdmZip> {
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`Failed to fetch ${url}: ${res.status} ${res.statusText}`);
  }
  const buffer = Buffer.from(await res.arrayBuffer());
  return new AdmZip(buffer);
}

// Pulls out every `--flag value` (or bare `--flag`) token from a shell-ish
// dfbench invocation, tolerating backslash line continuations.
function parseFlags(block: string): Record<string, string> {
  const flags: Record<string, string> = {};
  const re = /--([a-zA-Z][\w-]*)(?:[ \t]+(?:"([^"]*)"|(\S+)))?/g;
  let match: RegExpExecArray | null;
  while ((match = re.exec(block))) {
    const [, name, quoted, bare] = match;
    const value = quoted ?? bare ?? "";
    // Skip when the "value" is actually the next flag (bare boolean flag).
    flags[name] = value.startsWith("--") ? "" : value;
  }
  return flags;
}

function section(md: string, heading: string): string | null {
  const start = md.indexOf(heading);
  if (start === -1) return null;
  const rest = md.slice(start + heading.length);
  const next = rest.search(/\n#{2,3} /);
  return next === -1 ? rest : rest.slice(0, next);
}

function parseExpectedResults(md: string): ResultRow[] {
  const body = section(md, "Expected results");
  if (!body) throw new Error("No 'Expected results' section found");

  const rows: ResultRow[] = [];
  for (const line of body.split("\n")) {
    if (!line.trim().startsWith("|")) continue;
    const cells = line
      .split("|")
      .map((c) => c.trim().replace(/^\*\*|\*\*$/g, ""))
      .filter((c) => c.length > 0);
    if (cells.length < 6) continue;
    const [engineRaw, throughput, p50, p99, p999, avgLatency] = cells;
    if (/^-+$/.test(throughput)) continue; // markdown table separator row
    const engine = engineRaw.toLowerCase();
    if (!["dragonfly", "redis", "valkey"].includes(engine)) continue;
    rows.push({
      engine: engine[0].toUpperCase() + engine.slice(1),
      throughput,
      p50,
      p99,
      p999,
      avgLatency,
    });
  }
  if (rows.length === 0) throw new Error("Could not parse any result rows");
  return rows;
}

function opsFromThroughput(throughput: string): number {
  const m = /^([\d.]+)\s*([MK]?)/.exec(throughput);
  if (!m) throw new Error(`Unrecognized throughput value: ${throughput}`);
  const [, num, unit] = m;
  const multiplier = unit === "M" ? 1_000_000 : unit === "K" ? 1_000 : 1;
  return Math.round(parseFloat(num) * multiplier);
}

function buildDataset(
  tool: "dfly_bench" | "memtier",
  flags: Record<string, string>,
  usesValuePayload: boolean
): string {
  const parts: string[] = [];
  const keyMax = flags["command-key-maximum"] ?? flags["key-maximum"];
  const preloadItems = Number(flags["preload-items"] ?? 0);

  if (keyMax) {
    const count = formatCount(keyMax);
    parts.push(
      preloadItems > 1 ? `${count} keys, ${preloadItems} preloaded items each` : `${count} keys`
    );
  }

  const dataSize = flags["dfly-bench-data-size"] ?? flags["memtier-data-size"];
  if (usesValuePayload && dataSize) {
    parts.push(`${dataSize}B values`);
  }

  if (tool === "dfly_bench") {
    const distLabel = KEY_DIST_LABELS[flags["dfly-bench-key-dist"]];
    if (distLabel) parts.push(`${distLabel} key distribution`);
  }

  return parts.join(", ");
}

function formatCount(raw: string): string {
  const n = Number(raw);
  if (!Number.isFinite(n)) return raw;
  if (n >= 1_000_000 && n % 1_000_000 === 0) return `${n / 1_000_000}M`;
  if (n >= 1_000 && n % 1_000 === 0) return `${n / 1_000}K`;
  return String(n);
}

function usesValue(flags: Record<string, string>): boolean {
  if (flags["command"]) return true; // builtin GET/SET always read or write a value
  const template = flags["command-template"] ?? "";
  const preload = flags["preload-template"] ?? "";
  return template.includes("__data__") || preload.includes("__data__");
}

async function fetchMeasuredOn(harnessPath: string): Promise<string> {
  const url = `${GITHUB_API}/repos/dragonflydb/benchmarking/commits?path=${encodeURIComponent(
    harnessPath
  )}&per_page=1`;
  const res = await fetch(url, { headers: githubHeaders() });
  if (!res.ok) {
    console.warn(`  Could not fetch commit date for ${harnessPath} (${res.status}); using today.`);
    return new Date().toISOString().slice(0, 10);
  }
  const commits = await res.json();
  const date = commits?.[0]?.commit?.author?.date;
  return date ? date.slice(0, 10) : new Date().toISOString().slice(0, 10);
}

async function parseCommand(
  command: string,
  tool: "dfly_bench" | "memtier",
  harnessPath: string,
  md: string
): Promise<BenchmarkData> {
  const setup = section(md, "Stateful setup:") ?? "";
  const testRun = section(md, "Test run:") ?? "";
  const setupFlags = parseFlags(setup);
  const runFlags = parseFlags(testRun);

  const hardware = `Server: ${setupFlags["server-instance"]} (${setupFlags["server-arch"]}) · Client: ${setupFlags["client-instance"]} (${setupFlags["client-arch"]})`;

  const client =
    tool === "dfly_bench"
      ? `${runFlags["dfly-bench-threads"]} threads, ${runFlags["dfly-bench-conns"]} connections, pipeline ${runFlags["dfly-bench-pipeline"]}`
      : `${runFlags["memtier-threads"]} threads, ${runFlags["memtier-clients"]} clients, pipeline ${runFlags["memtier-pipeline"]}`;

  const dataset = buildDataset(tool, runFlags, usesValue(runFlags));

  const testTime = runFlags["test-time"];
  const warmupTime = runFlags["warmup-time"];
  const trials = Number(runFlags["trials"] ?? 1);
  const duration = `${testTime}s (${warmupTime}s warmup), ${trials} trial${trials === 1 ? "" : "s"}`;

  const results = parseExpectedResults(md);
  const opsByEngine = Object.fromEntries(
    results.map((r) => [r.engine, opsFromThroughput(r.throughput)])
  );

  const ordered = ["Dragonfly", "Valkey", "Redis"]
    .map((name) => results.find((r) => r.engine === name))
    .filter((r): r is ResultRow => Boolean(r));

  return {
    command,
    dragonflyOps: opsByEngine["Dragonfly"],
    valkeyOps: opsByEngine["Valkey"],
    redisOps: opsByEngine["Redis"],
    hardware,
    tool,
    client,
    dataset,
    duration,
    measuredOn: await fetchMeasuredOn(harnessPath),
    harnessPath,
    results: ordered,
  };
}

function renderBenchmarkBlock(data: BenchmarkData): string {
  const resultsLines = data.results
    .map(
      (r) =>
        `    { engine: "${r.engine}", throughput: "${r.throughput}", p50: "${r.p50}", p99: "${r.p99}", p999: "${r.p999}", avgLatency: "${r.avgLatency}" },`
    )
    .join("\n");

  return [
    START_MARKER,
    "## Benchmark",
    "",
    "<Benchmark",
    `  command="${data.command}"`,
    `  dragonflyOps={${data.dragonflyOps}}`,
    `  valkeyOps={${data.valkeyOps}}`,
    `  redisOps={${data.redisOps}}`,
    `  hardware="${data.hardware}"`,
    `  tool="${data.tool}"`,
    `  client="${data.client}"`,
    `  dataset="${data.dataset}"`,
    `  duration="${data.duration}"`,
    `  measuredOn="${data.measuredOn}"`,
    `  harnessPath="${data.harnessPath}"`,
    "  results={[",
    resultsLines,
    "  ]}",
    "/>",
    END_MARKER,
  ].join("\n");
}

// Where to insert a Benchmark section on a page that doesn't have one yet.
const INSERT_BEFORE_HEADINGS = [
  "## Best Practices",
  "## Common Mistakes",
  "## FAQs",
  "## See also",
  "## Pattern:",
];

function upsertBenchmarkBlock(fileContents: string, block: string): string {
  const markerRe = new RegExp(
    `${START_MARKER}[\\s\\S]*?${END_MARKER}`,
    "m"
  );
  if (markerRe.test(fileContents)) {
    return fileContents.replace(markerRe, block);
  }

  // Legacy (pre-marker) block: `## Benchmark` heading directly followed by
  // a single self-closing <Benchmark ... /> tag, with no markers.
  const legacyRe = /## Benchmark\n\n<Benchmark[\s\S]*?\n\/>\n?/m;
  if (legacyRe.test(fileContents)) {
    return fileContents.replace(legacyRe, `${block}\n`);
  }

  for (const heading of INSERT_BEFORE_HEADINGS) {
    const idx = fileContents.indexOf(`\n${heading}`);
    if (idx !== -1) {
      return `${fileContents.slice(0, idx)}\n${block}\n${fileContents.slice(idx + 1)}`;
    }
  }

  return `${fileContents.trimEnd()}\n\n${block}\n`;
}

function ensureBenchmarkImport(fileContents: string): string {
  if (fileContents.includes("@site/src/components/Benchmark")) {
    return fileContents;
  }
  const pageTitleImport = "import PageTitle from '@site/src/components/PageTitle';";
  if (fileContents.includes(pageTitleImport)) {
    return fileContents.replace(
      pageTitleImport,
      `${pageTitleImport}\nimport Benchmark from '@site/src/components/Benchmark';`
    );
  }
  // No PageTitle import (unusual, but be defensive): add right after front matter.
  return fileContents.replace(
    /^---\n[\s\S]*?\n---\n/,
    (fm) => `${fm}\nimport Benchmark from '@site/src/components/Benchmark';\n`
  );
}

function findDocFile(command: string): string | null {
  const target = `${command.toLowerCase()}.md`;
  const stack = [DOCS_COMMAND_REFERENCE];
  while (stack.length) {
    const dir = stack.pop()!;
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) stack.push(full);
      else if (entry.name.toLowerCase() === target) return full;
    }
  }
  return null;
}

async function main() {
  console.log("Fetching dragonflydb/benchmarking...");
  const zip = await fetchRepoZip(BENCHMARKING_ZIP);

  const reproduceEntries = zip
    .getEntries()
    .filter((e) => /\/benchmarks\/[^/]+\/(dfly_bench|memtier)\/[^/]+_reproduce\.md$/.test(e.entryName));

  // command -> { dfly_bench?: entry, memtier?: entry }
  const byCommand = new Map<string, Partial<Record<"dfly_bench" | "memtier", AdmZip.IZipEntry>>>();
  for (const entry of reproduceEntries) {
    const m = /\/benchmarks\/([^/]+)\/(dfly_bench|memtier)\//.exec(entry.entryName)!;
    const [, command, tool] = m;
    const existing = byCommand.get(command) ?? {};
    existing[tool as "dfly_bench" | "memtier"] = entry;
    byCommand.set(command, existing);
  }

  console.log(`Found ${byCommand.size} command(s) in benchmarking repo.`);

  let changed = 0;
  let skippedNoDoc = 0;
  let failed = 0;

  for (const [command, tools] of byCommand) {
    // Prefer dfly_bench for consistent methodology across all commands.
    const tool = tools.dfly_bench ? "dfly_bench" : "memtier";
    const entry = tools[tool]!;

    const docFile = findDocFile(command);
    if (!docFile) {
      console.log(`- ${command}: no matching docs/command-reference page, skipping.`);
      skippedNoDoc++;
      continue;
    }

    const zipInternalPath = entry.entryName.replace(/^[^/]+\//, ""); // strip "<repo>-<branch>/" prefix
    const harnessPath = zipInternalPath;

    try {
      const md = entry.getData().toString();
      const data = await parseCommand(command, tool, harnessPath, md);
      const block = renderBenchmarkBlock(data);

      const before = fs.readFileSync(docFile, "utf8");
      const after = ensureBenchmarkImport(upsertBenchmarkBlock(before, block));

      if (after !== before) {
        fs.writeFileSync(docFile, after);
        console.log(`- ${command}: updated ${path.relative(process.cwd(), docFile)}`);
        changed++;
      } else {
        console.log(`- ${command}: up to date.`);
      }
    } catch (err) {
      console.error(`- ${command}: FAILED to sync (${(err as Error).message})`);
      failed++;
    }
  }

  console.log(
    `\nDone. ${changed} file(s) changed, ${skippedNoDoc} command(s) skipped (no doc page), ${failed} failure(s).`
  );

  if (failed > 0) process.exitCode = 1;
}

main();
