const gulp         = require('gulp'),
      sass         = require('gulp-sass'),
      sourcemaps   = require('gulp-sourcemaps'),
      autoprefixer = require('autoprefixer'),
      rigger       = require('gulp-rigger'),
      cssnano      = require('cssnano'),
      imagemin     = require('gulp-imagemin'),
      clean        = require('gulp-clean'),
      pngquant     = require('imagemin-pngquant'),
      uglify       = require('gulp-uglify'),
      postcss      = require('gulp-postcss'),
      pxtorem      = require('postcss-pxtorem'),
      mqpacker     = require('css-mqpacker'),
      babel        = require('gulp-babel'),
      plumber      = require('gulp-plumber'),
      svgSprite    = require('gulp-svg-sprite');
      browserSync  = require('browser-sync').create();
      debug        = require('gulp-debug');
      concat       = require('gulp-concat');
      rename       = require("gulp-rename");

const SYNC_SERVER = 'http://localhost:8000';
const SYNC_BROWSER = 'google-chrome'
const SYNC_START_PAGE = SYNC_SERVER + '/messager/chat_open/2/'

const DIR_BUILD_STATIC = 'static'
const DIR_SATIC_APP = '/.'
const DIR_MAIN_APP = 'main'
const DIR_PREFIX_SATIC_APP = 'res_'

const JS_INIT_FOOTER = `./${DIR_MAIN_APP}/${DIR_PREFIX_SATIC_APP}js/footer/init.js`
const JS_AFTER_INIT_FOOTER = `./${DIR_MAIN_APP}/${DIR_PREFIX_SATIC_APP}js/footer/after_init/*.js`
const JS_INIT_HEADER = `./${DIR_MAIN_APP}/${DIR_PREFIX_SATIC_APP}js/header/init.js`

const template = {
    build: { //where
        js: `./${DIR_BUILD_STATIC}/js/`,
        css: `./${DIR_BUILD_STATIC}/css/`,
        img: `./${DIR_BUILD_STATIC}/img/`,
        fonts: `./${DIR_BUILD_STATIC}/fonts/`,
        svg: `./${DIR_BUILD_STATIC}/svg/`,
    },
    src: { //from where
        //Синтаксис original/**/*.* означает - взять все файлы всех расширений из папки и из вложенных каталогов
        app_css_scss: [
            `./**/${DIR_SATIC_APP}/${DIR_PREFIX_SATIC_APP}scss/*.css`,
            `./**/${DIR_SATIC_APP}/${DIR_PREFIX_SATIC_APP}scss/*.scss`
        ],
        app_js: {
            header: [
                `./**/${DIR_SATIC_APP}/${DIR_PREFIX_SATIC_APP}js/header/*.js`, 
                `!` + JS_INIT_HEADER,
                `!` + JS_AFTER_INIT_FOOTER,
                `!./` + DIR_BUILD_STATIC + `/**`
            ],
            footer: [
                `./**/${DIR_SATIC_APP}/${DIR_PREFIX_SATIC_APP}js/footer/*.js`, 
                `!` + JS_INIT_FOOTER,
                `!./` + DIR_BUILD_STATIC + `/**`
            ]

        },

        modals: `./**/templates/**/modals/*.html`,

        js: [
            `./${DIR_BUILD_STATIC}/js/header_all.js`,
            `./${DIR_BUILD_STATIC}/js/footer_all.js`
        ],
        scss: `./${DIR_BUILD_STATIC}/scss/main.scss`,
        img: `./**/${DIR_SATIC_APP}/${DIR_PREFIX_SATIC_APP}img/**/*.*`, 
        fonts: `./${DIR_MAIN_APP}/${DIR_SATIC_APP}/${DIR_PREFIX_SATIC_APP}fonts/*.*`,
        svg: `./**/${DIR_SATIC_APP}/${DIR_PREFIX_SATIC_APP}svg/*.svg`
    },
    clean: `./${DIR_BUILD_STATIC}`
};

const watch = {
    js:  template.src.app_js,
    scss: template.src.app_css_scss,
    img: template.src.img,
    svg: template.src.svg,
    fonts: template.src.fonts,
};

//#region ====================================js==========================================

function correctRenameHeaderStaticJs(path){

    if (path.dirname == '.'){
        path.dirname = 'header/init/'
        return
    }

    dirname_path = path.dirname.split('/')
    path.dirname = dirname_path[2] + '/' + dirname_path[0] + '/'
}

