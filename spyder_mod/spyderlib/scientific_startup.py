# -*- coding: utf-8 -*-
#
# Copyright © 2011 Pierre Raybaut
# Licensed under the terms of the MIT License
# (see spyderlib/__init__.py for details)

"""
Scientific Python startup script

Requires NumPy, SciPy and Matplotlib
"""

from __future__ import division

__has_numpy = True
__has_scipy = True
__has_matplotlib = True

#the tellurium packages
__has_libantimony = True
__has_sbml2matlab = True
__has_roadrunner = True
__has_teplugins = True
__has_tellurium = True

#==============================================================================
# Pollute the namespace but also provide MATLAB-like experience
#==============================================================================
try:
    from pylab import *  #analysis:ignore
    # Enable Matplotlib's interactive mode:
    ion()
except ImportError:
    pass

# Import modules following official guidelines:
try:
    import numpy as np
except ImportError:
    __has_numpy = False

try:
    import scipy as sp
except ImportError:
    __has_scipy = False

try:
    import matplotlib as mpl
    import matplotlib.pyplot as plt  #analysis:ignore
except ImportError:
    __has_matplotlib = False

#TELLURIUM IMPORTS

try:
    import sbml2matlab
except ImportError:
    __has_sbml2matlab = False

try:
    import roadrunner
except ImportError:
    __has_roadrunner = False

try:
    import libantimony
except ImportError:
    __has_libantimony = False

try:
    import teplugins
except ImportError:
    __has_teplugins = False

try:
    import tellurium as te
except ImportError:
    __has_tellurium = False

#==============================================================================
# Print what modules have been imported
#==============================================================================
__imports = ""
if __has_roadrunner:
    __imports += "Imported RoadRunner %s" % roadrunner.__version__.split(';')[0]
if __has_libantimony:
    __imports += ", libAntimony %s" % libantimony.LIBANTIMONY_VERSION_STRING
if __has_sbml2matlab:
    __imports += ", sbml2matlab %s" % sbml2matlab.__version__
if __has_teplugins:
    __imports += ", TePlugins %s" % teplugins.getVersion()
if __has_numpy:
    __imports += ", NumPy %s" % np.__version__
if __has_scipy:
    __imports += ", SciPy %s" % sp.__version__
if __has_matplotlib:
    __imports += ", Matplotlib %s" % mpl.__version__
if __has_tellurium:
    __imports += ", and Tellurium %s as 'te'" % te.__version__

if __imports:
    print __imports

#Not imported/ missing
__notimports = []
if not __has_roadrunner:
    __notimports.append("roadrunner")
if not __has_libantimony:
    __notimports.append("libantimony")
if not __has_sbml2matlab:
    __notimports.append("sbml2matlab")
if not __has_teplugins:
    __notimports.append("teplugins")
if not __has_numpy:
    __notimports.append("numpy")
#if not __has_scipy:
    #__notimports.append("scipy")
if not __has_matplotlib:
    __notimports.append("matplotlib")
if not __has_tellurium:
    __notimports.append("tellurium")

if __notimports:
    for fail in __notimports:
        from colorama import Fore, Style
    	print Fore.RED + Style.BRIGHT + "'import %s' failed" % fail

    print(Style.RESET_ALL)

import os
if os.environ.get('QT_API') != 'pyside':
    try:
        import guiqwt
        import guiqwt.pyplot as plt_
        import guidata
        plt_.ion()
        print "+ guidata %s, guiqwt %s" % (guidata.__version__,
                                           guiqwt.__version__)
    except ImportError:
        print

#==============================================================================
# Add help about the "scientific" command
#==============================================================================
def setscientific():
    """Set 'scientific' in __builtin__"""
    import __builtin__
    from site import _Printer
    infos = ""
    
    if __has_numpy:
        infos += """
This is a standard Python interpreter with preloaded tools for scientific 
computing and visualization. It tries to import the following modules:

>>> import numpy as np  # NumPy (multidimensional arrays, linear algebra, ...)"""

    if __has_scipy:
        infos += """
>>> import scipy as sp  # SciPy (signal and image processing library)"""

    if __has_matplotlib:
        infos += """
>>> import matplotlib as mpl         # Matplotlib (2D/3D plotting library)
>>> import matplotlib.pyplot as plt  # Matplotlib's pyplot: MATLAB-like syntax
>>> from pylab import *              # Matplotlib's pylab interface
>>> ion()                            # Turned on Matplotlib's interactive mode"""
    
    try:
        import guiqwt  #analysis:ignore
        infos += """
>>> import guidata  # GUI generation for easy dataset editing and display

>>> import guiqwt                 # Efficient 2D data-plotting features
>>> import guiqwt.pyplot as plt_  # guiqwt's pyplot: MATLAB-like syntax
>>> plt_.ion()                    # Turned on guiqwt's interactive mode"""
    except ImportError:
        pass
    
    if __has_numpy:
        infos += "\n"

    infos += """
Within Spyder, this interpreter also provides:
    * special commands (e.g. %ls, %pwd, %clear)
    * system commands, i.e. all commands starting with '!' are subprocessed
      (e.g. !dir on Windows or !ls on Linux, and so on)
"""
    __builtin__.scientific = _Printer("scientific", infos)


setscientific()
print 'Type "scientific" for more details.'

#==============================================================================
# Delete temp vars
#==============================================================================
del setscientific, __has_numpy, __has_scipy, __has_matplotlib, __imports
del __has_libantimony, __has_sbml2matlab, __has_roadrunner, __has_teplugins, __has_tellurium, __notimports


