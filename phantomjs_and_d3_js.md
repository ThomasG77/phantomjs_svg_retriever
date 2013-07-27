## Install (tested only on Ubuntu 12.04)

### PhantomJS install

    cd /opt/
    wget https://phantomjs.googlecode.com/files/phantomjs-1.9.1-linux-x86_64.tar.bz2
    sudo tar xvjf phantomjs-1.9.1-linux-x86_64.tar.bz2
    sudo chmod -R 777 phantomjs-1.9.1-linux-x86_64
    sudo rm phantomjs-1.9.1-linux-x86_64.tar.bz2
    sudo apt-get install libfreetype6 fontconfig
    echo 'export PATH=$PATH:/opt/phantomjs-1.9.1-linux-x86_64/bin' >> ~/.bashrc
    source ~/.bashrc

### Python install part

    sudo apt-get install python-setuptools
    sudo apt-get install python-rsvg
    sudo apt-get install libcairo2
    sudo easy_install pip
    sudo pip install bottle
    sudo pip install docopt

## Time for action

### Generate an SVG from a D3.js charts, graphs, maps,...

    phantomjs svg_d3.js http://congress.joshreyes.com timeline > my_svg.svg

### Convert to image with ImageMagick (RSVG or other tools can be used)

    convert my_svg.svg -background white -flatten my_jpg.jpg

## My solution

### Web side

Launch

    python phantom_svg_retriever.py web

Open your browser to [http://localhost:8080/scrapesvg?dom_id=us-map&url=http://congress.joshreyes.com](http://localhost:8080/scrapesvg?dom_id=us-map&url=http://congress.joshreyes.com) and enjoy

PhantomJS throught Python (generate also the image, PNG only supported at the moment)

    python phantom_svg_retriever.py no_server http://congress.joshreyes.com timeline

If you want to change the default png name

    python phantom_svg_retriever.py no_server http://congress.joshreyes.com timeline my_new_name.png

In both case, see  your directory: a new png file was created

## Sources:

### Directly related

 * https://blogs.law.harvard.edu/jreyes/2012/12/13/render-d3-js-driven-svg-server-side/
 * http://charlesleifer.com/blog/building-bookmarking-service-python-and-phantomjs/
 * http://techslides.com/grabbing-html-source-code-with-phantomjs-or-casperjs/

### Others way to do it

 * http://d3export.cancan.cshl.edu

### With Fabric Js, convert to Canvas and after you can convert to image

 * http://jsdo.it/_shimizu/KcEf