function correctRenameFooterStaticJs(path){

    if (path.dirname == '.'){
        path.dirname = 'footer/init/'
        return
    }

    dirname_path = path.dirname.split('/')
    path.dirname = dirname_path[2] + '/' + dirname_path[0] + '/'
}

gulp.task('dev-move-header-js', function() {
    
    const params = template.src.app_js.header;
    params.push(JS_INIT_HEADER);

    return gulp.src(params)
     .pipe(rename(correctRenameHeaderStaticJs))
     .pipe(gulp.dest(template.build.js));
  });

  gulp.task('dev-move-footer-js', function() {

    const params = template.src.app_js.footer;
    params.push(JS_INIT_FOOTER);
    params.push(JS_AFTER_INIT_FOOTER);

    return gulp.src(params)
        .pipe(rename(correctRenameFooterStaticJs))
        .pipe(gulp.dest(template.build.js));
    });


gulp.task('dev-concat-header-js', function() {
    
    const params = template.src.app_js.header;
    params.push(JS_INIT_HEADER);

    return gulp.src(params)
     .pipe(concat('header_all.js')) 
     .pipe(gulp.dest(template.build.js));
  });

gulp.task('dev-concat-footer-js', function() {

    const params = template.src.app_js.footer;
    params.push(JS_INIT_FOOTER);
    params.push(JS_AFTER_INIT_FOOTER);

    return gulp.src(params)
        .pipe(concat('footer_all.js')) 
        .pipe(gulp.dest(template.build.js));
    });

gulp.task('prod-base-scripts', function (type) {
    return gulp.src(template.src.js)
        .pipe(plumber())
        .pipe(rigger())
        .pipe(babel({
            presets: [
                ['@babel/env', {
                    modules: false
                }]
            ]
        }))
        .pipe(uglify())
        .pipe(gulp.dest(template.build.js))
        .pipe(browserSync.reload({
            stream: true
        }));
});

gulp.task('dev-base-scripts', function (type) {
    return gulp.src(template.src.js)
        .pipe(plumber())
        .pipe(rigger())
        .pipe(gulp.dest(template.build.js))
        .pipe(browserSync.reload({
            stream: true
        }));
});

gulp.task('prod-scripts', gulp.series(
    'dev-concat-header-js', 
    'dev-concat-footer-js',
    'prod-base-scripts'
));

gulp.task('dev-scripts', gulp.series(
    'dev-concat-header-js', 
    'dev-concat-footer-js',
    'dev-base-scripts'
));

gulp.task('dev-scripts-separation', gulp.series(
    'dev-move-header-js', 
    'dev-move-footer-js'
));


//#endregion =================================End js=================================================

//#region ===================================Css===========================================
gulp.task('dev-css', function() {
    return gulp.src(template.src.app_css_scss)
     .pipe(concat('main.scss')) 
     .pipe(gulp.dest(`./${DIR_BUILD_STATIC}/scss/`));
  });

  gulp.task('dev-base-css', function () {
    return gulp.src(template.src.scss)
        .pipe(plumber())
        .pipe(sourcemaps.init())
        .pipe(sass())
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest(template.build.css))
        .pipe(browserSync.reload({
            stream: true
        }));
});

gulp.task('prod-base-css', function () {

    return gulp.src(template.src.scss)
        .pipe(sass())
        .pipe(postcss([
            pxtorem(),
            autoprefixer({
                overrideBrowserslist: ['last 2 versions'],
                cascade: false,
                grid: true
            }),
            cssnano('main.css')
        ]))
        .pipe(gulp.dest(template.build.css))
});

gulp.task('dev-css', gulp.series( 
    'dev-css',
    'dev-base-css'
));

gulp.task('prod-css', gulp.series( 
    'dev-css',
    'prod-base-css'
));

//#endregion ===============================End css================================================

//#region =================================Image===========================================

function correctRename(path){
    path.dirname = path.dirname.split('/')[0]
}

gulp.task('dev-image', function () {
    return gulp.src(template.src.img)
        .pipe(rename(correctRename))
        .pipe(gulp.dest(template.build.img))
});


