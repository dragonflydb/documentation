const { readFileSync, writeFileSync, existsSync, readdirSync, statSync } = require('fs');
const { join } = require('path');

// Function to read JSON file
function readJsonFile(filePath) {
  if (existsSync(filePath)) {
    const fileContent = readFileSync(filePath, 'utf-8');
    return JSON.parse(fileContent);
  }
  return [];
}

// Function to recursively search for a file in the given directory
function findFileInDirectory(directory, fileName) {
  const files = readdirSync(directory);
  for (const file of files) {
    const fullPath = join(directory, file);
    const stat = statSync(fullPath);
    if (stat.isDirectory()) {
      const result = findFileInDirectory(fullPath, fileName);
      if (result) {
        return result;
      }
    } else if (stat.isFile() && file === fileName) {
      return fullPath;
    }
  }
  return null;
}

// Function to update content in markdown files
function updateMarkdownContent(directory, slug, newContent) {
  const fileName = `${slug}.md`;
  const filePath = findFileInDirectory(directory, fileName);
  if (filePath) {
    let fileContent = readFileSync(filePath, 'utf-8');
    const pageTitleIndex = fileContent.indexOf('<PageTitle');
    if (pageTitleIndex !== -1) {
      const endIndex = fileContent.indexOf('>', pageTitleIndex) + 1;
      const updatedContent = fileContent.slice(0, endIndex) + '\n\n' + newContent;
      writeFileSync(filePath, updatedContent);
      //console.log(`Updated content for ${slug}`);
    } else {
      console.log(`PageTitle not found in ${filePath}`);
    }
  } else {
    console.log(`File not found: ${fileName}`);
  }
}

// Path to the JSON file
const jsonFilePath = join(process.cwd(), './temp-new-content.json');

// Read the JSON file
const contentUpdates = readJsonFile(jsonFilePath);
// Update the markdown files
const docsDirectory = join(process.cwd(), 'docs/command-reference');
contentUpdates.forEach(({ slug, content }) => {
  updateMarkdownContent(docsDirectory, slug, content);
});
