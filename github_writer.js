github_writer.js import fs from "fs";

class GitHubWriter {
  constructor() {
    this.stepSummaryPath = process.env.GITHUB_STEP_SUMMARY;
    this.outputPath = process.env.GITHUB_OUTPUT;
  }

  async writeSummary(content) {
    if (this.stepSummaryPath) {
      await fs.promises.appendFile(this.stepSummaryPath, content);
    } else {
      console.log(content);
    }
  }

  async writeOutput(key, value) {
    if (this.outputPath) {
      await fs.promises.appendFile(this.outputPath, `${key}=${value}\n`);
    } else {
      console.log("GITHUB_OUTPUT not found. Printing to console:");
      console.log(`${key}=${value}`);
    }
  }
}

export default GitHubWriter;
