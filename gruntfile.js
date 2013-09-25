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
          paths: ['volcanicpixels', 'volcanicpixels/frontend', 'assets'],
          sourceMap: true,
          outputSourceFiles: true,
          strictMath: true,
          compress: true
        },
        files: {
          "assets/frontend.css": "volcanicpixels/frontend/styles.less"
        }
      }
    },
    bower: {
      target: {
        rjsConfig: 'assets/config.js'
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
      },
      js: {
        files: [{
          cwd: "volcanicpixels/frontend/",
          src: ['config.js', 'build.js'],
          dest: 'assets/'
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
    transpile: {
      frontend: {
        type: "amd",
        files: [{
          expand: true,
          cwd: 'volcanicpixels/frontend/',
          src: ['**/*.js', '!config.js', '!build.js'],
          dest: 'assets/'
        }]
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

  grunt.loadNpmTasks('grunt-bower-requirejs');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-es6-module-transpiler');
  grunt.loadNpmTasks('grunt-shell');

  // Default task(s).
  grunt.registerTask('default', ['pep8','jshint', 'less', 'copy', 'transpile']);
  grunt.registerTask('pep8', ['shell:pep8']);
  grunt.registerTask('test', ['pep8']);

};
