const fs = require('fs').promises;

class GitHubWriter {
  constructor() {
    this.stepSummaryPath = process.env.GITHUB_STEP_SUMMARY;
    this.outputPath = process.env.GITHUB_OUTPUT;
  }

  async writeSummary(content) {
    if (this.stepSummaryPath) {
      await fs.appendFile(this.stepSummaryPath, content);
    } else {
      console.log(content);
    }
  }

  async writeOutput(key, value) {
    if (this.outputPath) {
      await fs.appendFile(this.outputPath, `${key}=${value}\n`);
    } else {
      console.log("GITHUB_OUTPUT not found. Printing to console:");
      console.log(`${key}=${value}`);
    }
  }
}

module.exports = GitHubWriter;