const gulp = require('gulp');
const pump = require('pump');
const rename = require('gulp-rename');
const concat = require('gulp-concat');
const header = require('gulp-header');
// javascript
const babel = require('gulp-babel');
const uglify = require('gulp-uglify');
// sass
const sass = require('gulp-sass')(require('sass'));
// package.json
const version = require('./package.json').version;

const JS_WIDGET_INPUT = './src/ImageUploaderWidget.js';
const JS_WIDGET_NAME = 'image-uploader.js';
const JS_WIDGET_NAME_MIN = 'image-uploader.min.js';
const JS_OUTPUT = './image_uploader_widget/static/admin/js';
const SCSS_NAME = 'image-uploader.css';
const SCSS_NAME_MIN = 'image-uploader.min.css';
const SCSS_INPUT = './src/ImageUploaderWidget.scss';
const SCSS_OUTPUT = './image_uploader_widget/static/admin/css';
const HEADER = [
    '/**',
    ' * Django Image Uploader Widget - An image uploader widget for django.',
    ' * @version v' + version + '',
    ' * @author Eduardo Oliveira (EduardoJM) <eduardo_y05@outlook.com>.',
    ' * @link https://github.com/inventare/django-image-uploader-widget',
    ' * ',
    ' * Licensed under the MIT License (https://github.com/inventare/django-image-uploader-widget/blob/main/LICENSE).',
    ' */',
    '\n'
].join('\n');

function onError(err) {
    console.log(err);
    this.emit('end');
}

gulp.task('js', (callback) => {
    pump([
        gulp.src(JS_WIDGET_INPUT),
        concat(JS_WIDGET_NAME),
        babel({
            presets: ['@babel/env'],
            plugins: [
                'babel-plugin-remove-import-export',
                '@babel/plugin-proposal-class-properties',
            ]
        }),
        header(HEADER),
        gulp.dest(JS_OUTPUT),
        uglify().on('error', onError),
        rename(JS_WIDGET_NAME_MIN),
        header(HEADER),
        gulp.dest(JS_OUTPUT),
    ], callback);
});

gulp.task('scss-expanded', (callback) => {
    pump([
        gulp.src(SCSS_INPUT),
        sass({
            outputStyle: 'expanded'
        }).on('error', sass.logError),
        header(HEADER),
        rename(SCSS_NAME),
        gulp.dest(SCSS_OUTPUT),
    ], callback);
});

gulp.task('scss-compressed', (callback) => {
    pump([
        gulp.src(SCSS_INPUT),
        sass({
            outputStyle: 'compressed',
        }).on('error', sass.logError),
        header(HEADER),
        rename(SCSS_NAME_MIN),
        gulp.dest(SCSS_OUTPUT),
    ], callback);
});

gulp.task('scss', gulp.series([
    'scss-expanded',
    'scss-compressed'
]));
