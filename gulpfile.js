import gulp from 'gulp';
import rev from 'gulp-rev';
import revReplace from 'gulp-rev-replace';
import path from 'path';
import postcss from 'gulp-postcss';
import postcssUrl from 'postcss-url';

const paths = {
  src: 'dist',
  css: 'dist/*.css',
  js: 'dist/*.js',
  images: 'dist/assets/*.{png,jpg,jpeg,gif,svg}',
  html: 'dist/*.html'
};

// Task to process CSS and update URLs for images within CSS
gulp.task('process-css', () => {
  return gulp.src(paths.css)
    .pipe(postcss([
      postcssUrl({
        url: 'rebase'
      })
    ]))
    .pipe(gulp.dest(paths.src));
});

// Task to copy and fingerprint assets
gulp.task('rev-assets', () => {
  return gulp.src([paths.css, paths.js, paths.images], { base: paths.src, encoding: false})
    .pipe(rev())
    .pipe(gulp.dest(paths.src))
    .pipe(rev.manifest())
    .pipe(gulp.dest(paths.src));
});

// Task to replace asset links in HTML files
gulp.task('revreplace-html', () => {
  const manifest = gulp.src(path.join(paths.src, 'rev-manifest.json'));

  return gulp.src(paths.html)
    .pipe(revReplace({ manifest: manifest }))
    .pipe(gulp.dest(paths.src));
});

// Task to replace asset links in CSS files
gulp.task('revreplace-css', () => {
  const manifest = gulp.src(path.join(paths.src, 'rev-manifest.json'));

  return gulp.src(path.join(paths.src, '*.css'))
    .pipe(revReplace({ manifest: manifest }))
    .pipe(gulp.dest(paths.src));
});

// Default task to run all tasks in sequence
gulp.task('default', gulp.series('process-css', 'rev-assets', 'revreplace-html', 'revreplace-css'));
