const fs = require('fs')

// List all JS files and minify them
const jsFolder = fs.readdirSync('./static/js')
const jsFiles = []
for (const file of jsFolder) {
  // Check if file is JS file
  if (file.slice(-3) === '.js') {
    // If file is JS file, push it to array
    jsFiles.push('./static/js/' + file)
  }
};
require('esbuild').build({
  entryPoints: jsFiles,
  entryNames: '[name].min',
  minify: true,
  sourcemap: true,
  outdir: './static/js_min/'

}).catch(() => process.exit(1))

// List all CSS files and minify them
const cssFolder = fs.readdirSync('./static/css')
const cssFiles = []
for (const file of cssFolder) {
  // Check if file is CSS file
  if (file.slice(-4) === '.css') {
    // If file is CSS file, push it to array
    cssFiles.push('./static/css/' + file)
  }
};
require('esbuild').build({
  entryPoints: cssFiles,
  entryNames: '[name].min',
  minify: true,
  sourcemap: true,
  outdir: './static/css_min/'
}).catch(() => process.exit(1))
