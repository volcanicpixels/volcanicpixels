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
          src: 'volcanicpixels/frontend/config.js',
          dest: 'assets/config.js'
        }]
      }
    },
    requirejs: {
      frontend: {
        options: {
          baseUrl: "assets/",
          mainConfigFile: "assets/config.js",
          out: "assets/frontend.js",
          keepBuildDir: true,
          optimize: 'uglify2',
          generateSourceMaps: true,
          preserveLicenseComments: false,
          name: 'config',
          include: [ 'requirejs']
        }
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
      },
      js: {
        files: ['volcanicpixels/frontend/**/*.js', '!volcanicpixels/frontend/config.js'],
        tasks: ['js']
      },
      jsconfig: {
        files: ['volcanicpixels/frontend/config.js'],
        tasks: ['copy:js', 'bower', 'requirejs']
      },
      bowerjs: {
        files: ['assets/components/**.js', 'bower.json'],
        tasks: ['bower', 'requirejs']
      }
    },
    gae: {
      staging: {
        action: 'update',
        options: {
          application: "volcanicpixels-staging",
          version: "live"
        }
      },
      beta: {
        action: 'update',
        options: {
          application: "volcanic-pixels",
          version: "beta"
        }
      },
      live: {
        action: 'update',
        options: {
          application: "volcanic-pixels",
          version: "live"
        }
      }
    },
  });

  grunt.loadNpmTasks('grunt-bower-requirejs');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-requirejs');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-es6-module-transpiler');
  grunt.loadNpmTasks('grunt-shell');
  grunt.loadNpmTasks('grunt-gae');

  // Default task(s).
  grunt.registerTask('default', ['pep8','jshint', 'less', 'copy', 'transpile', 'bower', 'requirejs']);
  grunt.registerTask('pep8', ['shell:pep8']);
  grunt.registerTask('test', ['jshint', 'pep8']);
  grunt.registerTask('js', ['transpile', 'requirejs']);
  grunt.registerTask('staging', ['gae:staging']);
  grunt.registerTask('beta', ['gae:beta']);
  grunt.registerTask('production', ['gae:live']);

};
