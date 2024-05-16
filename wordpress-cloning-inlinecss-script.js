const juice = require('juice');
const fs = require('fs').promises;  // Using the promise-based version of fs

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

// Function to inline CSS and write file
const inlineCssAndWriteFile = async (htmlFile) => {
  try {
    const inlinedHtml = await new Promise((resolve, reject) => {
      juice.juiceFile(htmlFile, {}, (err, result) => {
        if (err) {
          reject(`Error inlining CSS for file ${htmlFile}: ${err}`);
        } else {
          resolve(result);
        }
      });
    });

    await fs.writeFile(htmlFile, inlinedHtml, 'utf8');
    console.log(`CSS inlined successfully for file ${htmlFile}`);
  } catch (error) {
    console.error(error);
  }
};

// Process each file in series
const processFiles = async () => {
  for (const htmlFile of htmlFiles) {
    await inlineCssAndWriteFile(htmlFile);
  }
};

// Start the process
processFiles();