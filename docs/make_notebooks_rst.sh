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
OUTDIR=$DIR/_notebooks/core

rm -rf $OUTDIR
mkdir -p $OUTDIR
cd $OUTDIR
# convert the notebooks to rst after running headlessly
# if errors should abort, remove the --allow-errors option
ipython nbconvert --to=rst --allow-errors --execute $NBDIR/*.ipynb

echo "--------------------------------------"
echo "postprocessing rst"
echo "--------------------------------------"
cd $OUTDIR

# remove the following lines from the documentation
sed -i '/%matplotlib inline/d' ./*.rst
sed -i '/Back to the main `Index <..\/index.ipynb>`__/d' ./*.rst
sed -i '/from __future__ import print_function/d' ./*.rst

# change the image locations
# .. image:: consecutiveUniUniReactions_files/consecutiveUniUniReactions_2_0.png
sed -i -- 's/.. image:: /.. image:: _notebooks\/core\//g' ./*.rst

