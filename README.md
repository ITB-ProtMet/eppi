# EPPI

 eppi - experimental proteotypic peptides investigator

**TO DO**: *Explain better `make.py` options* 

## Before to use EPPI
EPPI imports a Cython Param library with cython. Before to run EPPI you need to build this library.

     cd eppi/EPPI/peptidome/commons/
     python setup.py build_ext --inplace

*TO DO: I would manage this step in make.py file*

Eppi requires other external library:
 - [wx](http://wxpython.org/),
 - [matplotlib](http://matplotlib.org/),
 - [xlrd](http://www.python-excel.org/),
 - [jinja2](http://jinja.pocoo.org/),
 - [cython](http://cython.org).

To manage tests in EPPI (not yet Functional regrettably) we use [nosetests](https://nose.readthedocs.org/en/latest/).
I could run the `make.py`

    make.py test

that uses 

    nosetests --with-doc

## Building executable
To compile EPPI in an executable you need the latest version of
[pyinstaller](https://github.com/pyinstaller/pyinstaller/wiki).

For Windows you could build also an installer, but you need
[InnoSetup](http://www.jrsoftware.org/isinfo.php).
**TO DO**: *Manage this issue with `make,py`*
Edit `scb.iss` to set the correct paths.
We include also two makefiles to run (we use gnu make) the compiling pipe,
you need only to edit them to define your local paths.

    cd eppi

For windows:

    make -f Makefile_win_27.mak

For linux:

    make -f Makefile_linux.mak

or, for an executable that depends on OS in use type directly:

    python make.py dist

## Notes about resource used

The Eppi main interface comes from a IBM example. You can see the code [here](http://wiki.wxpython.org/WxProject).
or in the doc package in wxPython
"wxPythonx.y Docs and Demos/samples/wxProject/wxProject.py".

The dialog creation in `DialogCommons.py` is modified from Demo Dialog code. You can find the original code in the doc package in wxPython
"wxPythonx.y Docs and Demos/demo/Dialog.py".

The prj file management is inspired by a [Active Python recipe](http://code.activestate.com/recipes/576642/)
written by Raymond Hettinger - Wed, 4 Feb 2009 (MIT).

The [logo](https://commons.wikimedia.org/wiki/Tango_icons#mediaviewer/File:Face-glasses.svg)
is an image from Tango icons set.
The image is under public domain.

I copied the idea of `make.py` to [cryptully of Shanet](https://github.com/shanet/Cryptully/blob/master/make.py).


