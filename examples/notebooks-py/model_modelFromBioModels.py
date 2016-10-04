
# coding: utf-8

# Back to the main [Index](../index.ipynb)

# ### Model loading from BioModels
# Models can be easily retrieved from BioModels via their identifier.

# In[1]:

#!!! DO NOT CHANGE !!! THIS FILE WAS CREATED AUTOMATICALLY FROM NOTEBOOKS !!! CHANGES WILL BE OVERWRITTEN !!! CHANGE CORRESPONDING NOTEBOOK FILE !!!
from __future__ import print_function
import tellurium as te

# Load model from biomodels.
r = te.loadSBMLModel("http://www.ebi.ac.uk/biomodels-main/download?mid=BIOMD0000000010")
result = r.simulate(0, 3000, 5000)
r.plot(result);


# In[2]:



