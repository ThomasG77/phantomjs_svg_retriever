#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Phantomjs SVG retriever

Usage:
  phantom_svg_retriever.py web
  phantom_svg_retriever.py no_server <url> <dom_id>
  phantom_svg_retriever.py no_server <url> <dom_id> <image_name>
  phantom_svg_retriever.py (-h | --help)
  phantom_svg_retriever.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""

from bottle import route, request, response, run, template, debug
from PIL import Image
from docopt import docopt
#from lxml.html import parse
import os
import subprocess
import tempfile
import cStringIO
import cairo
import rsvg

APP_ROOT = os.path.dirname(os.path.realpath(__file__))
PHANTOM = '/opt/phantomjs-1.9.1-linux-x86_64/bin/phantomjs'
SCRIPT = os.path.join(APP_ROOT, 'svg_d3.js')
SCRIPT_STYLE = os.path.join(APP_ROOT, 'svg_d3_style.js')
SCRIPT_SVG = os.path.join(APP_ROOT, 'rasterize.js')
BATIK_PATH = "/opt/batik-1.7/batik-rasterizer.jar"

def executePhantomSVG (url, dom_id, file):
    params = [PHANTOM, SCRIPT, url, dom_id]
    output = subprocess.check_output(params)
    #doc = parse(url).getroot()
    params_style = [PHANTOM, SCRIPT_STYLE, url]
    output_style = subprocess.check_output(params_style)
    # We dont loop and consider only one style
    css_name = None
    if output_style != "False\n":
        # Empty/Create the local file with style
        css_name = "style.css"
        f = open(css_name, 'w')
        f.write(output_style)
        f.close()
        # Dirty way: no parsing just string manipulation...
        splitter = output.split('<svg')
        if len(splitter) > 1:
            svg_styles_files = splitter[0]
            svg_str = splitter[1]
        else:
            svg_styles_files = ""
            svg_str = splitter[0]
        output = svg_styles_files + '<?xml-stylesheet type="text/css" href="' + css_name + '" ?>\n' + '<svg' + svg_str

    output = '<?xml version="1.0" standalone="no"?>' + output
    output = output.replace('<svg ', '<svg xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:cc="http://creativecommons.org/ns#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:svg="http://www.w3.org/2000/svg" xmlns="http://www.w3.org/2000/svg" ')
    svg_base_name = "my_svg"
    svg_extension = ".svg"
    svg_name = svg_base_name + svg_extension
    f1 = open(svg_name, 'w')
    f1.write(output)
    f1.close()

    svg = rsvg.Handle(data=output)
    # Get SVG size (we dont deal with ratio or user defined size
    x = svg.props.width
    y = svg.props.height

    # Phantomjs svg converter
    params_phantomjs = [PHANTOM, SCRIPT_SVG, svg_name, svg_base_name + '.png', str(x) + '*' + str(y)]
    output_phantomjs = subprocess.check_output(params_phantomjs)
    img = Image.open(svg_base_name + '.png')
    format = 'PNG'
    img.save(file, format)
    os.remove(svg_name)
    if css_name != None:
         os.remove(css_name)


@route('/scrapesvg')
def index():
    # Retrieve parameters from URL
    url = request.params.get('url')
    dom_id = request.params.get('dom_id')

    # Rules to validate the incoming parameters
    if url and dom_id:
        validated = True
    else:
        return "Please provide an url with an url parameter refering webpage you want to scrape and dom_id to get the SVG id. A working example will look like http://localhost:8080/scrapesvg?dom_id=us-map&url=http://congress.joshreyes.com"
    # Prepare to execute PhantomJS
    buf = cStringIO.StringIO()
    executePhantomSVG(url, dom_id, buf)

    if validated:
        response.content_type = 'image/png'
        stream_content = buf.getvalue()
        buf.close()
        #response.set_header('Content-Disposition', 'attachment; filename="test.png"')
        response.set_header('Content-Length', str(len(stream_content)))
        return stream_content



if __name__ == '__main__':
    arguments = docopt(__doc__, version='Phantom SVG retriever 0.1')
    if arguments.get('web') == True:
        run(host='localhost', port=8080, reloader=True)
    if  arguments.get('no_server') == True:
        if arguments.get('<image_name>') != None:
            img_name = arguments.get('<image_name>')
        else:
            img_name = "my_png.png"
        executePhantomSVG(arguments.get('<url>'), arguments.get('<dom_id>'), img_name)
