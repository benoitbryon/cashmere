module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    copy: {
      img: {
        files: [
          {
            expand: true,
            cwd: 'assets/img/',
            src: '**',
            dest: 'public/img'
          }
        ]
      },
      glyphicons: {
        files: [
          {
            expand: true,
            cwd: 'bower_components/bootstrap/dist/fonts/',
            src: '**',
            dest: 'public/fonts'
          }
        ]
      }
    },
    less: {
      dev: {
        files: {
          "public/css/cashmere.css": "assets/css/cashmere.less"
        }
      }
    },
    uglify: {
      options: {
        mangle: false
      },
      dev: {
        files: {
          'public/js/libs.min.js': [
            'bower_components/jquery/dist/jquery.js',
            'bower_components/bootstrap/dist/js/bootstrap.js'
          ],
          'public/js/cashmere.min.js': [
            'assets/js/cashmere.js'
          ]
        }
      }
    },
    watch: {
      css: {
        files: ['assets/css/*.less'],
        tasks: ['less'],
        options: {
          nospawn: true
        }
      },
      img: {
        files: ['assets/img/**'],
        tasks: ['copy:img']
      },
      js: {
        files: ['assets/js/**.js', 'bower_components/**.js'],
        tasks: ['uglify']
      }
    }
  });

  // Task loading.
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-watch');

  // Default task(s).
  grunt.registerTask('default', ['watch']);

};
