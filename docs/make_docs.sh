#!/bin/bash
###############################################################
# Build script for tellurium documentation from rst files and 
# python docstrings in the tellurium package
#
# execute this script in the docs folder i.e., after
# 	cd tellurium/docs
#
# Usage: 
#	./make_docs.sh 2>&1 | tee ./make_docs.log
#
# The documentation is written in docs/_build
###############################################################
# remove old documentation
rm -rf _apidoc
rm -rf _built
rm -rf _notebooks

# create the rst files from the notebooks
./make_notebooks_rst.sh 2>&1 | tee ./make_notebooks_rst.log

# create auto documentation for tellurium package.
sphinx-apidoc -o _apidoc ../tellurium

# create html documentation
make html
# make a pdf
# make latexpdf

# the new documentation is now in docs/_built
firefox _build/html/index.html

