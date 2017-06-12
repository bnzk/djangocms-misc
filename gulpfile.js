var gulp = require('gulp'),
    sass = require('gulp-sass'),
    jshint= require('gulp-jshint'),
    path = require('path'),
    dummy = 'last';


// fix Promise() error from which package again?
require('es6-promise').polyfill();


gulp.task('sass', function () {
    return gulp.src('djangocms_misc/admin_style/static/djangocms_misc/admin/sass/*.sass')
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest('djangocms_misc/admin_style/static/djangocms_misc/admin/css'));
    return gulp.src('djangocms_misc/static/djangocms_misc/*.sass')
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest('djangocms_misc/static/djangocms_misc/css'));
});


gulp.task('jshint', function () {
    gulp.src(['gulpfile.js', 'djangocms_misc/**.js'])
        .pipe(jshint());
});


gulp.task('default', ['sass', 'jshint']);


gulp.task('watch', function () {
    gulp.watch('djangocms_misc/**/**.sass', ['sass']);
    gulp.watch(['gulpfile.js', 'djangocms_misc/**.js'], ['jshint']);
});

