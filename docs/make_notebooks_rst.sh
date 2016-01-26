#!/bin/bash
###############################################################
# Create the rst directly from the ipynb files
#
#
#
#
###############################################################

# convert the notebooks to rst after running headlessly
NOTEBOOK="notebooks/core/computeSteadyStat.ipynb"
ipython nbconvert --to=rst --ExecutePreprocessor.enabled=True $NOTEBOOK


# remove the %matplotlib inline line


# change the file naming & file location
