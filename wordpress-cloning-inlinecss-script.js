const juice = require('juice');
const fs = require('fs').promises;
const GitHubWriter = require('./github_writer');

// List of HTML files to be updated
const htmlFiles = [
  'dist/index.html',
  'dist/index-ar.html',
  'dist/index-cs.html',
  'dist/index-de.html',
  'dist/index-es.html',
  'dist/index-fr.html',
  'dist/index-it.html',
  'dist/index-ja.html',
  'dist/index-ko.html',
  'dist/index-pl.html',
  'dist/index-pt.html',
  'dist/index-ru.html',
  'dist/index-tr.html',
  'dist/index-zh-CN.html',
  'dist/index-zh-TW.html'
];

const writer = new GitHubWriter();

const inlineCssAndWriteFile = async (htmlFile) => {
  try {
    const inlinedHtml = await new Promise((resolve, reject) => {
      juice.juiceFile(htmlFile, {}, (err, result) => {
        if (err) {
          reject(`Skipping inlining CSS for file ${htmlFile}: \n ${err}`);
        } else {
          resolve(result);
        }
      });
    });

    await fs.writeFile(htmlFile, inlinedHtml, 'utf8');
    await writer.writeSummary(`- CSS inlined successfully for file ${htmlFile}\n`);
  } catch (error) {
    await writer.writeSummary(`- ${error}\n`);
    throw error;
  }
};

const processFiles = async () => {
  try {
    for (const htmlFile of htmlFiles) {
      try {
        await inlineCssAndWriteFile(htmlFile);
      } catch (error) {
        continue;
      }
    }
    await writer.writeOutput('script-success', 'true');
  } catch (error) {
    await writer.writeOutput('script-success', 'false');
    process.exit(1);
  }
};

// Start the process
processFiles();