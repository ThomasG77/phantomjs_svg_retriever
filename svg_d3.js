var system = require('system');

if (system.args.length != 3) {
  console.log("Usage: svg_d3.js url dom_id. If no id, use 'no_id' for dom_id value");
  phantom.exit(1);
}

var address = system.args[1];
var elementID = system.args[2];
var page = require('webpage').create();
//page.settings.resourceTimeout = 3000;

function serialize(elementID) {
  var serializer = new XMLSerializer();
  if (elementID == 'no_id') {
    var element = document.getElementsByTagName('svg');
    element =  element[0];
  } else {
    var element = document.getElementById(elementID);
  }
  
  return serializer.serializeToString(element);
}

function extract(elementID) {
  return function (status) {
    if (status != 'success') {
      console.log("Failed to open the page.");
    } else {
   window.setTimeout(function () {
      var output = page.evaluate(serialize, elementID);

      var js = page.evaluate(function () {
        var stylesheets = document.getElementsByTagName('link');
        var xml_css_ref = [];

        for (var i = 0, len = stylesheets.length; i < len; i++) {
          xml_css_ref.push('<?xml-stylesheet type="text/css" href="' + stylesheets[i].href + '" ?>');
        }
        return xml_css_ref;
      });

      console.log(js.join('\n') + '\n' + output);
      phantom.exit();
    }, 1500);
    }
  };
}

page.open(address, extract(elementID));
