
# coding: utf-8

# Back to the main [Index](../index.ipynb)

# #### Antimony, SBML, CellML

# In[1]:

#!!! DO NOT CHANGE !!! THIS FILE WAS CREATED AUTOMATICALLY FROM NOTEBOOKS !!! CHANGES WILL BE OVERWRITTEN !!! CHANGE CORRESPONDING NOTEBOOK FILE !!!
from __future__ import print_function
import tellurium as te

# antimony model
ant_model = """
    S1 -> S2; k1*S1;
    S2 -> S3; k2*S2;

    k1= 0.1; k2 = 0.2; 
    S1 = 10; S2 = 0; S3 = 0;
"""

# convert to SBML
sbml_model = te.antimonyToSBML(ant_model)

# convert to CellML
cellml_model = te.antimonyToCellML(ant_model)

# or from the sbml
cellml_model = te.sbmlToCellML(sbml_model)


# In[2]:



