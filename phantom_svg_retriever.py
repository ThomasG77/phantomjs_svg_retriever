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
from lxml.html import parse
import os
import subprocess
import tempfile
import cStringIO
import cairo
import rsvg

APP_ROOT = os.path.dirname(os.path.realpath(__file__))
PHANTOM = '/opt/phantomjs-1.9.1-linux-x86_64/bin/phantomjs'
SCRIPT = os.path.join(APP_ROOT, 'svg_d3.js')

def convert(data, ofile):
    # Create rsvg object from retrieve SVG
    svg = rsvg.Handle(data=data)
    
    # Get SVG size (we dont deal with ratio or user defined size
    x = svg.props.width
    y = svg.props.height
    
    # Create a cairo canevas
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, x, y)
    context = cairo.Context(surface)

    # Add background color (using SVG, so transparency...)
    context.set_source_rgb(1, 1, 1) # blue
    context.rectangle(0, 0, x, y)
    context.fill()

    # Render context and write to file or stream
    svg.render_cairo(context)
    surface.write_to_png(ofile)

def executePhantomSVG (url, dom_id, file):
    params = [PHANTOM, SCRIPT, url, dom_id]
    output = subprocess.check_output(params)
    doc = parse(url).getroot()
    # We dont loop and consider only one style
    if doc.body.head.find('style') != None:
        my_style = doc.body.head.find('style').text
        # Empty/Create the local file with style
        f = open('style.css', 'w')
        f.write(my_style)
        f.close()
        # Dirty way: no parsing just string manipulation...
        splitter = output.split('<svg')
        svg_styles_files = splitter[0]
        svg_str = splitter[1]
        output = svg_styles_files + '<?xml-stylesheet type="text/css" href="style.css" ?>\n' + '<svg' + svg_str

    convert(output, file)

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
