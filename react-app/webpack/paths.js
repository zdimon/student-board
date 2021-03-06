const path = require('path');

module.exports = {
  root: path.resolve(__dirname, '../'),
  outputPath: path.resolve(__dirname, '../../', 'sb/static/build'),
  entryPath: path.resolve(__dirname, '../', 'src/index.jsx'),
  templatePath: path.resolve(__dirname, '../', 'src/template.html'),
  imagesFolder: 'images',
  fontsFolder: 'fonts',
  cssFolder: 'css',
  jsFolder: 'js',
};
