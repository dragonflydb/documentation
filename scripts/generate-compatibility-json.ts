import fs from "fs/promises";
import path from "path";
import csv from "csv";

const parseCSV = (content: Buffer) =>
  new Promise<Record<string, string>[]>((resolve) => {
    const parser = csv.parse(content, { columns: true, trim: true });
    const rows = [];

    parser.on("data", (data) => {
      rows.push(data);
    });

    parser.on("end", () => {
      resolve(rows);
    });
  });

const main = async () => {
  const csvFilePath = process.argv[2];

  let fileContents: Buffer;

  try {
    fileContents = await fs.readFile(csvFilePath);
  } catch {
    return console.error(
      "Please provide the CSV file path as an argument to the script"
    );
  }

  const csvRows = await parseCSV(fileContents);

  let family = null;
  const json = csvRows.map((row) => {
    if (row["Command Family"]) family = row["Command Family"];

    return {
      family: family,
      command: row["Command"],
      support: row["Dragonfly Support"],
      notes: row["Comments"] || null,
    };
  });

  await fs.writeFile(
    path.resolve(__dirname, "../src/components/CompatibilityTable/data.json"),
    JSON.stringify(json)
  );
};

main();
