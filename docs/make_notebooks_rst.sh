#!/bin/bash
###############################################################
# Create the rst directly from the ipynb files
#  ./make_notebooks_rst.sh 2>&1 | tee ./make_notebooks_rst.log
###############################################################
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

date
echo "--------------------------------------"
echo "convert notebooks to rst"
echo "--------------------------------------"
NBDIR=$DIR/../examples/notebooks/core
NBOUTDIR=$DIR/_notebooks/core

rm -rf $NBOUTDIR
mkdir -p $NBOUTDIR
cd $NBOUTDIR
# convert the notebooks to rst after running headlessly
# if errors should abort, remove the --allow-errors option
# ipython nbconvert --to=rst --allow-errors --execute $NBDIR/*.ipynb
ipython nbconvert --to=rst --execute $NBDIR/*.ipynb
echo "DONE"

echo "--------------------------------------"
echo "postprocessing rst"
echo "--------------------------------------"
# remove the following lines from the documentation
sed -i '/%matplotlib inline/d' ./*.rst
sed -i '/Back to the main `Index <..\/index.ipynb>`__/d' ./*.rst
sed -i '/from __future__ import print_function/d' ./*.rst

# change the image locations
# .. image:: consecutiveUniUniReactions_files/consecutiveUniUniReactions_2_0.png
sed -i -- 's/.. image:: /.. image:: _notebooks\/core\//g' ./*.rst
echo "DONE"

echo "--------------------------------------"
echo "create python code"
echo "--------------------------------------"
PYOUTDIR=$DIR/../examples/notebooks-py
rm -rf $PYOUTDIR
mkdir -p $PYOUTDIR

# create python files next to the notebooks
cd $PYOUTDIR
# ipython nbconvert --to=python --allow-errors --execute $NBDIR/*.ipynb
ipython nbconvert --to=python --execute $NBDIR/*.ipynb

# replace the magic & add warning
sed -i -- "s/get_ipython().magic(u'matplotlib inline')/\#\!\!\! DO NOT CHANGE \!\!\! THIS FILE WAS CREATED AUTOMATICALLY FROM NOTEBOOKS \!\!\! CHANGES WILL BE OVERWRITTEN \!\!\! CHANGE CORRESPONDING NOTEBOOK FILE \!\!\!/g" ./*.py
echo "DONE"
