module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    jshint: {
      gruntfile: {
        src: 'gruntfile.js'
      }
    },
    less: {
      frontend: {
        options: {
          paths: ['volcanicpixels', 'volcanicpixels/frontend', 'bower_components', 'bower_components/*/'],
          sourceMap: true,
          outputSourceFiles: true,
          strictMath: true
        },
        files: {
          "assets/frontend.css": "volcanicpixels/frontend/styles.less"
        }
      }
    },
    copy: {
      fonts: {
        files: [{
          expand: true,
          cwd: "volcanicpixels/frontend/modules/fonts/",
          src: ['**', '!**.less'],
          dest: 'assets/fonts/'
        }]
      }
    },
    shell: {
      pep8: {
        command: 'pep8 volcanicpixels',
        options: {
          stdout: true,
          stderr: true,
          failOnError: true
        }
      }
    },
    watch: {
      gruntfile: {
        files: 'gruntfile.js',
        tasks: ['jshint:gruntfile']
      },
      python: {
        files: 'volcanicpixels/**/*.py',
        tasks: ['pep8']
      },
      less: {
        files: ['volcanicpixels/**/*.less'],
        tasks: ['less']
      },
      fonts: {
        files: ['volcanicpixels/frontend/modules/fonts/**'],
        tasks: ['copy:fonts']
      }
    }
  });

  // Load the plugin that provides the "uglify" task.
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-shell');

  // Default task(s).
  grunt.registerTask('default', ['pep8','jshint', 'less', 'copy']);
  grunt.registerTask('pep8', ['shell:pep8']);
  grunt.registerTask('test', ['pep8']);

};