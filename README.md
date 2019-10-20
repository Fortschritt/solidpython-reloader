# Solidpython Reloader

Automatically reload and recompile a solidpython project on file changes.

This tool is imitates Djangos *runserver* behaviour. Actually it depends on Django and
uses the Reloader class that powers *runserver*. 

# Installation

* If you already haven't done so for solidpython, optionally create a virtualenv
* pip install solidpython-reloader

# Usage

This package installs a script named *sp-reloader* into your PATH. You can use this to 
start a new project:
    sp-reloader startproject myproject

This creates a new project directory named *myproject*.

    $ ls myproject/
    myproject.py  myproject.scad  run.py

*myproject.py* is the file where your solidpython logic will reside in. 
*myproject.scad* will contain the translated openscad code. Right now, it is still empty.
*run.py* is the reloader for your project. If you want to start working on your project,
execute it:

    $ python run.py 
    INFO:root:Solidpython reloader started.

This starts the reloader, opens openscad and should render the sample code in *myproject.py*.

Now you are ready to model! Every time you save *myproject.py* or any other .py file in the
project directory, the scad file will be updated and rendered again.

# Customization

Out of the box, the *run.py* script observes changes in all *.py* and *.svg* files in the
current directory. You can add other files, file types or whole directories by adding
additional *reloader.watch_dir()* directives in *run.py*. You should add them after the
existing lines near the end of the file.