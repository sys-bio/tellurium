"""
Provides trivial wrappers around pip.
"""
from __future__ import print_function, division, absolute_import

import pip

def searchPackage(name):
    pip.main(['search', name])

def installPackage(name):
    pip.main(['install', name])

def uninstallPackage(name):
    pip.main(['uninstall', '-y', name])
