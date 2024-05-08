module.exports = function(grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        
        // Configuration for inline-css
        inlinecss: {
            main: {
                options: {
                },
                files: {
                    'dist/index-index.html': 'dist/index.html'
                }
            }
        }
    });

    // Load the plugin
    grunt.loadNpmTasks('grunt-inline-css');

    // Default task(s).
    grunt.registerTask('default', ['inlinecss']);
};