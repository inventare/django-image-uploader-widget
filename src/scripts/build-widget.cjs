const { build } = require('esbuild');
const buildOptions = require('yargs-parser')(process.argv.slice(2), {
  boolean: ['debug', 'sourcemap'],
});

build({
  entryPoints: ['src/widget.ts'],
  bundle: true,
  minify: !buildOptions.debug,
  sourcemap: buildOptions.sourcemap,
  outfile: 'image_uploader_widget/static/admin/js/image-uploader-widget' + (buildOptions.debug ? '' : '.min') + '.js',
  plugins: [],
  target: ['es2020', 'chrome84', 'firefox84', 'safari14', 'edge84']
}).catch(() => process.exit(1));
