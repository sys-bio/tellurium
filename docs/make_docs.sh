#!/bin/bash
###############################################################
# Build script for tellurium documentation from rst files and 
# python docstrings in the tellurium package
#
# execute this script in the docs folder i.e., after
# 	cd tellurium/docs
#
# The documentation is written in docs/_build
###############################################################
# remove old documentation
rm -rf _apidoc
rm -rf _built

# create auto documentation for tellurium package.
sphinx-apidoc -o _apidoc ../tellurium

# create html documentation
make html

# the new documentation is now in docs/_built
firefox _build/html/index.html

