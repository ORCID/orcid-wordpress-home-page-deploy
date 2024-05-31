const fs = require("fs");
const { PurgeCSS } = require("purgecss");
const GitHubWriter = require("./github_writer");

const gitHubWriter = new GitHubWriter();

// Function to count the number of lines in a file
const countLines = (filePath) => {
  const fileContent = fs.readFileSync(filePath, "utf-8");
  return fileContent.split("\n").length;
};

const cssFilePath = "dist/wordpress-homepage.css";
const outputFilePath = "dist/wordpress-homepage.css";

(async () => {
  try {
    // Initial number of lines
    const initialLines = countLines(cssFilePath);

    // Purge CSS
    const purgeCss = new PurgeCSS();

    const purgecssResult = await purgeCss.purge({
      content: ["dist/index.html"],
      css: [cssFilePath],
      output: outputFilePath,
      safelist: {
        // standard: [/^is-/],
        deep: [
          /:where\(([^)]+)\)/, // This will match `:where` with any content inside the parentheses
        ],
      },
    });

    // Write the purged CSS to the output file
    fs.writeFileSync(outputFilePath, purgecssResult[0].css, {
      encoding: "utf-8",
    });

    // Final number of lines
    const finalLines = countLines(outputFilePath);

    // Create the report
    const report = `- Initial number of lines: ${initialLines}
- Final number of lines: ${finalLines}
`;

    // Write the report to the GitHub Actions job summary
    await gitHubWriter.writeSummary(report);
  } catch (error) {
    gitHubWriter.writeSummary(`- ${error}\n`);
    gitHubWriter.writeOutput("script-success", "false");
    sys.exit(1);
  }
})();
