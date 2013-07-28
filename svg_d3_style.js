var system = require('system');

if (system.args.length != 2) {
  console.log("Usage: svg_d3.js_style url");
  phantom.exit(1);
}

var address = system.args[1];
var page = require('webpage').create();
//page.settings.resourceTimeout = 3000;

function extract() {
  return function (status) {
    if (status != 'success') {
      console.log("Failed to open the page.");
    } else {
   window.setTimeout(function () {
      var css = page.evaluate(function () {
        var stylesheets = document.getElementsByTagName('style');
        var css_style_tag = [];
        if (stylesheets.length > 0) {
          for (var i = 0, len = stylesheets.length; i < len; i++) {
            css_style_tag.push(stylesheets[i].innerHTML);
          }
          return css_style_tag.join('\n');
        } else {
          return "False";
        }
      });
      console.log(css);
      phantom.exit();
    }, 200);
    }
  };
}

page.open(address, extract());