gulp.task('prod-image', function () {
    return gulp.src(template.src.img)
        .pipe(imagemin({ //image compression
            progressive: true,
            svgoPlugins: [{removeViewBox: false}],
            use: [pngquant()],
            interlaced: true
        }))
        .pipe(rename(correctRename))
        .pipe(gulp.dest(template.build.img))

});

//#endregion =================================End image============================================

//#region ===================================Svg============================================
gulp.task('dev-svg-sprite', function () {

    const config = {
        transform: [{svgo: {
            js2svg: {pretty: true}, // Отключаем минификацию svg.
            plugins: [
              {cleanupListOfValues: {floatPrecision: 0}},
              {inlineStyles: {onlyMatchedOnce: false}},
              {removeAttrs: {attrs: [
                'stroke', 
                'data-name', 
                'style'
            ]}},
              {removeAttributesBySelector: {selector: ':not([fill="none"])', attributes: ['fill']}}
            ]
          }}],
            mode: {
                stack: {
                    sprite: "../sprite.svg"
                }
            }
        }

    return gulp.src(template.src.svg) 
        .pipe(svgSprite(config))
        .pipe(gulp.dest(template.build.svg));
});

gulp.task('prod-svg-sprite', function () {

    const config = {
        mode: {
            stack: {
                sprite: "../sprite.svg"
            }
        }
    }

    return gulp.src(template.src.svg)
        .pipe(svgSprite(config))
        .pipe(gulp.dest(template.build.svg));
});
//#endregion ===================================End svg====================================

//#region ====================================Fonts=========================================

gulp.task('fonts', function () {
    return gulp.src(template.src.fonts)
        .pipe(gulp.dest(template.build.fonts))
});

//#endregion ====================================End fonts=================================

//#region ====================================Build==========================================

gulp.task('dev-build-lite', gulp.parallel([
    'dev-scripts',
    'dev-css',
]));

gulp.task('dev-build', gulp.parallel([
    'fonts',
    'dev-scripts',
    'dev-css',
    'dev-image',
    'dev-svg-sprite'
]));

gulp.task('prod-build', gulp.parallel([
    'fonts',
    'prod-scripts',
    'prod-css',
    'prod-image',
    'prod-svg-sprite'
]));

gulp.task('clean', function () {
    return gulp.src([template.clean], {read: false, allowEmpty: true})
        .pipe(clean({force: true}));
});

gulp.task('clean-and-build-dev', gulp.series(['clean', 'dev-build']));
gulp.task('clean-and-build-prod', gulp.series(['clean', 'prod-build']));

//#endregion ====================================End build=============================================


gulp.task('browser-sync', function () {
    browserSync.init({
        proxy: SYNC_START_PAGE,
        browser: SYNC_BROWSER
    });
});


gulp.task('watch-lite', function () {
    gulp.watch(watch.scss, gulp.series('dev-css'));
    gulp.watch(watch.js, gulp.series('dev-scripts'));
});

gulp.task('watch-only-pictures', function () {
    gulp.watch(watch.img, gulp.series('dev-image'));
    gulp.watch(watch.svg, gulp.series('dev-svg-sprite'));
});

gulp.task('watch-no-fonts', function () {
    gulp.watch(watch.scss, gulp.series('dev-css'));
    gulp.watch(watch.js, gulp.series('dev-scripts'));
    gulp.watch(watch.img, gulp.series('dev-image'));
    gulp.watch(watch.svg, gulp.series('dev-svg-sprite'));
});

gulp.task('watch-all', function () {
    gulp.watch(watch.scss, gulp.series('dev-css'));
    gulp.watch(watch.js, gulp.series('dev-scripts'));
    gulp.watch(watch.img, gulp.series('dev-image'));
    gulp.watch(watch.svg, gulp.series('dev-svg-sprite'));
    gulp.watch(watch.fonts, gulp.series('fonts'));
});


gulp.task('reload-watch-lite', gulp.parallel(['watch-lite', 'browser-sync']));
gulp.task('reload-watch-only-pictures', gulp.parallel(['watch-only-pictures', 'browser-sync']));
gulp.task('reload-watch-no-fonts', gulp.parallel(['watch-no-fonts', 'browser-sync']));
gulp.task('reload-watch-all', gulp.parallel(['watch-all', 'browser-sync']));

gulp.task('dev-build-reload-watch-all', gulp.series(['clean', 'dev-build', 'reload-watch-all']));
