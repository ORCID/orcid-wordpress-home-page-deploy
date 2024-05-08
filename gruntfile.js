module.exports = function(grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        
        // Configuration for inline-css
        inlinecss: {
            main: {
                options: {
                },
                files: {
                    'dist/index.html': 'dist/index.html',
                //     "dis/index-ar.html": "dist/index-ar.html",
                //     "dist/index-cs.html": "dist/index-cs.html",
                //     "dist/index-de.html": "dist/index-de.html",
                //     "dist/index-es.html": "dist/index-es.html",
                //     "dist/index-fr.html": "dist/index-fr.html",
                //     "dist/index-it.html": "dist/index-it.html",
                //     "dist/index-ja.html": "dist/index-ja.html",
                //     "dis/index-ko.html": "dist/index-ko.html",
                //     "dist/index-pl.html": "dist/index-pl.html",
                //     "dist/index-pt.html": "dist/index-pt.html",
                //     "dist/index-ru.html": "dist/index-ru.html",
                //     "dist/index-tr.html": "dist/index-tr.html",
                //     "dist/index-zh-CN.html": "dist/index-zh-CN.html",
                //     "dist/index-zh-TW.html": "dist/index-zh-TW.html",
                }
            }
        }
    });

    // Load the plugin
    grunt.loadNpmTasks('grunt-inline-css');

    // Default task(s).
    grunt.registerTask('default', ['inlinecss']);
};