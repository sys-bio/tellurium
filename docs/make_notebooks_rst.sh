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

# notebook directory
NBDIR=$DIR/../examples/notebooks/core
# widget notebook directory
WIDGETDIR=$DIR/../examples/notebooks/widgets
# output directory
NBOUTDIR=$DIR/_notebooks/core

# clean output dir
rm -rf ${NBOUTDIR}
mkdir -p ${NBOUTDIR}
cd ${NBOUTDIR}

# convert the notebooks to rst after running headlessly
# if errors should abort, remove the --allow-errors option
# jupyter nbconvert --to=rst --allow-errors --execute $NBDIR/*.ipynb
# In the process the notebooks are completely executed
nsucceeded=0
nfailed=0
for f in $NBDIR/*.ipynb; do
    b=$(basename $f)
    l=$b.log
    logfile=/tmp/$l
    echo "Converting $b -> log $logfile"
    jupyter nbconvert --to=rst --allow-errors --output-dir=${NBOUTDIR} --execute $f >$logfile 2>&1
    if [ ! $? -eq 0 ]; then
        echo "  Failed: $b"
        nfailed=$((nfailed+=1))
    else
        nsucceeded=$((nsucceeded+=1))
    fi
done
#jupyter nbconvert --to=rst --allow-errors --output-dir=${NBOUTDIR} --execute $WIDGETDIR/*.ipynb
echo "DONE converting notebooks"
echo -e "  Succeeded: $nsucceeded, Failed: $nfailed\n\n"

echo "--------------------------------------"
echo "postprocessing rst"
echo "--------------------------------------"
# remove the following lines from the documentation
sed -i '/%matplotlib inline/d' ./*.rst
sed -i '/Back to the main `Index <..\/index.ipynb>`__/d' ./*.rst
sed -i '/from __future__ import print_function/d' ./*.rst
sed -i '/te.setDefaultPlottingEngine("matplotlib")/d' ./*.rst

# change the image locations
# .. image:: consecutiveUniUniReactions_files/consecutiveUniUniReactions_2_0.png
echo "Changing image paths..."
sed -i -- 's/.. image:: /.. image:: _notebooks\/core\//g' ./*.rst
echo "Patching code directives"
# readthedocs cannot handle ipython3 code blocks
# readthedocs also cannot handle the code:: directive, need code-block instead
sed -i -- 's/.. code:: ipython3/.. code-block:: python/g' ./*.rst
echo "DONE postprocessing"

# skip this part for now, doesn't seem to work
if false; then
    echo "--------------------------------------"
    echo "create python code"
    echo "--------------------------------------"
    # clean output dir
    PYOUTDIR=$DIR/../examples/notebooks-py
    rm -rf $PYOUTDIR
    mkdir -p $PYOUTDIR

    # create python files
    cd $PYOUTDIR
    # jupyter nbconvert --to=python --allow-errors --execute $NBDIR/*.ipynb
    jupyter nbconvert --to=python --allow-errors --execute --output-dir=${PYOUTDIR} $NBDIR/*.ipynb

    # replace the magic & add warning
    sed -i -- "s/get_ipython().magic(u'matplotlib inline')/\#\!\!\! DO NOT CHANGE \!\!\! THIS FILE WAS CREATED AUTOMATICALLY FROM NOTEBOOKS \!\!\! CHANGES WILL BE OVERWRITTEN \!\!\! CHANGE CORRESPONDING NOTEBOOK FILE \!\!\!/g" ./*.py
    echo "DONE converting to Python scripts"
fi
