
# coding: utf-8

# Back to the main [Index](../index.ipynb)

# ### Test models

# In[1]:

#!!! DO NOT CHANGE !!! THIS FILE WAS CREATED AUTOMATICALLY FROM NOTEBOOKS !!! CHANGES WILL BE OVERWRITTEN !!! CHANGE CORRESPONDING NOTEBOOK FILE !!!
from __future__ import print_function
import tellurium as te

# To get the builtin models use listTestModels
print(te.listTestModels())


# #### Load test model

# In[2]:

# To load one of the test models use loadTestModel:
# r = te.loadTestModel('feedback.xml')
# result = r.simulate (0, 10, 100)
# r.plot (result)

# If you need to obtain the SBML for the test model, use getTestModel
sbml = te.getTestModel('feedback.xml')

# To look at one of the test model in Antimony form:
ant = te.sbmlToAntimony(te.getTestModel('feedback.xml'))
print(ant)

