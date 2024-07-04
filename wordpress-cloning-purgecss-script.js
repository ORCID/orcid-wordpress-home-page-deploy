import fs from "fs";
import { PurgeCSS } from "purgecss";
import GitHubWriter from "./github_writer.js";

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
      safelist: [
          /:is/, // https://github.com/FullHuman/purgecss/issues/978
          /:where/, // https://github.com/FullHuman/purgecss/issues/978
          /:not/, // https://github.com/FullHuman/purgecss/issues/1197
      ]
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
    await gitHubWriter.writeSummary(`- ${error}\n`);
    await gitHubWriter.writeOutput("script-success", "false");
    sys.exit(1);
  }
})();
