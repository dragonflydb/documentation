import React from "react";
import clsx from "clsx";

import styles from "./styles.module.css";

interface BenchmarkProps {
  /** Command name shown in the intro sentence, e.g. "GET". */
  command: string;
  dragonflyOps: number;
  redisOps: number;
  valkeyOps: number;
  /** Server + client instance types, e.g. "Server: m7g.8xlarge (arm64) · Client: c6gn.8xlarge (arm64)". */
  hardware: string;
  /** Load-generation tool and concurrency settings. */
  client: string;
  /** Keyspace / value size used for the run. */
  dataset: string;
  /** Test duration, warmup, and trial count. */
  duration: string;
  /** ISO date the numbers were captured. */
  measuredOn: string;
  /** Path to the reproduce doc within github.com/dragonflydb/benchmarking. */
  harnessPath: string;
  /** "memtier_benchmark" or "dfly_bench" — used in the closing methodology sentence. */
  tool: string;
  /** Verbatim rows from the harness's "Expected results" table. */
  results: {
    engine: string;
    throughput: string;
    p50: string;
    p99: string;
    p999: string;
    avgLatency: string;
  }[];
}

function formatOps(n: number): string {
  return n.toLocaleString("en-US");
}

function formatTick(v: number): string {
  if (v === 0) return "0";
  return `${(v / 1_000_000).toFixed(2).replace(/0$/, "")}M`;
}

export default function Benchmark({
  command,
  dragonflyOps,
  redisOps,
  valkeyOps,
  hardware,
  client,
  dataset,
  duration,
  measuredOn,
  harnessPath,
  tool,
  results,
}: BenchmarkProps): JSX.Element {
  const engines = [
    { name: "Dragonfly", ops: dragonflyOps, isWinner: true },
    { name: "Valkey", ops: valkeyOps, isWinner: false },
    { name: "Redis", ops: redisOps, isWinner: false },
  ];

  const max = Math.max(dragonflyOps, redisOps, valkeyOps);
  const scale = Math.ceil(max / 500_000) * 500_000;
  const ticks = [0, 1, 2, 3, 4].map((i) => formatTick((scale * i) / 4));

  const methodology: [string, string][] = [
    ["Hardware", hardware],
    ["Client", client],
    ["Dataset", dataset],
    ["Duration", duration],
    ["Measured", measuredOn],
  ];

  const harnessUrl = `https://github.com/dragonflydb/benchmarking/blob/main/${harnessPath}`;

  return (
    <div className={styles.benchmark}>
      <p>
        Sustained throughput for <code>{command}</code> on a single instance,
        measured against Redis and Valkey on identical hardware. Higher is
        better.
      </p>

      <div className={styles.rows}>
        {engines.map((engine) => {
          const width = ((engine.ops / scale) * 100).toFixed(1) + "%";
          const relative = engine.isWinner
            ? "OPS"
            : (dragonflyOps / engine.ops).toFixed(1) + "× OPS";

          return (
            <div key={engine.name} className={styles.row}>
              <span
                className={clsx(styles.name, {
                  [styles.winnerName]: engine.isWinner,
                })}
              >
                {engine.name}
              </span>
              <span className={styles.track}>
                <span
                  className={clsx(styles.bar, {
                    [styles.winnerBar]: engine.isWinner,
                  })}
                  style={{ width }}
                />
              </span>
              <span className={styles.value}>
                <span
                  className={clsx({ [styles.winnerName]: engine.isWinner })}
                >
                  {formatOps(engine.ops)}
                </span>
                <span className={styles.relative}>{relative}</span>
              </span>
            </div>
          );
        })}
      </div>

      <div className={styles.axis}>
        <span />
        <div>
          <div className={styles.axisTicks}>
            {ticks.map((_, i) => (
              <span key={i} />
            ))}
          </div>
          <div className={styles.axisLabels}>
            {ticks.map((label, i) => (
              <span key={i}>{label}</span>
            ))}
          </div>
          <div className={styles.axisCaption}>operations / second</div>
        </div>
        <span />
      </div>

      <table className={styles.resultsTable}>
        <thead>
          <tr>
            <th>Engine</th>
            <th>Throughput</th>
            <th>p50</th>
            <th>p99</th>
            <th>p99.9</th>
            <th>Avg Latency</th>
          </tr>
        </thead>
        <tbody>
          {results.map((row) => (
            <tr key={row.engine}>
              <td
                className={clsx({
                  [styles.winnerName]: row.engine === "Dragonfly",
                })}
              >
                {row.engine}
              </td>
              <td>{row.throughput}</td>
              <td>{row.p50}</td>
              <td>{row.p99}</td>
              <td>{row.p999}</td>
              <td>{row.avgLatency}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h3>Methodology</h3>
      <table className={styles.methodologyTable}>
        <tbody>
          {methodology.map(([label, value]) => (
            <tr key={label}>
              <td className={styles.methodologyLabel}>{label}</td>
              <td>
                <code>{value}</code>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <p className={styles.footnote}>
        Ran through <code>{tool}</code> until throughput stabilized; the
        reported figure is the median throughput sampled during the run.
        Harness and raw output: <a href={harnessUrl}>dragonflydb/benchmarking</a>.
      </p>
    </div>
  );
}
