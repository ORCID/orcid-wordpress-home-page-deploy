const juice = require('juice');
const fs = require('fs');

// List of HTML files to be updated
const htmlFiles = [
  'dist/index.html',
  // 'dist/index-ar.html',
  // 'dist/index-cs.html',
  // 'dist/index-de.html',
  // 'dist/index-es.html',
  // 'dist/index-fr.html',
  // 'dist/index-it.html',
  // 'dist/index-ja.html',
  // 'dist/index-ko.html',
  // 'dist/index-pl.html',
  // 'dist/index-pt.html',
  // 'dist/index-ru.html',
  // 'dist/index-tr.html',
  // 'dist/index-zh-CN.html',
  // 'dist/index-zh-TW.html'
];

// Inline CSS for each HTML file
htmlFiles.forEach(htmlFile => {

    juice.juiceFile(htmlFile, {}, (err, inlinedHtml) => {
      if (err) {
        console.error(`Error inlining CSS for file ${htmlFile}: ${err}`);
        return;
      }


      fs.writeFile(htmlFile, inlinedHtml, 'utf8', err => {
        if (err) {
          console.error(`Error writing file ${htmlFile}: ${err}`);
          return;
        }
        console.log(`CSS inlined successfully for file ${htmlFile}`);
      });
    });
  
});