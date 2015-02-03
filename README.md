# EPPI

 eppi - experimental proteotypic peptides investigator
 
## Before to use EPPI
EPPI imports a Cython Param library with cython. Before to run EPPI you need to build this library. 

     cd eppi/EPPI/peptidome/commons/
     python setup.py build_ext --inplace
     
Eppi requires other external library, such wx, matplotlib or xlrd, but they are all stuff that you can install with distutils (easy_install) or pip.
To manage tests in EPPI (not yet Functional regrettably) we use nosetests and nose-exclude

    cd eppi
    nose --with-doc --exclude-dir=doc

## Building executable
To compile EPPI in an executable you need the latest version of 
[pyinstaller](https://github.com/pyinstaller/pyinstaller/wiki).
For Windows you could build also an installer, but you need 
[InnoSetup](http://www.jrsoftware.org/isinfo.php). 
Edit `scb.iss` to set the correct paths.
We include also two makefiles to run (we use gnu make) the compiling pipe, 
you need only to edit them to define your local paths.

    cd eppi
  
For windows:

    make -f Makefile_win_27.mak
  
For linux:

    make -f Makefile_linux.mak

## Notes about resource used

The Eppi main interface comes from a IBM example. You can see the code [here](http://wiki.wxpython.org/WxProject). 
or in the doc package in wxPython 
"wxPythonx.y Docs and Demos/samples/wxProject/wxProject.py".

The prj file management is inspired by a [Active Python recipe](http://code.activestate.com/recipes/576642/) 
written by Raymond Hettinger - Wed, 4 Feb 2009 (MIT). 
 
The [logo](https://commons.wikimedia.org/wiki/Tango_icons#mediaviewer/File:Face-glasses.svg) 
is an image from Tango icons set.
The image is under public domain.