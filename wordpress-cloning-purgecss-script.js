const fs = require('fs');
const { PurgeCSS } = require("purgecss");
const GitHubWriter = require('./github_writer');

const gitHubWriter = new GitHubWriter();

// Function to count the number of lines in a file
const countLines = (filePath) => {
  const fileContent = fs.readFileSync(filePath, 'utf-8');
  return fileContent.split('\n').length;
};

const cssFilePath = 'dist/combined_styles.css';
const outputFilePath = 'dist/combined_styles.css';

(async () => {
  try {
    // Initial number of lines
    const initialLines = countLines(cssFilePath);

    // Purge CSS
    const purgeCss = new PurgeCSS()

    const purgecssResult = await purgeCss.purge()

    // Write the purged CSS to the output file
    fs.writeFileSync(outputFilePath, purgecssResult[0].css, 'utf-8');

    // Final number of lines
    const finalLines = countLines(outputFilePath);

    // Create the report
    const report = 
`- Initial number of lines: ${initialLines}
- Final number of lines: ${finalLines}
`;

    // Write the report to the GitHub Actions job summary
    await gitHubWriter.writeSummary(report);
  } catch (error) {
    gitHubWriter.writeSummary(`- ${error}\n`);  
    gitHubWriter.writeOutput('script-success', 'false');
    sys.exit(1)
  }
})();